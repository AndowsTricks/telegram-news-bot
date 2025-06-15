import feedparser
import json
import os
import requests
from summarizer import summarize_article
from translator import translate_text
from image_handler import get_image_url
from time import sleep

# Load config
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
POST_INTERVAL = int(os.getenv("POST_INTERVAL", "1800"))
  # Default: 30 min

# Load posted URLs
if os.path.exists("posted.json"):
    with open("posted.json", "r") as f:
        posted = set(json.load(f))
else:
    posted = set()

# Load RSS URLs
with open("rss_feeds.txt", "r") as f:
    feeds = [line.strip() for line in f if line.strip()]

print("Bot is running...\n")

while True:
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            link = entry.link
            if link in posted:
                continue

            title = entry.title
            summary = summarize_article(link)
            summary_si = translate_text(summary)
            image_url = get_image_url(link)

            caption = f"\u2728 {title}\n\n{summary_si}\n\n\ud83d\udd17 {link}"
            send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

            payload = {
                "chat_id": CHANNEL_ID,
                "caption": caption,
                "photo": image_url or "https://via.placeholder.com/150"
            }

            try:
                res = requests.post(send_url, data=payload)
                if res.status_code == 200:
                    posted.add(link)
                    with open("posted.json", "w") as f:
                        json.dump(list(posted), f, indent=2)
                    print(f"Posted: {title}")
                else:
                    print(f"Failed to post: {res.text}")
            except Exception as e:
                print(f"Error: {e}")

            sleep(10)  # avoid spamming
    print("Sleeping before next check...")
    sleep(POST_INTERVAL)

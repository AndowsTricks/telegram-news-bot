import os
import time
import json
import feedparser
import requests
from translator import translate_to_sinhala

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
POST_INTERVAL = int(os.getenv("POST_INTERVAL", "1800"))
HF_TOKEN = os.getenv("HF_TOKEN")

POSTED_FILE = "posted.json"
RSS_FEEDS_FILE = "rss_feeds.txt"

def load_posted_ids():
    if not os.path.exists(POSTED_FILE):
        return set()
    with open(POSTED_FILE, "r") as f:
        return set(json.load(f))

def save_posted_ids(posted_ids):
    with open(POSTED_FILE, "w") as f:
        json.dump(list(posted_ids), f)

def get_summary(text):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text[:1024]}
    response = requests.post(
        "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
        headers=headers,
        json=payload
    )
    try:
        return response.json()[0]["summary_text"]
    except Exception:
        return text[:300]

def post_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def main():
    posted_ids = load_posted_ids()
    while True:
        with open(RSS_FEEDS_FILE, "r") as f:
            feeds = f.read().splitlines()
        for feed_url in feeds:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:
                post_id = entry.get("id", entry.get("link"))
                if post_id in posted_ids:
                    continue
                summary = get_summary(entry.get("summary", entry.get("description", "")))
                sinhala = translate_to_sinhala(summary)
                post = f"<b>{entry.title}</b>

{summary}

🌐 <i>{sinhala}</i>
🔗 {entry.link}"
                post_to_telegram(post)
                posted_ids.add(post_id)
        save_posted_ids(posted_ids)
        time.sleep(POST_INTERVAL)

if __name__ == "__main__":
    main()

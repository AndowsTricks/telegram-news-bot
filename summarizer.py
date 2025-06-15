
from transformers import pipeline

# Load model once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_article(url):
    try:
        import requests
        from bs4 import BeautifulSoup

        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.text for p in paragraphs])[:4000]

        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Summary error: {e}")
        return "Unable to summarize this article."

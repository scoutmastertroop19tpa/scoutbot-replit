
import requests
from bs4 import BeautifulSoup
import os
import json
from uuid import uuid4

urls = [
    "https://newtroop19tampa.com/",
    "https://newtroop19tampa.com/faq/",
    "https://newtroop19tampa.com/join/",
    "https://newtroop19tampa.com/about-troop-19/",
    "https://newtroop19tampa.com/welcome/",
    "https://newtroop19tampa.com/leadersguide/",
    "https://newtroop19tampa.com/knot-challenge/",
    "https://newtroop19tampa.com/advancement/",
    "https://newtroop19tampa.com/gallery/",
    "https://newtroop19tampa.com/donate/",
    "https://newtroop19tampa.com/contact/",
    "https://newtroop19tampa.com/newsletter/"
]

def clean_html(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    for script in soup(['script','style','header','footer','svg','form']):
        script.extract()
    return soup.get_text(separator=' ', strip=True)

def chunk_text(text, size=2000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + size)
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

data = []
for url in urls:
    try:
        text = clean_html(url)
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            data.append({
                "id": str(uuid4()),
                "source": url,
                "url": url,
                "chunk_index": i,
                "content": chunk
            })
    except Exception as e:
        print(f"Failed {url}: {e}")

os.makedirs("data", exist_ok=True)
with open("data/faq_site_chunks.json","w",encoding="utf-8") as f:
    json.dump(data,f,indent=2)

print("Data scraped and saved to data/faq_site_chunks.json")


# ScoutBot Self-Hosted

## Setup
1. Install Python 3.10+.
2. Run: `pip install -r requirements.txt`
3. Set your OpenAI API key: `export OPENAI_API_KEY='your-key'`
4. Run `python scrape_and_embed.py` to scrape site content and create `data/faq_site_chunks.json`.
5. Start the bot: `python app.py`
6. Visit http://localhost:5000 to test.

## Embedding on WordPress
- Upload to your server (SiteGround or similar).
- Use an iframe or reverse proxy to embed:
  `<iframe src="https://yourdomain.com:5000" style="border:none;width:400px;height:500px;"></iframe>`
- Or copy the floating bubble HTML/JS into a custom HTML block.

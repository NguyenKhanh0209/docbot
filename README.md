# DocBot VS-01

Clone of OptiSigns' OptiBot support assistant, built on Google Gemini File Search.

## Setup
1. `cp .env.sample .env` and fill in `GEMINI_API_KEY`
2. `pip install -r requirements.txt`
3. `python uploader/create_store.py` (auto-creates a File Search Store; copy the printed name into `.env`)

## Run locally
```bash
python main.py
```
This scrapes support.optisigns.com, diffs against `state/article_hashes.json`
(SHA-256 per article), and uploads only added/updated files to the Gemini
File Search Store, which auto-embeds and indexes them.

## Chunking strategy
Gemini File Search handles chunking and embedding automatically using
`gemini-embedding-001` — no manual chunk-size configuration is exposed via API.

## Stats (last run)
- Files scraped: 405 (support.optisigns.com, all categories)
- Files indexed in vector store: [điền số từ check_status.py]

## Daily job
Runs via GitHub Actions daily at 03:00 UTC.
Logs: https://github.com/<you>/docbot-vs-01/actions

## Sample Q&A
See `screenshot.png` — assistant answering "How do I add a YouTube video?"
with cited Article URLs, tested via `uploader/test_chat.py`.

## Notes
- Uses Gemini API free tier (no billing required); free tier terms allow
  Google to use inputs/outputs to improve products — acceptable here since
  source data is already public support documentation.
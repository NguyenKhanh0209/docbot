import requests, re, hashlib, json, os, html
from pathlib import Path
from markdownify import markdownify as md

BASE = "https://support.optisigns.com"
OUT_DIR = Path("data/articles")
HASH_FILE = Path("state/article_hashes.json")


def fetch_all_articles():
    articles, url = [], f"{BASE}/api/v2/help_center/articles.json?per_page=100"
    while url:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        data = r.json()
        articles.extend(data["articles"])
        url = data.get("next_page")
    return articles


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:80]


def html_to_clean_md(body_html, article):
    text = md(body_html, heading_style="ATX", code_language="")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    header = (
        f"# {article['title']}\n\n"
        f"Article URL: {article['html_url']}\n"
        f"Last Updated: {article['updated_at']}\n\n"
    )
    return header + text


def load_hashes():
    if HASH_FILE.exists():
        return json.loads(HASH_FILE.read_text())
    return {}


def save_hashes(h):
    HASH_FILE.parent.mkdir(exist_ok=True)
    HASH_FILE.write_text(json.dumps(h, indent=2))


def run():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    old_hashes = load_hashes()
    new_hashes = {}
    added, updated, skipped = [], [], []

    for art in fetch_all_articles():
        if not art.get("body"):
            continue
        content = html_to_clean_md(art["body"], art)
        digest = hashlib.sha256(content.encode()).hexdigest()
        slug = slugify(art["title"])
        fname = f"{slug}.md"
        new_hashes[fname] = digest

        if fname not in old_hashes:
            added.append(fname)
        elif old_hashes[fname] != digest:
            updated.append(fname)
        else:
            skipped.append(fname)
            continue  

        (OUT_DIR / fname).write_text(content, encoding="utf-8")

    save_hashes(new_hashes)
    print(f"Added: {len(added)}, Updated: {len(updated)}, Skipped: {len(skipped)}")
    return added, updated, skipped


if __name__ == "__main__":
    run()

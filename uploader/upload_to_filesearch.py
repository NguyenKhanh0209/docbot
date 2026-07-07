import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
ARTICLES_DIR = Path("data/articles")
STORE_NAME = os.environ["FILE_SEARCH_STORE_NAME"]

MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 3  
SLEEP_BETWEEN_UPLOADS = 1  
MIN_CONTENT_BYTES = 50  


def upload_one(fname: str, path: Path, retries: int = MAX_RETRIES) -> bool:
    for attempt in range(1, retries + 1):
        try:
            op = client.file_search_stores.upload_to_file_search_store(
                file=str(path),
                file_search_store_name=STORE_NAME,
                config={"display_name": fname},
            )
            while not op.done:
                time.sleep(2)
                op = client.operations.get(op)

            print(f"Indexed: {fname}")
            return True

        except Exception as e:
            print(f"  Attempt {attempt}/{retries} failed for {fname}: {e}")
            if attempt < retries:
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)

    print(f"FAILED after {retries} attempts: {fname}")
    return False


def validate_file(path: Path) -> str | None:
    if not path.exists():
        return "file not found"

    size = path.stat().st_size
    if size == 0:
        return "file is empty (0 bytes)"

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        return f"invalid UTF-8 encoding: {e}"

    if len(text.strip()) < MIN_CONTENT_BYTES:
        return f"content too short ({len(text.strip())} chars, likely empty article)"

    return None


def upload_delta(files_to_upload: list[str]) -> tuple[int, list[str]]:
    if not files_to_upload:
        print("No new/updated files to upload.")
        return 0, []

    success_count = 0
    failed_files = []

    for i, fname in enumerate(files_to_upload, start=1):
        path = ARTICLES_DIR / fname
        print(f"[{i}/{len(files_to_upload)}] Processing: {fname}")

        reason = validate_file(path)
        if reason:
            print(f"  SKIP ({reason})")
            failed_files.append(f"{fname} (skipped: {reason})")
            continue

        ok = upload_one(fname, path)
        if ok:
            success_count += 1
        else:
            failed_files.append(f"{fname} (upload failed)")

        time.sleep(SLEEP_BETWEEN_UPLOADS)

    print("\n" + "=" * 50)
    print(f"SUMMARY: {success_count}/{len(files_to_upload)} uploaded successfully")
    if failed_files:
        print(f"{len(failed_files)} file(s) had issues:")
        for f in failed_files:
            print(f"  - {f}")
    print("=" * 50)

    return success_count, failed_files


if __name__ == "__main__":
    all_files = sorted(f.name for f in ARTICLES_DIR.glob("*.md"))
    n, failed = upload_delta(all_files)
    print(f"\nUploaded {n}/{len(all_files)} files.")
    if failed:
        print(f"Files needing attention: {failed}")

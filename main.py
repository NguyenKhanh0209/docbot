import os
from dotenv import load_dotenv

load_dotenv()

from scraper.scrape import run as scrape_run
from uploader.upload_to_filesearch import upload_delta


def main():
    added, updated, skipped = scrape_run()
    delta = added + updated
    n, failed = upload_delta(delta)
    print(
        f"SUMMARY -> added:{len(added)} updated:{len(updated)} skipped:{len(skipped)} uploaded:{n} failed:{len(failed)}"
    )


if __name__ == "__main__":
    main()

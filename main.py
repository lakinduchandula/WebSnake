# main.py

import re
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


def sanitize_filename(url: str) -> str:
    parsed = urlparse(url)
    path_segments = [segment for segment in parsed.path.split("/") if segment]

    def normalize_segment(segment: str) -> str:
        segment = segment.lower()
        segment = segment.replace("_", "-")
        segment = segment.replace("%20", "-")
        segment = segment.replace("--", "-")

        if match := re.match(r"^(gh)[-_]?(\d+)$", segment):
            return f"{match.group(1)}-{match.group(2)}"
        if match := re.match(r"^(topic|t)[-_]?(\d+)$", segment):
            return f"t{match.group(2)}"
        if match := re.match(r"^(question|q)[-_]?(\d+)$", segment):
            return f"q{match.group(2)}"
        if segment in {"discussion", "view", "exam", "all", "questions", "answer", "answers", "page"}:
            return ""

        return re.sub(r"[^a-z0-9-]+", "-", segment).strip("-")

    normalized = [normalized for normalized in (normalize_segment(seg) for seg in path_segments) if normalized]

    if normalized:
        filename = "-".join(normalized[:4])
    else:
        filename = parsed.netloc.replace(".", "-").lower()

    filename = re.sub(r"-+", "-", filename).strip("-")
    return f"{filename}.png"


def capture_website(page, url: str) -> Path:
    screenshot_name = sanitize_filename(url)
    screenshot_path = SCREENSHOT_DIR / screenshot_name

    print(f"Navigating to {url}...")
    page.goto(url, wait_until="domcontentloaded", timeout=30_000)

    print("Skipping button click for now.")
    print(f"Taking screenshot to {screenshot_path}...")
    page.screenshot(path=str(screenshot_path), full_page=True)

    return screenshot_path


def main() -> None:
    url = input("Enter website URL: ").strip()

    if not url.startswith(("http://", "https://")):
        print("Invalid URL")
        return

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            screenshot_path = capture_website(page, url)
            browser.close()

        print(f"Screenshot saved: {screenshot_path}")

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
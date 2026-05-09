# main.py

from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


def sanitize_filename(url: str) -> str:
    parsed = urlparse(url)
    domain = parsed.netloc.replace(".", "_")
    path = parsed.path.replace("/", "_").strip("_")

    if not path:
        path = "home"

    return f"{domain}_{path}.png"


def capture_website(url: str) -> Path:
    screenshot_name = sanitize_filename(url)
    screenshot_path = SCREENSHOT_DIR / screenshot_name

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={"width": 1440, "height": 900}
        )

        page.goto(url, wait_until="networkidle")

        page.screenshot(
            path=str(screenshot_path),
            full_page=True
        )

        browser.close()

    return screenshot_path


def main() -> None:
    url = input("Enter website URL: ").strip()

    if not url.startswith(("http://", "https://")):
        print("Invalid URL")
        return

    try:
        screenshot_path = capture_website(url)
        print(f"Screenshot saved: {screenshot_path}")

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
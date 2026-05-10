# main.py

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)

CONFIG_FILE = Path("sites.json")


def load_config() -> dict:
    """Load configuration from sites.json"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"exam_family": "GH-900", "topic_number": 1, "last_question": 0}


def save_config(config: dict) -> None:
    """Save configuration to sites.json"""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def generate_screenshot_name(config: dict) -> str:
    """Generate screenshot filename from config data"""
    exam_family = config.get("exam_family", "GH-900")
    topic_number = config.get("topic_number", 1)
    last_question = config.get("last_question", 0)
    return f"{exam_family}-{topic_number}-{last_question}.png"


def capture_website(page, url: str, config: dict) -> tuple[Path, dict]:
    """Capture website screenshot and return path and updated config"""
    screenshot_name = generate_screenshot_name(config)
    screenshot_path = SCREENSHOT_DIR / screenshot_name

    print(f"Navigating to {url}...")
    page.goto(url, wait_until="domcontentloaded", timeout=30_000)

    print("Skipping button click for now.")
    print(f"Taking screenshot to {screenshot_path}...")
    page.screenshot(path=str(screenshot_path), full_page=True)

    # Increment the last_question number
    config["last_question"] += 1

    return screenshot_path, config


def main() -> None:
    while True:
        url = input("\nEnter website URL (or 'quit' to exit): ").strip()

        if url.lower() in {"quit", "exit", "q"}:
            print("Exiting...")
            break

        if not url.startswith(("http://", "https://")):
            print("Invalid URL. Please enter a valid URL starting with http:// or https://")
            continue

        # Load current configuration
        config = load_config()
        print(f"Current config: {config}")

        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1440, "height": 900})
                screenshot_path, updated_config = capture_website(page, url, config)
                browser.close()

            # Save updated configuration
            save_config(updated_config)
            print(f"Screenshot saved: {screenshot_path}")
            print(f"Updated config: {updated_config}")

        except Exception as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
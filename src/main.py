"""Automation to enable uploading a new fantasygrounds mod or ext file to the FG Forge and publishing it to the Live channel"""

import logging
import os
from pathlib import Path, PurePath

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from forge_api import ForgeItem, ForgeCredentials, ForgeURLs, ReleaseChannel

logging.basicConfig(level=logging.WARNING, format="%(asctime)s : %(levelname)s : %(message)s")
load_dotenv(Path(PurePath(__file__).parents[1], ".env"))

TIMEOUT_SECONDS: float = 15


def configure_headless_chrome() -> webdriver.ChromeOptions:
    """Prepare and return chrome options for using selenium for testing via headless systems like Github Actions"""
    options = webdriver.ChromeOptions()
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,1024")
    return options


def main() -> None:
    """Hey, I just met you, and this is crazy, but I'm the main function, so call me maybe."""
    new_file = Path(PurePath(__file__).parents[1], os.environ["FG_UL_FILE"])
    logging.debug("File upload path determined to be: %s", new_file)
    if not new_file.is_file():
        raise Exception(f"File at {str(new_file)} is not found.")

    creds = ForgeCredentials(os.environ["FG_USER_ID"], os.environ["FG_USER_NAME"], os.environ["FG_USER_PASS"])
    item = ForgeItem(creds, os.environ["FG_ITEM_ID"], timeout=TIMEOUT_SECONDS)
    urls = ForgeURLs()

    with webdriver.Chrome(service=Service(), options=configure_headless_chrome()) as driver:
        item.upload_and_publish(driver, urls, new_file, ReleaseChannel.LIVE)


if __name__ == "__main__":
    main()

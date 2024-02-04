"""Automation to enable uploading a new fantasygrounds mod or ext file to the FG Forge and publishing it to the Live channel"""

import logging
import os
from pathlib import Path, PurePath

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import build_processing
from forge_api import ForgeItem, ForgeCredentials, ForgeURLs, ReleaseChannel

logging.basicConfig(level=logging.INFO, format="%(asctime)s : %(levelname)s : %(message)s")

TIMEOUT_SECONDS: float = 7
CHROME_ARGS: list[str] = [
    "--remote-debugging-port=9222",
    "--headless=new",
    "--window-size=1280,1024",
]


def configure_headless_chrome() -> webdriver.ChromeOptions:
    """Prepare and return chrome options for using selenium for testing via headless systems like Github Actions"""
    options = webdriver.ChromeOptions()
    [options.add_argument(arg) for arg in CHROME_ARGS]
    return options


def construct_objects() -> (list[Path], ForgeItem, ForgeURLs):
    """Get the build files,"""
    new_files = [build_processing.get_build(PurePath(__file__).parents[1], file) for file in os.environ["FG_UL_FILE"].split(",")]
    creds = ForgeCredentials(os.environ["FG_USER_NAME"], os.environ["FG_USER_PASS"])
    item = ForgeItem(creds, os.environ["FG_ITEM_ID"], TIMEOUT_SECONDS)
    urls = ForgeURLs()
    return new_files, item, urls


def main() -> None:
    """Hey, I just met you, and this is crazy, but I'm the main function, so call me maybe."""
    load_dotenv(Path(PurePath(__file__).parents[1], ".env"))
    new_files, item, urls = construct_objects()

    with webdriver.Chrome(service=Service(), options=configure_headless_chrome()) as driver:
        item.upload_and_publish(driver, urls, new_files, ReleaseChannel.LIVE)

        readme_text = build_processing.get_readme(new_files)
        readme_override = "FG_README_UPDATE" in os.environ and os.environ["FG_README_UPDATE"] == "FALSE"
        if readme_text and not readme_override:
            item.update_description(driver, urls, readme_text)


if __name__ == "__main__":
    main()

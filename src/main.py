"""Automation to enable uploading a new fantasygrounds mod or ext file to the FG Forge and publishing it to the Live channel"""

import getpass
import logging
import os
from pathlib import Path, PurePath

import requestium
from selenium import webdriver
from dotenv import load_dotenv

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
    file_names = os.environ.get("FG_UL_FILE") or input("Files to include in build (comma-separated and within project folder): ")
    new_files = [build_processing.get_build(PurePath(__file__).parents[1], file) for file in file_names.split(",")]
    user_name = os.environ.get("FG_USER_NAME") or input("FantasyGrounds username: ")
    user_pass = os.environ.get("FG_USER_PASS") or getpass.getpass("FantasyGrounds password: ")
    creds = ForgeCredentials(user_name, user_pass)
    item_id = os.environ.get("FG_ITEM_ID") or input("Forge item ID: ")
    item = ForgeItem(creds, item_id, TIMEOUT_SECONDS)
    urls = ForgeURLs()
    return new_files, item, urls


def main() -> None:
    """Hey, I just met you, and this is crazy, but I'm the main function, so call me maybe."""
    load_dotenv(Path(PurePath(__file__).parents[1], ".env"))
    new_files, item, urls = construct_objects()

    with requestium.Session(driver=webdriver.Chrome(options=configure_headless_chrome())) as s:
        channel = os.environ.get("FG_RELEASE_CHANNEL", ReleaseChannel.LIVE)
        item.upload_and_publish(s, urls, new_files, channel)

        readme_text = build_processing.get_readme(new_files)
        readme_update = bool(os.environ.get("FG_README_UPDATE", "TRUE"))
        if readme_text and readme_update:
            item.update_description(s, urls, readme_text)


if __name__ == "__main__":
    main()

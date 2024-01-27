"""Provides classes for authenticating to and managing items on the FantasyGrounds Forge marketplace"""
import json.decoder
import logging
import time
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup
from requestium import Session
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from drop_file import drag_and_drop_file

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s")


@dataclass(frozen=True)
class ForgeURLs:
    MANAGE_CRAFT = "https://forge.fantasygrounds.com/crafter/manage-craft"
    API_CRAFTER_ITEMS = "https://forge.fantasygrounds.com/api/crafter/items"


@dataclass(frozen=True)
class ForgeCredentials:
    """Dataclass used to store the authentication credentials used on FG Forge"""

    user_id: str
    username: str
    password: str
    password_md5: str

    def get_csrf_token(page_text: str) -> str:
        """Find and return the Cross-Site Request Forgery token from the meta tags of the provided html webpage"""

        soup = BeautifulSoup(page_text, "lxml")
        return soup.select_one("meta[name='csrf-token']")["content"]


@dataclass(frozen=True)
class ReleaseChannel:
    """Constants representing the numeric strings used to represent each release channel"""

    LIVE = "1"
    TEST = "2"
    NONE = "0"


@dataclass(frozen=True)
class ForgeItem:
    """Dataclass used to interact with an item on the FG Forge"""

    creds: ForgeCredentials
    item_id: str

    def open_manage_item_page(self, session: Session):
        session.driver.get(ForgeURLs.MANAGE_CRAFT)
        time.sleep(3)
        if session.driver.find_element(By.ID, "login-form"):
            username_field = session.driver.find_element(By.NAME, "vb_login_username")
            password_field = session.driver.find_element(By.NAME, "vb_login_password")
            username_field.send_keys(self.creds.username)
            password_field.send_keys(self.creds.password)
            password_field.submit()
            time.sleep(6)
        try:
            session.driver.find_element(By.ID, "item-list-content")
        except NoSuchElementException:
            raise Exception("Could not load the Manage Craft page!")

        items_per_page = session.driver.find_element(By.NAME, "items-table_length")
        items_per_page.send_keys("100")
        time.sleep(3)

        # Click appropriate item page
        session.driver.find_element(By.XPATH, f"//a[@data-item-id='{self.item_id}']").click()
        time.sleep(3)

    def upload_item_build(self, session: Session, new_build: Path) -> bool:
        """Uploads a new build to this Forge item, returning True if successful"""

        # Click upload tab
        session.driver.find_element(By.ID, "manage-build-uploads-tab").click()
        time.sleep(3)

        # Drag file into dropzone
        dropzone = session.driver.find_element(By.ID, "build-upload-dropzone")
        drag_and_drop_file(dropzone, new_build)
        time.sleep(6)

        # Check if files are there
        try:
            session.driver.find_element(By.CLASS_NAME, "dz-filename")
        except NoSuchElementException:
            raise Exception("File drag and drop didn't work!")

        # Click dropzone submit button
        session.driver.find_element(By.ID, "submit-build-button").click()
        time.sleep(18)

        # Check if files are gone
        try:
            session.driver.find_element(By.CLASS_NAME, "dz-filename")
            raise Exception("File did not upload correctly!")
        except NoSuchElementException:
            return True

    def get_item_api_url(self) -> str:
        """Constructs the API URL specific to this Forge item"""
        return f"{ForgeURLs.API_CRAFTER_ITEMS}/{self.item_id}"

    def get_item_builds(self, session: Session) -> list[dict[str]]:
        """Retrieves a list of recent builds that have been uploaded to this Forge item"""
        response = session.get(
            ForgeURLs.MANAGE_CRAFT,
        )
        headers = {"X-CSRF-Token": ForgeCredentials.get_csrf_token(response.text)}
        response = session.post(
            f"{self.get_item_api_url()}/builds/data-table",
            headers=headers,
        )
        try:
            logging.debug(response.json())
            return response.json().get("data")
        except json.decoder.JSONDecodeError:
            if response.status_code != 302:
                raise Exception("Authentication Issues! No JSON data returned.", response.url)
            raise Exception("No JSON data returned!", response.url)

    def set_build_channel(self, build_id: str, channel: ReleaseChannel, session: Session) -> bool:
        """Sets the build channel of this Forge item to the specified value, returning True on 200 OK"""
        response = session.get(
            ForgeURLs.MANAGE_CRAFT,
        )
        headers = {"X-CSRF-Token": ForgeCredentials.get_csrf_token(response.text)}
        response = session.post(
            f"{self.get_item_api_url()}/builds/{build_id}/channels/{channel}",
            headers=headers,
        )
        return response.status_code == 200

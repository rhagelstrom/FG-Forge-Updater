"""Provides classes for authenticating to and managing items on the FantasyGrounds Forge marketplace"""
import logging
import time
from dataclasses import dataclass
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from drop_file import drag_and_drop_file

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s")


class ForgeURLs:
    """Contains URL strings for webpages used on the forge"""
    MANAGE_CRAFT: str = "https://forge.fantasygrounds.com/crafter/manage-craft"
    API_CRAFTER_ITEMS: str = "https://forge.fantasygrounds.com/api/crafter/items"


@dataclass(frozen=True)
class ForgeCredentials:
    """Dataclass used to store the authentication credentials used on FG Forge"""

    user_id: str
    username: str
    password: str
    password_md5: str


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

    def open_manage_item_page(self, driver: webdriver, urls: ForgeURLs):
        driver.get(urls.MANAGE_CRAFT)
        time.sleep(3)
        if driver.find_element(By.ID, "login-form"):
            username_field = driver.find_element(By.NAME, "vb_login_username")
            password_field = driver.find_element(By.NAME, "vb_login_password")
            username_field.send_keys(self.creds.username)
            password_field.send_keys(self.creds.password)
            password_field.submit()
            time.sleep(6)
        try:
            driver.find_element(By.ID, "item-list-content")
        except NoSuchElementException:
            raise Exception("Could not load the Manage Craft page!")

        items_per_page = driver.find_element(By.NAME, "items-table_length")
        items_per_page.send_keys("100")
        time.sleep(3)

        # Click appropriate item page
        driver.find_element(By.XPATH, f"//a[@data-item-id='{self.item_id}']").click()
        time.sleep(3)

    @staticmethod
    def upload_item_build(driver: webdriver, new_build: Path) -> bool:
        """Uploads a new build to this Forge item, returning True if successful"""

        # Click upload tab
        driver.find_element(By.ID, "manage-build-uploads-tab").click()
        time.sleep(3)

        # Drag file into dropzone
        dropzone = driver.find_element(By.ID, "build-upload-dropzone")
        drag_and_drop_file(dropzone, new_build)
        time.sleep(6)

        # Check if files are there
        try:
            driver.find_element(By.CLASS_NAME, "dz-filename")
        except NoSuchElementException:
            raise Exception("File drag and drop didn't work!")

        # Click dropzone submit button
        driver.find_element(By.ID, "submit-build-button").click()
        time.sleep(18)

        # Check if files are gone
        try:
            driver.find_element(By.CLASS_NAME, "dz-filename")
            raise Exception("File did not upload correctly!")
        except NoSuchElementException:
            return True

    def get_item_api_url(self) -> str:
        """Constructs the API URL specific to this Forge item"""
        return f"{ForgeURLs.API_CRAFTER_ITEMS}/{self.item_id}"

    def set_build_channel(self, build_id: str, channel: ReleaseChannel, driver: webdriver, urls: ForgeURLs) -> bool:
        """Sets the build channel of this Forge item to the specified value, returning True on 200 OK"""
        driver.get(
            urls.MANAGE_CRAFT,
        )
        csrf_token = driver.find_element(By.XPATH, "//meta[@name='csrf-token']").get_attribute("content")
        headers = {"X-CSRF-Token": csrf_token}

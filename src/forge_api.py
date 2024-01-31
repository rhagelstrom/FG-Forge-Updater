"""Provides classes for authenticating to and managing items on the FantasyGrounds Forge marketplace"""

import logging
import time
from dataclasses import dataclass
from pathlib import Path
from glob import glob

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

logging.basicConfig(level=logging.WARNING, format="%(asctime)s : %(levelname)s : %(message)s")

SPEED_INTERVAL = 2


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
class ForgeItem:
    """Dataclass used to interact with an item on the FG Forge"""

    creds: ForgeCredentials
    item_id: str

    def open_manage_item_page(self, driver: webdriver, urls: ForgeURLs) -> None:
        """Navigate to the manage-craft/ page, login if needed, and set the per-page item count to 100"""
        driver.get(urls.MANAGE_CRAFT)
        time.sleep(SPEED_INTERVAL)
        if driver.find_element(By.ID, "login-form"):
            username_field = driver.find_element(By.NAME, "vb_login_username")
            password_field = driver.find_element(By.NAME, "vb_login_password")
            username_field.send_keys(self.creds.username)
            password_field.send_keys(self.creds.password)
            password_field.submit()
            time.sleep(SPEED_INTERVAL * 3)
        try:
            driver.find_element(By.ID, "item-list-content")
        except NoSuchElementException:
            raise Exception("Could not load the Manage Craft page!")

        items_per_page = driver.find_element(By.NAME, "items-table_length")
        items_per_page.send_keys("100")
        time.sleep(SPEED_INTERVAL)

        # Click appropriate item page
        driver.find_element(By.XPATH, f"//a[@data-item-id='{self.item_id}']").click()
        time.sleep(SPEED_INTERVAL)

    def upload_item_build(self, driver: webdriver, new_build: Path, urls: ForgeURLs) -> None:
        """Uploads a new build to this Forge item, returning True if successful"""

        if not new_build.is_file():
            logging.error("File at %s is not found.", str(new_build))
            print(glob(str(new_build.parent)))

        # Click upload tab
        driver.find_element(By.ID, "manage-build-uploads-tab").click()
        time.sleep(SPEED_INTERVAL)

        dz_inputs = driver.find_elements(By.XPATH, "//input[@type='file' and @class='dz-hidden-input']")
        dz_inputs[1].send_keys(str(new_build))
        time.sleep(SPEED_INTERVAL)

        # Check if files are there
        try:
            driver.find_element(By.CLASS_NAME, "dz-upload")
        except NoSuchElementException:
            raise Exception("File drag and drop didn't work!")

        # Click dropzone submit button
        driver.find_element(By.ID, "submit-build-button").click()
        time.sleep(SPEED_INTERVAL * 2)

        try:
            # raise an exception based on the toast message, if displayed
            driver.find_element(By.XPATH, "//*[@class='toast toast-error']")
            toast_message = driver.find_element(By.CLASS_NAME, "toast-message")
            raise Exception(toast_message.text)
        except NoSuchElementException:
            pass

        try:
            # raise an exception if dropzone shows an error message
            dropzone_error_div = driver.find_element(By.CLASS_NAME, "dz-error-message")
            if dropzone_error_div.value_of_css_property("display") == "block":
                dropzone_error = dropzone_error_div.find_element(By.TAG_NAME, "span")
                raise Exception(dropzone_error.get_attribute("innerHTML"))
        except NoSuchElementException:
            pass

        try:
            # raise an exception if the file is still uploading after sleeping
            upload_progress_bar_width_filled = driver.find_element(By.CLASS_NAME, "dz-upload").value_of_css_property("width").replace("px", "")
            upload_progress_bar_width = driver.find_element(By.CLASS_NAME, "dz-progress").value_of_css_property("width").replace("px", "")
            upload_progress = float(upload_progress_bar_width_filled) / float(upload_progress_bar_width)
            raise Exception("File upload timed out at {:.0f}%".format(upload_progress))
        except NoSuchElementException:
            pass

        # Click back button
        driver.get(urls.MANAGE_CRAFT)
        time.sleep(SPEED_INTERVAL)

        # Click appropriate item page
        driver.find_element(By.XPATH, f"//a[@data-item-id='{self.item_id}']").click()
        time.sleep(SPEED_INTERVAL)

        # Click appropriate item page
        item_builds = driver.find_elements(By.XPATH, "//select[@class='form-control item-build-channel item-build-option']")
        item_builds_latest = Select(item_builds[0])
        item_builds_latest.select_by_visible_text("Live")
        time.sleep(SPEED_INTERVAL)

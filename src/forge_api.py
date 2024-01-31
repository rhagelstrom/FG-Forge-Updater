"""Provides classes for authenticating to and managing items on the FantasyGrounds Forge marketplace"""

import logging
import time
from dataclasses import dataclass
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(level=logging.WARNING, format="%(asctime)s : %(levelname)s : %(message)s")

TIMEOUT = 10


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

        try:
            WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.ID, "login-form")))
            username_field = driver.find_element(By.NAME, "vb_login_username")
            password_field = driver.find_element(By.NAME, "vb_login_password")
            username_field.send_keys(self.creds.username)
            password_field.send_keys(self.creds.password)
            password_field.submit()
        except TimeoutException:
            pass

        try:
            WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.NAME, "items-table_length")))
            items_per_page = Select(driver.find_element(By.NAME, "items-table_length"))
            items_per_page.select_by_visible_text("100")
        except TimeoutException:
            raise Exception("Could not load the Manage Craft page!")

        try:
            WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, f"//a[@data-item-id='{self.item_id}']")))
            item_link = driver.find_element(By.XPATH, f"//a[@data-item-id='{self.item_id}']")
            item_link.click()
        except TimeoutException:
            raise Exception("Could not find item page, is FORGE_ITEM_ID correct?")

    def upload_item_build(self, driver: webdriver, new_build: Path, urls: ForgeURLs) -> None:
        """Uploads a new build to this Forge item, returning True if successful"""

        if not new_build.is_file():
            raise Exception(f"File at {str(new_build)} is not found.")

        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.ID, "manage-build-uploads-tab")))
        uploads_tab = driver.find_element(By.ID, "manage-build-uploads-tab")
        uploads_tab.click()

        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "dz-hidden-input")))
        time.sleep(0.5)
        dz_inputs = driver.find_elements(By.CLASS_NAME, "dz-hidden-input")
        dz_inputs[1].send_keys(str(new_build))

        try:
            WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "dz-upload")))
        except TimeoutException:
            raise Exception("File drag and drop didn't work!")

        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.ID, "submit-build-button")))
        submit_button = driver.find_element(By.ID, "submit-build-button")
        submit_button.click()

        try:
            WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//*[@class='toast toast-error']")))
            toast_error_box = driver.find_element(By.XPATH, "//*[@class='toast toast-error']")
            toast_message = toast_error_box.find_element(By.CLASS_NAME, "toast-message").text
            raise Exception(toast_message)
        except TimeoutException:
            pass

        try:
            WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "dz-error-message")))
            dropzone_error_box = driver.find_element(By.CLASS_NAME, "dz-error-message")
            dropzone_error_box_visible = bool(dropzone_error_box.value_of_css_property("display") == "block")
            if dropzone_error_box_visible:
                dropzone_error_message = dropzone_error_box.find_element(By.TAG_NAME, "span").get_attribute("innerHTML")
                raise Exception(dropzone_error_message)
        except TimeoutException:
            pass

        try:
            upload_progress_bar = driver.find_element(By.CLASS_NAME, "dz-upload")
            upload_progress_bar_width_filled = upload_progress_bar.value_of_css_property("width").replace("px", "")
            upload_progress_bar_width = driver.find_element(By.CLASS_NAME, "dz-progress").value_of_css_property("width").replace("px", "")
            upload_progress = float(upload_progress_bar_width_filled) / float(upload_progress_bar_width)
            raise Exception("File upload timed out at {:.0f}%".format(upload_progress))
        except NoSuchElementException:
            pass

        driver.get(urls.MANAGE_CRAFT)

        try:
            WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, f"//a[@data-item-id='{self.item_id}']")))
            item_link = driver.find_element(By.XPATH, f"//a[@data-item-id='{self.item_id}']")
            item_link.click()
        except TimeoutException:
            raise Exception("Could not find item page, is FORGE_ITEM_ID correct?")

        try:
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, "//select[@class='form-control item-build-channel item-build-option']"))
            )
            item_builds = driver.find_elements(By.XPATH, "//select[@class='form-control item-build-channel item-build-option']")
            item_builds_latest = Select(item_builds[0])
            item_builds_latest.select_by_visible_text("Live")
        except TimeoutException:
            raise Exception("Could not find item page, is FORGE_ITEM_ID correct?")

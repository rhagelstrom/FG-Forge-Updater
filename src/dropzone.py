import time
from dataclasses import dataclass
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@dataclass
class DropzoneErrorHandling:
    driver: webdriver
    timeout: float

    def check_report_toast_error(self):
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, "//*[@class='toast toast-error']")))
            toast_error_box = self.driver.find_element(By.XPATH, "//*[@class='toast toast-error']")
            toast_message = toast_error_box.find_element(By.CLASS_NAME, "toast-message").text
            raise Exception(toast_message)
        except TimeoutException:
            pass

    def check_report_dropzone_upload_error(self):
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "dz-error-message")))
            dropzone_error_box = self.driver.find_element(By.CLASS_NAME, "dz-error-message")
            dropzone_error_box_visible = bool(dropzone_error_box.value_of_css_property("display") == "block")
            if dropzone_error_box_visible:
                dropzone_error_message = dropzone_error_box.find_element(By.TAG_NAME, "span").get_attribute("innerHTML")
                raise Exception(dropzone_error_message)
        except TimeoutException:
            pass

    def check_report_upload_percentage(self):
        try:
            upload_progress_bar = self.driver.find_element(By.CLASS_NAME, "dz-upload")
            upload_progress_bar_width_filled = upload_progress_bar.value_of_css_property("width").replace("px", "")
            upload_progress_bar_width = self.driver.find_element(By.CLASS_NAME, "dz-progress").value_of_css_property("width").replace("px", "")
            upload_progress = float(upload_progress_bar_width_filled) / float(upload_progress_bar_width)
            raise Exception("File upload timed out at {:.0f}%".format(upload_progress))
        except NoSuchElementException:
            pass


def drag_build_to_dropzone(driver: webdriver, timeout: float, new_build: Path) -> None:
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='manage-build-uploads-tab']")))
    uploads_tab = driver.find_element(By.XPATH, "//a[@id='manage-build-uploads-tab']")
    uploads_tab.click()

    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "dz-hidden-input")))
    time.sleep(0.5)
    dz_inputs = driver.find_elements(By.CLASS_NAME, "dz-hidden-input")
    dz_inputs[1].send_keys(str(new_build))

    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "dz-upload")))
    except TimeoutException:
        raise Exception("File drag and drop didn't work!")

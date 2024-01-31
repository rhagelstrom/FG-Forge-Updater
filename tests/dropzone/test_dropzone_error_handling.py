from unittest.mock import Mock

import pytest
from selenium.webdriver.common.by import By

from src.dropzone import DropzoneErrorHandling, DropzoneException, LongUploadException, ToastErrorException


def test_check_report_toast_error() -> None:
    def find_element(by, value) -> Mock:
        if by == By.XPATH and value == "//*[@class='toast toast-error']":
            element = Mock()
            element.find_element.return_value.text = "Never send a boy to do a woman's job."
            return element

    mock_driver = Mock()
    mock_driver.find_element = find_element

    with pytest.raises(ToastErrorException):
        error_handling = DropzoneErrorHandling(mock_driver)
        error_handling.check_report_toast_error()


def test_check_report_dropzone_upload_error() -> None:
    def find_element(by, value) -> Mock:
        if by == By.CLASS_NAME and value == "dz-error-message":
            element = Mock()
            element.value_of_css_property.return_value = "block"
            return element
        if by == By.TAG_NAME and value == "span":
            element = Mock()
            element.get_attribute.return_value = "We have no names, man. No names. We are nameless!"
            return element

    mock_driver = Mock()
    mock_driver.find_element = find_element

    with pytest.raises(DropzoneException):
        error_handling = DropzoneErrorHandling(mock_driver)
        error_handling.check_report_dropzone_upload_error()


def test_check_report_upload_percentage() -> None:
    def find_element(by, value) -> Mock:
        if by == By.CLASS_NAME and value == "dz-upload":
            element = Mock()
            element.value_of_css_property.return_value = "55px"
            return element
        if by == By.CLASS_NAME and value == "dz-progress":
            element = Mock()
            element.value_of_css_property.return_value = "80px"
            return element

    mock_driver = Mock()
    mock_driver.find_element = find_element

    with pytest.raises(LongUploadException):
        error_handling = DropzoneErrorHandling(mock_driver)
        error_handling.check_report_upload_percentage()

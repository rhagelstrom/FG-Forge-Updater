from pathlib import Path
from unittest.mock import MagicMock, call

import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.dropzone import add_file_to_dropzone

TEST_ELEMENTS = [
    (By.XPATH, "//a[@id='manage-build-uploads-tab']"),
    (By.CLASS_NAME, "dz-hidden-input"),
    (By.CLASS_NAME, "dz-upload"),
]


def find_element(by: str, value: str, elements: list[tuple[str, str]]) -> MagicMock:
    """Construct the WebElement mock object if matching any definition in elements"""
    if (by, value) in elements:
        element = MagicMock(spec=WebElement)
        element.click.return_value = None
        element.is_enabled.return_value = True
        element.is_displayed.return_value = True
        element.send_keys.return_value = None
        element.find_elements.return_value = [element, element]
        return element


def find_element_all(by: str, value: str) -> MagicMock:
    """Construct the WebElement mock object if matching any definition in TEST_ELEMENTS"""
    return find_element(by, value, TEST_ELEMENTS)


def find_element_unsuccessful(by: str, value: str) -> MagicMock:
    """Construct the WebElement mock object, but only if matching the first two definitions in TEST_ELEMENTS"""
    return find_element(by, value, [TEST_ELEMENTS[0], TEST_ELEMENTS[1]])


def find_elements(by, value) -> list[MagicMock]:
    """Construct a list of two of the requested mock element"""
    return [find_element_all(by, value), find_element_all(by, value)]


def test_add_file_to_dropzone() -> None:
    """Ensure that adding files to dropzones searches for the right elements"""

    mock_driver = MagicMock(spec=webdriver.Chrome)
    mock_driver.find_element.side_effect = find_element_all
    mock_driver.find_elements.side_effect = find_elements

    add_file_to_dropzone(mock_driver, 2, Path(__file__))

    expected_find_element = [
        call(By.XPATH, "//a[@id='manage-build-uploads-tab']"),
        call(By.CLASS_NAME, "dz-hidden-input"),
        call(By.CLASS_NAME, "dz-upload"),
    ]
    assert mock_driver.find_element.mock_calls == expected_find_element
    mock_driver.find_elements.assert_called_once_with(By.CLASS_NAME, "dz-hidden-input")


def test_add_file_to_dropzone_timeout() -> None:
    """Ensure that exception is thrown if file is not found in dropzone after adding"""

    mock_driver = MagicMock(spec=webdriver.Chrome)
    mock_driver.find_element.side_effect = find_element_unsuccessful
    mock_driver.find_elements.side_effect = find_elements

    with pytest.raises(TimeoutException):
        add_file_to_dropzone(mock_driver, 2, Path(__file__))

    expected_find_element = [
        call(By.XPATH, "//a[@id='manage-build-uploads-tab']"),
        call(By.CLASS_NAME, "dz-hidden-input"),
        call(By.CLASS_NAME, "dz-upload"),
        call(By.CLASS_NAME, "dz-upload"),
        call(By.CLASS_NAME, "dz-upload"),
        call(By.CLASS_NAME, "dz-upload"),
    ]
    assert mock_driver.find_element.mock_calls == expected_find_element
    mock_driver.find_elements.assert_called_once_with(By.CLASS_NAME, "dz-hidden-input")

from dataclasses import FrozenInstanceError

import pytest
from polyfactory.factories import DataclassFactory

from src.forge_api import ForgeCredentials, ForgeItem


class ForgeCredentialsFactory(DataclassFactory[ForgeCredentials]):
    """Represents a ForgeCredentials object for the purposes of testing ForgeItem objects"""
    __model__ = ForgeCredentials


def test_forge_item_creation() -> None:
    """Ensures that provided item id and timeout limit are found in the ForgeItems object and that attempts at modifying values are not allowed"""
    item_string = "33"
    timeout_string = float(3.14159)

    creds = ForgeCredentialsFactory.build()
    item = ForgeItem(creds, item_string, timeout_string)

    assert item.creds == creds
    assert item.item_id == item_string
    assert item.timeout == timeout_string
    with pytest.raises(FrozenInstanceError):
        item.item_id = "7"

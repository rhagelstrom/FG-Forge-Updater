import pytest
from dataclasses import FrozenInstanceError

from src.forge_api import ForgeCredentials


def test_forge_credentials_creation() -> None:
    creds = ForgeCredentials("doug", "i_Love md5!")
    assert creds.username == "doug"
    assert creds.password == "i_Love md5!"
    with pytest.raises(FrozenInstanceError):
        creds.password = "new_password"

"""Provides classes for authenticating to and managing items on the FantasyGrounds Forge marketplace"""

import logging
from dataclasses import dataclass
from pathlib import Path

from requests import Session

FORGE_URL = "https://forge.fantasygrounds.com"
API_URL_BASE = f"{FORGE_URL}/api"

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s")


class ReleaseChannel:
    """Constants representing the numeric strings used to represent each release channel"""

    LIVE = "1"
    TEST = "2"
    NONE = "0"


@dataclass(frozen=True)
class ForgeCredentials:
    """Dataclass used to store the authentication credentials used on FG Forge"""

    user_id: str
    password: str
    csrf_token: str
    php_session_id: str


@dataclass(frozen=True)
class ForgeItem:
    """Dataclass used to interact with an item on the FG Forge"""

    creds: ForgeCredentials
    item_id: str

    def get_item_api_url(self) -> str:
        """Constructs the API URL specific to this Forge item"""
        return f"{API_URL_BASE}/crafter/items/{self.item_id}"

    def get_item_data(self, session: Session) -> dict[str]:
        """Retrieves item data for this Forge item, such as title, description, posting date, etc"""
        response = session.get(
            self.get_item_api_url(),
        )
        session.cookies.set("bb_sessionhash", response.cookies["bb_sessionhash"], path="/", domain=".fantasygrounds.com")
        return response.json()

    def get_item_builds(self, session: Session) -> list[dict[str]]:
        """Retrieves a list of recent builds that have been uploaded to this Forge item"""
        headers = {
            "X-CSRF-Token": self.creds.csrf_token,
        }
        response = session.post(
            f"{self.get_item_api_url()}/builds/data-table",
            headers=headers,
        )
        session.cookies.set("bb_sessionhash", response.cookies["bb_sessionhash"], path="/", domain=".fantasygrounds.com")
        return response.json().get("data")

    def upload_item_build(self, new_build: Path, session: Session) -> bool:
        """Uploads a new build to this Forge item, returning True on 200 OK"""
        headers = {
            "X-CSRF-Token": self.creds.csrf_token,
        }
        upload_files = {"buildFiles[0]": (new_build.name, new_build.read_bytes(), "application/vnd.novadigm.EXT")}
        response = session.post(
            f"{self.get_item_api_url()}/builds/upload",
            headers=headers,
            files=upload_files,
        )
        session.cookies.set("bb_sessionhash", response.cookies["bb_sessionhash"], path="/", domain=".fantasygrounds.com")
        logging.debug(response.request.body)
        return response.status_code == 200

    def set_build_channel(self, build_id: str, channel: ReleaseChannel, session: Session) -> bool:
        """Sets the build channel of this Forge item to the specified value, returning True on 200 OK"""
        headers = {
            "X-CSRF-Token": self.creds.csrf_token,
        }
        response = session.post(
            f"{self.get_item_api_url()}/builds/{build_id}/channels/{channel}",
            headers=headers,
        )
        session.cookies.set("bb_sessionhash", response.cookies["bb_sessionhash"], path="/", domain=".fantasygrounds.com")
        return response.status_code == 200

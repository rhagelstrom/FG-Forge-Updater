import logging
from dataclasses import dataclass
from pathlib import Path

from requests import Session

FORGE_URL = "https://forge.fantasygrounds.com"
API_URL_BASE = f"{FORGE_URL}/api"

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s")


class ReleaseChannel:
    LIVE = "1"
    TEST = "2"
    NONE = "0"


@dataclass(frozen=True)
class Credentials:
    user_id: str
    password: str


@dataclass(frozen=True)
class ForgeCredentials(Credentials):
    csrf_token: str
    php_session_id: str

    def get_auth_cookies(self, session: Session) -> str:
        return f"PHPSESSID={self.php_session_id}; bb_userid={self.user_id}; bb_password={self.password}"

    def get_csrf_token(self, session: Session) -> str:
        return self.csrf_token


@dataclass(frozen=True)
class ForgeCrafter:
    creds: ForgeCredentials
    crafter_id: str

    def get_creator_items(self, session: Session) -> dict[str]:
        response = session.get(
            f"{API_URL_BASE}/crafter/items/{self.crafter_id}",
            headers={"Cookie": self.creds.get_auth_cookies(session)},
        )
        return response.json()


@dataclass(frozen=True)
class ForgeItem:
    creds: ForgeCredentials
    item_id: str

    def get_item_api_url(self) -> str:
        return f"{API_URL_BASE}/crafter/items/{self.item_id}"

    def get_item_data(self, session: Session) -> dict[str]:
        response = session.get(
            self.get_item_api_url(),
            headers={"Cookie": self.creds.get_auth_cookies(session)},
        )
        return response.json()

    def get_item_builds(self, session: Session) -> list[dict[str]]:
        headers = {
            "X-CSRF-Token": self.creds.get_csrf_token(session),
            "Cookie": self.creds.get_auth_cookies(session),
        }
        response = session.post(
            f"{self.get_item_api_url()}/builds/data-table",
            headers=headers,
        )
        return response.json().get("data")

    def upload_item_build(self, new_build: Path, session: Session) -> bool:
        headers = {
            "X-CSRF-Token": self.creds.get_csrf_token(session),
            "Cookie": self.creds.get_auth_cookies(session),
        }
        upload_files = {"buildFiles": (new_build.name, new_build.read_bytes(), "application/vnd.novadigm.EXT")}
        response = session.post(
            f"{self.get_item_api_url()}/builds/upload",
            headers=headers,
            files=upload_files,
        )
        return response.status_code == 200

    def set_build_channel(self, build_id: str, channel: ReleaseChannel, session: Session) -> bool:
        headers = {
            "X-CSRF-Token": self.creds.get_csrf_token(session),
            "Cookie": self.creds.get_auth_cookies(session),
        }
        response = session.post(
            f"{self.get_item_api_url()}/builds/{build_id}/channels/{channel}",
            headers=headers,
        )
        return response.status_code == 200

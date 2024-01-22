from dataclasses import dataclass

from bs4 import BeautifulSoup
from requests import Session

FORGE_URL = "https://forge.fantasygrounds.com"
API_URL_BASE = f"{FORGE_URL}/api"


@dataclass(frozen=True)
class Credentials:
    user_id: str
    password: str


@dataclass(frozen=True)
class ForgeCredentials(Credentials):
    session: Session

    def get_auth_cookie(self) -> str:
        return f"bb_userid={self.user_id}; bb_password={self.password}"

    def get_php_session_id(self) -> str:
        r = self.session.post(f"{FORGE_URL}/crafter/manage-craft", data={})
        return f"PHPSESSID={r.cookies['PHPSESSID']}"

    def get_csrf_token(self) -> str:
        response = self.session.get(
            f"{FORGE_URL}/crafter/manage-craft",
            headers={"Cookie": self.get_auth_cookie()},
        )
        soup = BeautifulSoup(response.content, "html5lib")
        return soup.find(attrs={"name": "csrf-token"}).get("content")


@dataclass(frozen=True)
class ForgeCrafter:
    creds: ForgeCredentials
    crafter_id: str
    session: Session
    CRAFTER_API_URL = f"{API_URL_BASE}/crafter"

    def get_creator_items(self) -> dict:
        return self.session.get(
            f"{self.CRAFTER_API_URL}/items/{self.crafter_id}",
            headers={"Cookie": self.creds.get_auth_cookie()},
        ).json()


@dataclass(frozen=True)
class ForgeItem:
    creds: ForgeCredentials
    item_id: str
    session: Session
    LIVE_CHANNEL = "1"
    TEST_CHANNEL = "2"

    def get_item_api_url(self) -> str:
        return f"{API_URL_BASE}/crafter/items/{self.item_id}"

    def get_item_data(self) -> dict:
        return self.session.get(
            self.get_item_api_url(),
            headers={"Cookie": self.creds.get_auth_cookie()},
        ).json()

    def get_item_builds(self) -> dict:
        return self.session.get(
            f"{self.get_item_api_url()}/builds/data-table",
            headers={"Cookie": self.creds.get_auth_cookie()},
        ).json()

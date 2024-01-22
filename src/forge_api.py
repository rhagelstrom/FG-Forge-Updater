from dataclasses import dataclass

from requests import Session
from bs4 import BeautifulSoup

FORGE_URL = "https://forge.fantasygrounds.com"
API_URL_BASE = f"{FORGE_URL}/api"


@dataclass(frozen=True)
class Credentials:
    user_id: str
    password: str


@dataclass(frozen=True)
class ForgeCredentials(Credentials):
    session: Session

    def get_auth_cookie(self):
        return f"bb_userid={self.user_id}; bb_password={self.password}"

    def get_csrf_token(self):
        response = self.session.get(
            f"{FORGE_URL}/crafter/manage-craft",
            headers={"Cookie": self.get_auth_cookie()},
        )
        soup = BeautifulSoup(response.content, "html5lib")
        return soup.find(attrs={"name": "csrf-token"}).get("content")


@dataclass(frozen=True)
class ForgeCrafter:
    session: Session
    creds: ForgeCredentials
    crafter_id: str
    CRAFTER_API_URL = f"{API_URL_BASE}/crafter"

    def get_creator_items(self):
        return self.session.get(
            f"{self.CRAFTER_API_URL}/items/{self.crafter_id}",
            headers={"Cookie": self.creds.get_auth_cookie()},
        ).json()


@dataclass(frozen=True)
class ForgeItem:
    session: Session
    creds: ForgeCredentials
    item_id: str
    LIVE_CHANNEL = "1"
    TEST_CHANNEL = "2"

    def get_item_api_url(self):
        return f"{API_URL_BASE}/crafter/items/{self.item_id}"

    def get_item_data(self):
        return self.session.get(
            self.get_item_api_url(),
            headers={"Cookie": self.creds.get_auth_cookie()},
        ).json()

    def get_item_builds(self):
        return self.session.get(
            f"{self.get_item_api_url()}/builds/data-table",
            headers={"Cookie": self.creds.get_auth_cookie()},
        ).json()

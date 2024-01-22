from dataclasses import dataclass

from requests import Session

FORGE_URL = "https://forge.fantasygrounds.com"
API_URL_BASE = f"{FORGE_URL}/api"


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
        return session.get(
            f"{API_URL_BASE}/crafter/items/{self.crafter_id}",
            headers={"Cookie": self.creds.get_auth_cookies(session)},
        ).json()


@dataclass(frozen=True)
class ForgeItem:
    creds: ForgeCredentials
    item_id: str

    def get_item_api_url(self) -> str:
        return f"{API_URL_BASE}/crafter/items/{self.item_id}"

    def get_item_data(self, session: Session) -> dict[str]:
        return session.get(
            self.get_item_api_url(),
            headers={"Cookie": self.creds.get_auth_cookies(session)},
        ).json()

    def get_item_builds(self, session: Session) -> list[dict[str]]:
        headers = {
            "X-CSRF-Token": self.creds.get_csrf_token(session),
            "Cookie": self.creds.get_auth_cookies(session),
        }
        return (
            session.post(
                f"{self.get_item_api_url()}/builds/data-table",
                headers=headers,
            )
            .json()
            .get("data")
        )

    def upload_item_build(self, new_build, session: Session) -> bool:
        headers = {
            "X-CSRF-Token": self.creds.get_csrf_token(session),
            "Cookie": self.creds.get_auth_cookies(session),
        }
        response = session.post(
            f"{self.get_item_api_url()}/builds/upload",
            headers=headers,
            files=({"buildFiles": (None, new_build)}),
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

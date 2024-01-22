from pathlib import Path, PurePath

from dotenv import dotenv_values
from requests import Session

from src.forge_api import ForgeItem, ForgeCredentials, ReleaseChannel


def main() -> None:
    config = dotenv_values(Path(PurePath(__file__).parents[1], ".env"))
    with Session() as s:
        creds = ForgeCredentials(config.get("bb_userid"), config.get("bb_password"), config.get("csrf_token"), config.get("php_session_id"))
        item = ForgeItem(creds, config.get("forge_item"))
        item_builds = item.get_item_builds(s)  # get all builds for this item
        item_builds.sort(key=lambda k: k["build_num"], reverse=True)  # sort newest first
        item.set_build_channel(item_builds[0]["id"], ReleaseChannel.LIVE, s)  # assign newest build to live channel


if __name__ == "__main__":
    main()

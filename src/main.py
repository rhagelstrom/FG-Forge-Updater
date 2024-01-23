import logging
from pathlib import Path, PurePath

import requests
from dotenv import dotenv_values

from src.forge_api import ForgeItem, ForgeCredentials, ReleaseChannel

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s")


def main() -> None:
    config = dotenv_values(Path(PurePath(__file__).parents[1], ".env"))
    with requests.Session() as s:
        # TODO: Add functionality to automatically obtain php_session_id
        creds = ForgeCredentials(config.get("bb_userid"), config.get("bb_password"), config.get("php_session_id"), s)

        s.cookies.update(requests.utils.cookiejar_from_dict({"PHPSESSID": creds.php_session_id, "bb_userid": creds.user_id, "bb_password": creds.password}))

        item = ForgeItem(creds, config.get("forge_item"))

        # item.upload_item_build(Path(PurePath(__file__).parents[1], config.get("upload_file")), s)

        item_builds = item.get_item_builds(s)  # get all builds for this item
        if item_builds:
            item_builds.sort(key=lambda k: k["build_num"], reverse=True)  # sort newest first
            item.set_build_channel(item_builds[0]["id"], ReleaseChannel.LIVE, s)  # assign newest build to live channel
            logging.debug(item_builds)


if __name__ == "__main__":
    main()

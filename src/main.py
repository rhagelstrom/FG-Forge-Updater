from pathlib import Path, PurePath

import requests
from dotenv import dotenv_values

from src.forge_api import ForgeItem, ForgeCredentials, ReleaseChannel


def main() -> None:
    config = dotenv_values(Path(PurePath(__file__).parents[1], ".env"))
    with requests.Session() as s:
        # TODO: Add functionality to automatically obtain csrf_token and php_session_id by logging in with user/pass
        creds = ForgeCredentials(config.get("bb_userid"), config.get("bb_password"), config.get("csrf_token"), config.get("php_session_id"))
        cookies = requests.utils.cookiejar_from_dict({"PHPSESSID": creds.php_session_id, "bb_userid": creds.user_id, "bb_password": creds.password})
        s.cookies.update(cookies)
        item = ForgeItem(creds, config.get("forge_item"))
        item.upload_item_build(Path(PurePath(__file__).parents[1], config.get("upload_file")), s)
        item_builds = item.get_item_builds(s)  # get all builds for this item
        item_builds.sort(key=lambda k: k["build_num"], reverse=True)  # sort newest first
        item.set_build_channel(item_builds[0]["id"], ReleaseChannel.LIVE, s)  # assign newest build to live channel


if __name__ == "__main__":
    main()

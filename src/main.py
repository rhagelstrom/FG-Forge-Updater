import hashlib
import logging
from pathlib import Path, PurePath

from dotenv import dotenv_values
from requestium import Session
from selenium import webdriver

from forge_api import ForgeItem, ForgeCredentials, ReleaseChannel

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s")


def upload_make_live(session: Session, item: ForgeItem, new_file: Path) -> None:
    item.open_manage_item_page(session)
    # item.upload_item_build(session, new_file)

    item_builds = item.get_item_builds(session)  # get all builds for this item
    # if not item_builds:
    #    Exception("No builds found for item")
    #
    #    item_builds.sort(key=lambda k: k["build_num"], reverse=True)  # sort newest first
    #    item.set_build_channel(item_builds[0]["id"], ReleaseChannel.LIVE, session)  # assign newest build to live channel


def main() -> None:
    config = dotenv_values(Path(PurePath(__file__).parents[1], ".env"))
    pass_md5 = hashlib.md5(config.get("password").encode("utf-8")).hexdigest()
    creds = ForgeCredentials(config.get("user_id"), config.get("username"), config.get("password"), pass_md5)

    item = ForgeItem(creds, config.get("item_id"))

    with Session(driver=webdriver.Chrome(), headless=True) as session:
        session.copy_user_agent_from_driver()
        session.cookies.set(name="bb_userid", value=creds.user_id, domain=".fantasygrounds.com")
        session.cookies.set(name="bb_password", value=creds.password_md5, domain=".fantasygrounds.com")

        new_file = Path(PurePath(__file__).parents[1], config.get("upload_file"))
        logging.debug("File upload path determined to be: %s", new_file)
        upload_make_live(session, item, new_file)


if __name__ == "__main__":
    main()

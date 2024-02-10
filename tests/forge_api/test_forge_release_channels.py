from src.forge_api import ReleaseChannel


def test_forge_urls() -> None:
    """Ensure set values in ForgeURLs have not been changed"""
    assert ReleaseChannel.LIVE.value == "1"
    assert ReleaseChannel.TEST.value == "2"
    assert ReleaseChannel.NONE.value == "0"

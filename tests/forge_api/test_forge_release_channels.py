from src.forge_api import ForgeReleaseChannel


def test_forge_urls() -> None:
    """Ensure set values in ForgeURLs have not been changed."""
    assert ForgeReleaseChannel.LIVE.value == "1"
    assert ForgeReleaseChannel.TEST.value == "2"
    assert ForgeReleaseChannel.NONE.value == "0"

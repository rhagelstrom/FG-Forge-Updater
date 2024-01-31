from pathlib import Path, PurePath

import pytest

from src.main import get_build_file


def test_get_build_file() -> None:
    assert isinstance(get_build_file(PurePath(__file__).parent, PurePath(__file__).name), Path)


def test_get_build_file_path_is_not_folder() -> None:
    with pytest.raises(Exception):
        get_build_file(PurePath(__file__), PurePath(__file__).name)


def test_get_build_file_does_not_exist() -> None:
    with pytest.raises(Exception):
        get_build_file(PurePath(__file__).parents[1], "file-does-not-exist")

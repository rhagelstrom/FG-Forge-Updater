import os
from pathlib import Path

from src.build_processing import get_readme


def test_readme_html() -> None:
    """Ensure that markdown text is being converted to html."""
    with open(os.path.join(os.path.dirname(__file__), "markdown_example/markdown.html"), encoding="utf-8") as file:
        html = file.read()
    zip_path = Path(os.path.join(os.path.dirname(__file__), 'markdown_example/markdown.zip'))
    assert f"{get_readme([zip_path])}\n" == html

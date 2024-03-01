import itertools
import logging
import re
from pathlib import Path, PurePath
from zipfile import ZipFile

import mdformat
from bs4 import BeautifulSoup
from markdown import markdown

README = "README.md"


def apply_styles_to_table(soup: str) -> str:
    """Style tables for better legibility"""
    colors = itertools.cycle(["#FFFFFF", "#E6E6E6"])
    for html_table in soup.find_all("table"):
        for col in html_table.find_all("td"):
            col["style"] = "border:1px solid #000; padding:0.5em;"
        for row in html_table.find_all("tr"):
            row["style"] = f"background-color: {next(colors)}; border:1px solid #000;"
    return soup


def replace_images_with_link(soup: str, no_images: bool) -> str:
    """Replace all images with boilerplate text"""
    for img in soup.find_all("img"):
        new_tag = soup.new_tag("a", href=img["src"])
        new_tag.string = "" if no_images else img.get("alt", "[IMG]")
        img.replace_with(new_tag)
    return soup


def readme_html(readme: ZipFile, no_images: bool = False) -> str:
    """returns an html-formatted string"""
    markdown_text = readme.read(README).decode("UTF-8")
    markdown_text = re.sub(r"!\[]\(\..+?\)", "", markdown_text)
    markdown_text = mdformat.text(markdown_text)
    html = markdown(markdown_text, extensions=["extra", "nl2br", "smarty"])
    html = BeautifulSoup(html, "html.parser")
    html = replace_images_with_link(html, no_images)
    html = apply_styles_to_table(html)
    return str(html)


def get_readme(new_files: list[Path], no_images: bool = False) -> str:
    """Parses the first README.md found in the new files and returns an html-formatted string"""
    return next((readme_html(ZipFile(file), no_images) for file in new_files if README in ZipFile(file).namelist()), "")


def get_build(file_path: PurePath, env_file: str) -> Path:
    """Combines PurePath and file name into a Path object, ensure that a file exists there, and returns the Path"""
    new_file = Path(file_path, env_file)
    logging.info("File upload path determined to be: %s", new_file)
    if not new_file.is_file():
        raise FileNotFoundError(f"File at {str(new_file)} is not found.")
    return new_file

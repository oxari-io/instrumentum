import os
import pytest
from pathlib import Path

from jinja2 import Template

from requests import HTTPError


from dotenv import load_dotenv

from oxari.pdf import (
    download_pdf,
    _download_template,
)  # import python module

load_dotenv()

STORAGETYPE = "STANDARD"
DO_SPACE = os.getenv("DO_SPACE")
DO_REGION = os.getenv("DO_REGION")
DO_KEY = os.getenv("DO_SPACE_ACCESS_KEY")
DO_SECRET = os.getenv("DO_SPACE_SECRET_KEY")

ROOT = Path(__file__).parent.as_posix()


def test_download_template():
    resp = _download_template(file_name="./template.html", root=ROOT)
    assert type(resp) == Template
    

# def test_download_pdf():
#     resp = download_pdf(user_id="uuuid88", order_id="42", space_path=)



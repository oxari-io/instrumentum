import os
import io
from dotenv import load_dotenv
import pytest
from pathlib import Path

from jinja2 import Template

from requests import HTTPError



from oxari.pdf import (
    _create_key_name,
    _save_pdf_locally,
    download_pdf,
    _download_template,
    _fill_pdf,
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

def test_create_key_name():
    resp = _create_key_name(user_id="uuuid8", order_id="1234567890123456789012345678901", space_path=None)
    assert isinstance(resp, str)

def test_fill_pdf():
    template_resp = _download_template(file_name="./template.html", root=ROOT)
    result = _fill_pdf(template_resp, {"user_id" : "uuuid8", "order_id" : "1234567890123456789012345678901"})
    assert isinstance(result, io.BytesIO)

def test_save_pdf_locally():
    resp = _save_pdf_locally(binary_data='Hello World'.encode(), user_id = "uuuid8" , order_id = "1234567890123456789012345678901")

    assert resp.get("file") is not None



    


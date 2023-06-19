"""
The tests are executed in order.

- putting file
- check for it
- get its content
- remove it
- check for it again and fail
"""
import os
import pytest

from requests import HTTPError


from dotenv import load_dotenv

from oxari.digitalocean import (
    check_object,
    get_object,
    put_object,
    delete_object,
)  # import python module

load_dotenv()

STORAGETYPE = "STANDARD"
DO_SPACE = os.getenv("DO_SPACE")
DO_REGION = os.getenv("DO_REGION")
DO_KEY = os.getenv("DO_SPACE_ACCESS_KEY")
DO_SECRET = os.getenv("DO_SPACE_SECRET_KEY")

TEST_FILE_NAME = "test.txt"


@pytest.mark.order(1)
def test_put_object():
    # open file in binary
    with open(f"tests/{TEST_FILE_NAME}", "rb") as file:
        binary_data = file.read()
    resp = put_object(
        file_name=TEST_FILE_NAME,
        binary_data=binary_data,
        do_secret=DO_SECRET,
        do_key=DO_KEY,
        do_space=DO_SPACE,
        do_region=DO_REGION,
    )
    assert resp.status_code == 200


@pytest.mark.order(2)
def test_check_object():
    resp = check_object(
        file_name=TEST_FILE_NAME,
        do_secret=DO_SECRET,
        do_key=DO_KEY,
        do_space=DO_SPACE,
        do_region=DO_REGION,
    )
    file_location = resp.get("file")
    assert file_location is not None


@pytest.mark.order(3)
def test_get_object():
    resp_cont, resp_headers = get_object(
        file_name=TEST_FILE_NAME,
        do_secret=DO_SECRET,
        do_key=DO_KEY,
        do_space=DO_SPACE,
        do_region=DO_REGION,
    )
    assert type(resp_headers) == dict
    assert type(resp_cont) == bytes


@pytest.mark.order(4)
def test_delete_object():
    resp = delete_object(
        file_name=TEST_FILE_NAME,
        do_secret=DO_SECRET,
        do_key=DO_KEY,
        do_space=DO_SPACE,
        do_region=DO_REGION,
    )
    assert resp.status_code == 204


@pytest.mark.order(5)
def test_check_object_after():
    with pytest.raises(HTTPError) as exc_info:
        resp = check_object(
            file_name=TEST_FILE_NAME,
            do_secret=DO_SECRET,
            do_key=DO_KEY,
            do_space=DO_SPACE,
            do_region=DO_REGION,
        )
    assert exc_info.value.response.status_code == 404

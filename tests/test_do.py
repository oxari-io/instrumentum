import os

from dotenv import load_dotenv

from oxari.digitalocean import check_object, get_object, put_object  # import python module

load_dotenv()

STORAGETYPE = "STANDARD"
DO_SPACE = os.getenv("DO_SPACE")
DO_REGION = os.getenv("DO_REGION")
DO_KEY = os.getenv("DO_SPACE_ACCESS_KEY")
DO_SECRET = os.getenv("DO_SPACE_SECRET_KEY")


def test_put_object():
    # open file in binary
    with open("tests/test.txt", 'rb') as file:
        binary_data = file.read()
    resp = put_object(do_storage_type=STORAGETYPE,file_name = "test.txt", binary_data=binary_data, do_secret=DO_SECRET, do_key=DO_KEY, do_space=DO_SPACE, do_region=DO_REGION)
    assert resp.status_code == 200

# def test_check_object():
#     pass

# def test_get_object():
#     pass


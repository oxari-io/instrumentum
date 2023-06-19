from datetime import datetime, timedelta, date

from dotenv import load_dotenv
import hashlib
from datetime import datetime
import requests
from loguru import logger
from aws_requests_auth.aws_auth import AWSRequestsAuth

load_dotenv()


def _get_date_string():
    now = datetime.utcnow()
    year_month_day_format = '%Y-%m-%d'
    date = now.strftime(year_month_day_format)
    return date


def _construct_do_url(file_name, do_space, do_region):
    divider = "" if file_name[0] == "/" else "/"
    url = f'https://{do_space}.{do_region}.digitaloceanspaces.com{divider}{file_name}'
    return url


def put_object(binary_data, file_name, do_space, do_region, do_key, do_secret, content_type="application/octet-stream"):
    do_storage_type = "STANDARD"
    headers = {
        "Content-Type": content_type,
        "x-amz-storage-class": do_storage_type,
        "x-amz-acl": "private",
    }

    auth = AWSRequestsAuth(aws_access_key=do_key,
                           aws_secret_access_key=do_secret,
                           aws_host=f'{do_space}.{do_region}.digitaloceanspaces.com',
                           aws_region=do_region,
                           aws_service='s3')

    url = _construct_do_url(file_name, do_space, do_region)
    response = requests.put(url, data=binary_data, headers=headers, auth=auth)

    if response.status_code != 200:
        response.raise_for_status()

    return response


def check_object(file_name, do_space, do_region, do_key, do_secret):
    auth = AWSRequestsAuth(aws_access_key=do_key,
                           aws_secret_access_key=do_secret,
                           aws_host=f'{do_space}.{do_region}.digitaloceanspaces.com',
                           aws_region=do_region,
                           aws_service='s3')

    url = _construct_do_url(file_name, do_space, do_region)
    response = requests.head(url, auth=auth)

    if response.status_code != 200:
        response.raise_for_status()
    content_size = response.headers.get('content-length')
    content_type = response.headers.get('content-type')
    return {"file": response.url, "file_size": int(content_size), "file_type": content_type}


def get_object(file_name, do_space, do_region, do_key, do_secret):
    # Prepare the headers
    date = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    empty_payload_hash = hashlib.sha256(b'').hexdigest()
    headers = {
        "x-amz-content-sha256": empty_payload_hash,
        "x-amz-date": date,
    }

    # Prepare the AWSRequestsAuth object
    auth = AWSRequestsAuth(
        aws_access_key=do_key,
        aws_secret_access_key=do_secret,
        aws_host=f"{do_space}.{do_region}.digitaloceanspaces.com",
        aws_region=do_region,
        aws_service="s3",
    )

    # Send the GET request
    url = _construct_do_url(file_name, do_space, do_region)

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        response.raise_for_status()

    return response.content, dict(response.headers)


def delete_object(file_name, do_space, do_region, do_key, do_secret):
    # Prepare the headers
    date = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    empty_payload_hash = hashlib.sha256(b'').hexdigest()
    headers = {
        "x-amz-content-sha256": empty_payload_hash,
        "x-amz-date": date,
    }

    # Prepare the AWSRequestsAuth object
    auth = AWSRequestsAuth(
        aws_access_key=do_key,
        aws_secret_access_key=do_secret,
        aws_host=f"{do_space}.{do_region}.digitaloceanspaces.com",
        aws_region=do_region,
        aws_service="s3",
    )

    # Send the GET request
    url = _construct_do_url(file_name, do_space, do_region)
    response = requests.delete(url, headers=headers, auth=auth)

    if response.status_code != 204:
        response.raise_for_status()

    return response

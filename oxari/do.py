
from datetime import datetime, timedelta, date
from io import BytesIO

from dotenv import load_dotenv
import hashlib
from jinja2 import Environment, FileSystemLoader
import os
from xhtml2pdf import pisa  # import python module
from pathlib import Path
import io
from datetime import datetime
import requests
from loguru import logger
from aws_requests_auth.aws_auth import AWSRequestsAuth

load_dotenv()

DO_SPACE = os.getenv("DO_SPACE")
DO_REGION = os.getenv("DO_REGION")
DO_KEY = os.getenv("DO_SPACE_ACCESS_KEY")
DO_SECRET = os.getenv("DO_SPACE_SECRET_KEY")

def _download_template(file_name, root):
    env = Environment(loader=FileSystemLoader(root))
    template = env.get_template(file_name)

    return template


def _fill_pdf(template, values):

    filled_template = template.render(values)
    # Convert the filled HTML template to PDF
    # config = pdfkit.configuration(wkhtmltopdf=os.path.join(os.environ.get('LAMBDA_TASK_ROOT', os.getcwd()), 'bin', 'wkhtmltopdf'))
    # pdf = pdfkit.from_string(filled_template, False, configuration=config)
    pisa_context = pisa.CreatePDF(filled_template, dest_bytes=True)
    pdf_stream = io.BytesIO(pisa_context)
    return pdf_stream


def _get_date_string():
    now = datetime.utcnow()
    year_month_day_format = '%Y-%m-%d'
    date = now.strftime(year_month_day_format)
    return date

def _save_orderform(binary_data, args, space_path, save_locally=False):
    user_id = args.get("user_id")
    order_id = args.get("order_id")
    # # UPLOAD PDF TO DO BUCKET
    if not save_locally:
        response = _save_remotely(binary_data, user_id, order_id, space_path)
    if save_locally:
        response = _save_locally(binary_data, user_id, order_id)

    return response


def _create_key_name(user_id, order_id, space_path):
    file_name = f"{user_id}_{order_id}.pdf"
    do_file_name = f"{space_path}/{file_name}"
    return do_file_name


def _save_remotely(binary_data, user_id, order_id, space_path):
    do_file_name = _create_key_name(user_id, order_id, space_path)
    STORAGETYPE = "STANDARD"

    # Define the file name and content type
    _ = _put_object(binary_data, do_file_name, DO_SPACE, DO_REGION, STORAGETYPE, DO_KEY, DO_SECRET)
    return _check_object(do_file_name, DO_SPACE, DO_REGION, DO_KEY, DO_SECRET)

def _put_object(binary_data, file_name, do_space, do_region, do_storage_type, do_key, do_secret):
    content_type = "application/pdf"
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
    response = requests.put(url, 
                            data=binary_data, 
                            headers=headers, 
                            auth=auth)

    if response.status_code != 200:
        response.raise_for_status()

    return response

def _construct_do_url(file_name, do_space, do_region):
    divider = "" if file_name[0] == "/" else "/"
    url = f'https://{do_space}.{do_region}.digitaloceanspaces.com{divider}{file_name}'
    return url

def _check_object(file_name, do_space, do_region, do_key, do_secret):
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
    return {"file": response.url, "file_size": int(content_size), "file_type":content_type}


def _save_locally(binary_data, user_id, order_id):

    key_name = f"{user_id}_{order_id}.pdf"

    with io.open(key_name, 'wb') as f:
        result = f.write(binary_data)

    return {"file": Path(key_name).absolute().as_uri(), "file_size": result}


def _get_object(file_name, do_space, do_region, do_key, do_secret):
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
        print("RESPONSE")
        print(response.content)
        print(response.headers)
        print(url)

        raise Exception({'error': 'Downloading file failed', 'status_code': response.status_code})

    return response.content


def _download_pdf(user_id, order_id, space_path):
    key_name = _create_key_name(user_id, order_id, space_path)
    # SPACE = "oxari-storage"
    content = _get_object(key_name, DO_SPACE, DO_REGION, DO_KEY, DO_SECRET)
    return content

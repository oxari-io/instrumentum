
from jinja2 import Environment, FileSystemLoader
import io
from xhtml2pdf import pisa
from pathlib import Path

from oxari.digitalocean import check_object, get_object, put_object  # import python module
import os

DO_SPACE = os.getenv("DO_SPACE")
DO_REGION = os.getenv("DO_REGION")
DO_KEY = os.getenv("DO_SPACE_ACCESS_KEY")
DO_SECRET = os.getenv("DO_SPACE_SECRET_KEY")

def _create_key_name(user_id, order_id, space_path):
    file_name = f"{user_id}_{order_id}.pdf"
    do_file_name = f"{space_path}/{file_name}"
    return do_file_name

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



def _save_document(binary_data, args, space_path, save_locally=False):
    user_id = args.get("user_id")
    order_id = args.get("order_id")
    # # UPLOAD PDF TO DO BUCKET
    if not save_locally:
        response = _save_pdf_remotely(binary_data, user_id, order_id, space_path)
    if save_locally:
        response = _save_pdf_locally(binary_data, user_id, order_id)

    return response

def _save_pdf_remotely(binary_data, user_id, order_id, space_path):
    do_file_name = _create_key_name(user_id, order_id, space_path)
    STORAGETYPE = "STANDARD"

    # Define the file name and content type
    _ = put_object(binary_data, do_file_name, DO_SPACE, DO_REGION, STORAGETYPE, DO_KEY, DO_SECRET, "application/pdf")
    return check_object(do_file_name, DO_SPACE, DO_REGION, DO_KEY, DO_SECRET)


def _save_pdf_locally(binary_data, user_id, order_id):

    key_name = f"{user_id}_{order_id}.pdf"

    with io.open(key_name, 'wb') as f:
        result = f.write(binary_data)

    return {"file": Path(key_name).absolute().as_uri(), "file_size": result}


def download_pdf(user_id, order_id, space_path):
    key_name = _create_key_name(user_id, order_id, space_path)
    content, _ = get_object(key_name, DO_SPACE, DO_REGION, DO_KEY, DO_SECRET)
    return content

from fastapi import File
from dotenv import load_dotenv, find_dotenv
from google.cloud import storage
import os
from datetime import datetime
import logging
from PyPDF2 import PdfReader
from io import BytesIO
from PIL import Image
import pytesseract
from retry import retry
import json

load_dotenv(find_dotenv(), override=True)

storage_client = storage.Client()
bucket_name = os.getenv("GCP_BUCKET_NAME")

logger = logging.getLogger(__name__)

@retry(tries=3,delay=2)
def upload_file(file:File)-> str:
    try:
        storage_client = storage.Client()
        bucket_name = os.getenv("GCP_BUCKET_NAME")
        # Generate a unique filename using current date and time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{current_time}_{file}"
        # Upload file to GCP bucket
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        file.seek(0)
        blob.upload_from_file(file)
        return filename
    except Exception as e:
        raise ValueError(f"Error in upload_file: {e}")

@retry(tries=3,delay=2)
def read_file_content(bucket_name: str, blob_name: str) -> str:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    file_content = blob.download_as_bytes()
    
    file_extension = blob_name.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(file_content)
    elif file_extension in ['jpg', 'jpeg', 'png']:
        return extract_text_from_image(file_content)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

def extract_text_from_pdf(file_content: bytes) -> str:
    pdf = PdfReader(BytesIO(file_content))
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

def extract_text_from_image(file_content: bytes) -> str:
    image = Image.open(BytesIO(file_content))
    return pytesseract.image_to_string(image)


def write_json_output(json_filename: str, processed_content:str):
    bucket = storage_client.bucket(bucket_name)
    json_blob = bucket.blob(json_filename)
    json_blob.upload_from_string(
        data=json.dumps(processed_content, indent=2),
        content_type='application/json'
    )
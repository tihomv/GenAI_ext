from dotenv import load_dotenv, find_dotenv
import os
import langchain_google_genai as genai
from google.cloud import storage
import base64
import logging
from PyPDF2 import PdfReader
from io import BytesIO
from PIL import Image
import pytesseract
from langchain_core.prompts import load_prompt
from retry import retry

load_dotenv(find_dotenv(), override=True)

logger = logging.getLogger(__name__)


def classify_document(llm, file_content: str, file_name: str) -> str:
    prompt = load_prompt(r"demo/prompts/classification.yaml")
    prompt = prompt.invoke({"file_content": file_content})
    try:
        response = llm.invoke(prompt)
        classification = response.strip()
        if classification not in ["Deed", "Mortgage", "DeedOfTrust", "N\A"]:
            raise ValueError(f"Invalid classification: {classification}")
        return classification
    except Exception as e:
        logger.error(f"Error classifying document: {str(e)}")
        raise

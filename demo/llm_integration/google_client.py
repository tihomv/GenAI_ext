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

load_dotenv(find_dotenv(), override=True)

logger = logging.getLogger(__name__)

def get_llm(model: str = "gemini-1.5-flash"):
    return genai.GoogleGenerativeAI(model=model)


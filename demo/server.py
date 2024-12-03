# from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse, JSONResponse
# from langserve import add_routes
from dotenv import load_dotenv, find_dotenv
from google.cloud import storage
import os
from datetime import datetime
from demo.llm_integration.google_client import get_llm
from demo.utils.utils import classify_document
from demo.utils.parsers import get_pydantic_parser, DocumentType
import logging
from pydantic import ValidationError
import json
from langchain_core.prompts import load_prompt
from demo.utils.document_loader import upload_file, read_file_content, write_json_output

import time

load_dotenv(find_dotenv(), override=True)

# app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize GCP storage client
bucket_name = os.getenv("GCP_BUCKET_NAME")
print(bucket_name)
# Initialize LLM
llm = get_llm()


# @app.get("/")
# async def redirect_root_to_docs():
#     return RedirectResponse("/docs")
#
# @app.post("/upload-and-process")
def process_file(filename):
    try:
        # Read and extract content from the file
        file_content = read_file_content(bucket_name, filename)
        logger.info(f"file content: {file_content}")

        # Classify the document
        logger.info("Classifying document...")
        doc_classification = classify_document(llm, file_content, filename)
        logger.info(f"Document classified as: {doc_classification}")

        # Get the appropriate Pydantic parser
        try:
            doc_type = DocumentType(doc_classification)
            print(doc_type)
            parser = get_pydantic_parser(doc_type)
        except ValueError:
            logger.error(f"Invalid document classification: {doc_classification}")
            return JSONResponse(content={
                "error": f"Invalid document classification: {doc_classification}"
            }, status_code=400)

        # Process the file using the parser
        logger.info("Processing file with parser...")
        processed_content = process_file_with_parser(file_content, filename, parser, llm, doc_classification)

        # Store the parsed information in the Google bucket
        json_filename = f"{os.path.splitext(filename)[0]}.json"

        write_json_output(json_filename=json_filename, processed_content=processed_content)

        logger.info(f"Stored parsed information in {json_filename}")
        return processed_content
        return JSONResponse(content={
            "message": "File processed successfully",
            "document_type": doc_classification,
            "result": processed_content,
            "json_file": json_filename,
        })
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


def upload_and_process_file(file):
    try:
        start_time = time.time()
        # filename = upload_file(file)
        elapsed_time = time.time() - start_time
        logger.info(f"upload_file: {elapsed_time}")

        # Read and extract content from the file
        start_time = time.time()
        file_content = read_file_content(bucket_name, filename)
        logger.info(f"file content: {file_content}")
        elapsed_time = time.time() - start_time
        logger.info(f"file_content {elapsed_time}")

        # Classify the document
        start_time = time.time()
        logger.info("Classifying document...")
        doc_classification = classify_document(llm, file_content, filename)
        logger.info(f"Document classified as: {doc_classification}")
        elapsed_time = time.time() - start_time
        logger.info(f"doc_classification {elapsed_time}")

        # Get the appropriate Pydantic parser
        try:
            start_time = time.time()
            doc_type = DocumentType(doc_classification)
            print(doc_type)
            parser = get_pydantic_parser(doc_type)
            elapsed_time = time.time() - start_time
            logger.info(f"get_pydantic_parser {elapsed_time}")
        except ValueError:
            logger.error(f"Invalid document classification: {doc_classification}")
            return JSONResponse(content={
                "error": f"Invalid document classification: {doc_classification}"
            }, status_code=400)

        # Process the file using the parser
        start_time = time.time()
        logger.info("Processing file with parser...")
        processed_content = process_file_with_parser(file_content, filename, parser, llm, doc_classification)
        elapsed_time = time.time() - start_time
        logger.info(f"Processing file with parser {elapsed_time}")

        # Store the parsed information in the Google bucket
        start_time = time.time()
        json_filename = f"document_extr/static/json/{os.path.splitext(filename)[0]}.json"
        write_json_output(json_filename=json_filename, processed_content=processed_content)
        elapsed_time = time.time() - start_time
        print(f"Stored parsed information {elapsed_time}")
        logger.info(f"Stored parsed information in {json_filename}")
        return processed_content
        # return JSONResponse(content={
        #     "message": "File processed successfully",
        #     "document_type": doc_classification,
        #     "result": processed_content,
        #     "json_file": json_filename,
        # })
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


def process_file_with_parser(file_content: str, filename: str, parser, llm, doc_classification: str):
    # Load the appropriate prompt template based on the document classification
    prompt_file = f".\prompts\{doc_classification.lower()}.yaml"
    try:
        prompt = load_prompt(prompt_file)
    except FileNotFoundError:
        logger.warning(f"Specific prompt file not found for {doc_classification}. Using base prompt.")
        prompt = load_prompt(r"demo/prompts/base.yaml")

    # Prepare the prompt with file content and parser instructions
    formatted_prompt = prompt.format(
        file_content=file_content,
        format_instructions=parser.get_format_instructions()
    )

    logger.info("Invoking LLM for information extraction...")
    response = llm.invoke(formatted_prompt)
    print(f"final response: {response}")
    logger.info("LLM response received")

    try:
        logger.info("Parsing LLM response...")
        parsed_content = parser.parse(response)
        logger.info("LLM response parsed successfully")
        return parsed_content.dict(exclude_none=True)  # This will exclude any None values from the output
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        logger.error(f"LLM response: {response}")
        # Instead of raising an error, return partial results
        partial_results = e.model.dict(exclude_none=True)
        logger.info(f"Returning partial results: {partial_results}")
        return partial_results

# Edit this to add the chain you want to add
# add_routes(app, NotImplemented)

# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)

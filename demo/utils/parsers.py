from langchain_core.output_parsers import PydanticOutputParser
from .fields_model import Deed, DeedOfTrust, Mortgage, Documents
from typing import List, Optional
from enum import Enum

class DocumentType(Enum):
    DEED = "Deed"
    MORTGAGE = "Mortgage"
    DEED_OF_TRUST = "DeedOfTrust"

def get_pydantic_parser(doctype: DocumentType):
    if doctype == DocumentType.DEED:
        return PydanticOutputParser(pydantic_object=Deed)
    elif doctype == DocumentType.MORTGAGE:
        return PydanticOutputParser(pydantic_object=Mortgage)
    elif doctype == DocumentType.DEED_OF_TRUST:
        return PydanticOutputParser(pydantic_object=DeedOfTrust)
    else:
        raise ValueError(f"Invalid document type: {doctype}")

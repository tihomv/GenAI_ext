from pydantic import BaseModel, RootModel
from typing import List, Optional

class Deed(BaseModel):
    document_classification: str
    document_classification_confidence: float
    borrower_first_name: Optional[str] = None
    borrower_first_name_confidence: Optional[float] = None
    borrower_last_name: Optional[str] = None
    borrower_last_name_confidence: Optional[float] = None
    borrower_relationship_type: Optional[str] = None
    borrower_relationship_type_confidence: Optional[float] = None
    borrower_zip_code: Optional[str] = None
    borrower_zip_code_confidence: Optional[float] = None
    borrower_city: Optional[str] = None
    borrower_city_confidence: Optional[float] = None
    borrower_state: Optional[str] = None
    borrower_state_confidence: Optional[float] = None
    borrower_street_address: Optional[str] = None
    borrower_street_address_confidence: Optional[float] = None
    sale_date: Optional[str] = None
    sale_date_confidence: Optional[float] = None
    sale_price: Optional[str] = None
    sale_price_confidence: Optional[float] = None
    company_name: Optional[str] = None
    company_name_confidence: Optional[float] = None
    attorney_name: Optional[str] = None
    attorney_name_confidence: Optional[float] = None
    lender_first_name_or_company_name: Optional[str] = None
    lender_first_name_or_company_name_confidence: Optional[float] = None
    lender_zip_code: Optional[str] = None
    lender_zip_code_confidence: Optional[float] = None
    lender_city: Optional[str] = None
    lender_city_confidence: Optional[float] = None
    lender_state: Optional[str] = None
    lender_state_confidence: Optional[float] = None
    property_zip_code: Optional[str] = None
    property_zip_code_confidence: Optional[float] = None
    property_city: Optional[str] = None
    property_city_confidence: Optional[float] = None
    amortization_term: Optional[str] = None
    amortization_term_confidence: Optional[float] = None
    loan_due_date: Optional[str] = None
    loan_due_date_confidence: Optional[float] = None
    interest_rate: Optional[str] = None
    interest_rate_confidence: Optional[float] = None

class Mortgage(BaseModel):
    document_classification: str
    document_classification_confidence: float
    borrower_first_name: Optional[str] = None
    borrower_first_name_confidence: Optional[float] = None
    borrower_last_name: Optional[str] = None
    borrower_last_name_confidence: Optional[float] = None
    borrower_relationship_type: Optional[str] = None
    borrower_relationship_type_confidence: Optional[float] = None
    borrower_zip_code: Optional[str] = None
    borrower_zip_code_confidence: Optional[float] = None
    borrower_city: Optional[str] = None
    borrower_city_confidence: Optional[float] = None
    borrower_state: Optional[str] = None
    borrower_state_confidence: Optional[float] = None
    borrower_street_address: Optional[str] = None
    borrower_street_address_confidence: Optional[float] = None
    sale_date: Optional[str] = None
    sale_date_confidence: Optional[float] = None
    sale_price: Optional[str] = None
    sale_price_confidence: Optional[float] = None
    company_name: Optional[str] = None
    company_name_confidence: Optional[float] = None
    attorney_name: Optional[str] = None
    attorney_name_confidence: Optional[float] = None
    lender_first_name_or_company_name: Optional[str] = None
    lender_first_name_or_company_name_confidence: Optional[float] = None
    lender_zip_code: Optional[str] = None
    lender_zip_code_confidence: Optional[float] = None
    lender_city: Optional[str] = None
    lender_city_confidence: Optional[float] = None
    lender_state: Optional[str] = None
    lender_state_confidence: Optional[float] = None
    property_zip_code: Optional[str] = None
    property_zip_code_confidence: Optional[float] = None
    property_city: Optional[str] = None
    property_city_confidence: Optional[float] = None
    amortization_term: Optional[str] = None
    amortization_term_confidence: Optional[float] = None
    loan_due_date: Optional[str] = None
    loan_due_date_confidence: Optional[float] = None
    interest_rate: Optional[str] = None
    interest_rate_confidence: Optional[float] = None

class DeedOfTrust(BaseModel):
    document_classification: str
    document_classification_confidence: float
    borrower_first_name: Optional[str] = None
    borrower_first_name_confidence: Optional[float] = None
    borrower_last_name: Optional[str] = None
    borrower_last_name_confidence: Optional[float] = None
    borrower_relationship_type: Optional[str] = None
    borrower_relationship_type_confidence: Optional[float] = None
    borrower_zip_code: Optional[str] = None
    borrower_zip_code_confidence: Optional[float] = None
    borrower_city: Optional[str] = None
    borrower_city_confidence: Optional[float] = None
    borrower_state: Optional[str] = None
    borrower_state_confidence: Optional[float] = None
    borrower_street_address: Optional[str] = None
    borrower_street_address_confidence: Optional[float] = None
    sale_date: Optional[str] = None
    sale_date_confidence: Optional[float] = None
    sale_price: Optional[str] = None
    sale_price_confidence: Optional[float] = None
    company_name: Optional[str] = None
    company_name_confidence: Optional[float] = None
    attorney_name: Optional[str] = None
    attorney_name_confidence: Optional[float] = None
    lender_first_name_or_company_name: Optional[str] = None
    lender_first_name_or_company_name_confidence: Optional[float] = None
    lender_zip_code: Optional[str] = None
    lender_zip_code_confidence: Optional[float] = None
    lender_city: Optional[str] = None
    lender_city_confidence: Optional[float] = None
    lender_state: Optional[str] = None
    lender_state_confidence: Optional[float] = None
    property_zip_code: Optional[str] = None
    property_zip_code_confidence: Optional[float] = None
    property_city: Optional[str] = None
    property_city_confidence: Optional[float] = None
    amortization_term: Optional[str] = None
    amortization_term_confidence: Optional[float] = None
    loan_due_date: Optional[str] = None
    loan_due_date_confidence: Optional[float] = None
    interest_rate: Optional[str] = None
    interest_rate_confidence: Optional[float] = None

class Document(BaseModel):
    Deed: Optional[Deed] = None
    Mortgage: Optional[Mortgage] = None
    DeedOfTrust: Optional[DeedOfTrust] = None

class Documents(RootModel):
    root: List[Document]

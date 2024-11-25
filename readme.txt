1. Dango webframework is used for UI.
2. Google cloud is used to store documents.
3. PyPDF2 is used to read content of the pdf.
4. Pre-defined classification prompt is used with gemini-1.5-pro to classify the given document.
5. According to the classification list of field extracted from the document is selected.
6. Pre-defined document type prompt is used with gemini-1.5-pro to extract field from the given document.
7. Data Manipulation on llm output from gemini to fill into UI.
 
 
 Overview  
This project involves a web application built using the Django framework for its user interface, Google Cloud for document storage, and advanced AI-driven classification and extraction techniques powered by Gemini-1.5-pro. PyPDF2 is employed to process PDF documents, while pre-defined prompts enable document classification and field extraction.


Step-by-Step Flow

1. Document Upload via Django Web Interface
- User Interaction: Users access the Django web application through their browser. 
- Action: Users upload a document (PDF format) using the UI.
- Outcome: The document is sent to Google Cloud for secure storage.



 2. Storing Documents on Google Cloud
- Technology: The uploaded document is transmitted to Google Cloud Storage via Django backend integration.
- Outcome: A unique identifier (URL/path) for the document is stored in the database for further processing.



 3. Reading Content of the PDF using PyPDF2
- Action: The backend retrieves the document from Google Cloud.
- Processing: PyPDF2 extracts textual content from the PDF.
- Outcome: The text content is prepared for classification.



 4. Document Classification using Gemini-1.5-pro
- Input: Extracted text from the PDF and a pre-defined classification prompt.
- Technology: The prompt is sent to Gemini-1.5-pro to determine the document type (e.g., Invoice, Contract, Report).
- Outcome: Gemini-1.5-pro returns the document classification.



 5. Field Selection Based on Classification
- Action: Based on the document classification, a pre-defined list of fields relevant to that type is retrieved (e.g., for an Invoice, fields like Invoice Number, Date, Amount, etc.).
- Outcome: The field list is finalized for extraction.



 6. Field Extraction using Gemini-1.5-pro
- Input: The original document text and a pre-defined document type prompt.
- Technology: The prompt guides Gemini-1.5-pro to extract specific fields from the document.
- Outcome: Gemini-1.5-pro provides structured field data (e.g., Invoice Number: 12345, Date: 2023-11-18, Amount: $1000).



 7. Data Manipulation for UI Integration
- Action: The structured output from Gemini-1.5-pro is processed and formatted to match the UI's requirements.
- Technology: Custom Python scripts manipulate the data to ensure consistency and accuracy.
- Outcome: The extracted information is displayed on the Django web UI for user review and interaction.



 End-to-End Summary
1. Users upload a document via the Django UI.  
2. The document is securely stored in Google Cloud.  
3. PyPDF2 extracts text content from the PDF.  
4. Gemini-1.5-pro classifies the document using a pre-defined prompt.  
5. Relevant fields are selected based on classification.  
6. Gemini-1.5-pro extracts specific field values using another pre-defined prompt.  
7. Data is manipulated and presented in the UI for user interaction.

This seamless flow ensures an efficient, AI-driven document processing experience.
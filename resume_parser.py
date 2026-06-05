import pdfplumber
from docx import Document
from io import BytesIO

def extract_text_from_pdf(uploaded_file):
    """
    Extract text from PDF uploaded in Streamlit file_uploader.
    """
    text = ""

    # uploaded_file is a BytesIO object
    with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    return text


def extract_text_from_docx(uploaded_file):
    """
    Extract text from DOCX uploaded in Streamlit file_uploader.
    """
    text = ""
    doc = Document(uploaded_file)

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text

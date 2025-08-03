# modules/document_parser.py

import fitz  # PyMuPDF
import docx
from typing import Literal


def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from a PDF file using PyMuPDF"""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_text_from_docx(file_path: str) -> str:
    """Extracts text from a DOCX file using python-docx"""
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


def extract_text(file_path: str, file_type: Literal['pdf', 'docx']) -> str:
    """Detects format and returns extracted text"""
    if file_type == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_type == "docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Use 'pdf' or 'docx'")

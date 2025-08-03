# test_document_parser.py

from modules.document_parser import extract_text

file_path = "data/draft.docx"  # Change to .pdf if testing with PDF
file_type = "docx"  # or "pdf"

text = extract_text(file_path, file_type)

print("\n✅ Extracted Text:\n")
print(text[:1000])  # Show only first 1000 characters

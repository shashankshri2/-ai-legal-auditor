# test_citation_extractor.py

from modules.citation_extractor import extract_citations
from modules.document_parser import extract_text

text = extract_text("data/draft.docx", "docx")
citations = extract_citations(text)

print("\n🔎 Extracted Citations:")
for c in citations:
    print("-", c)

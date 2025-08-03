# test_web_verifier.py

from modules.document_parser import extract_text
from modules.citation_extractor import extract_citations
from modules.web_verifier import verify_citations_with_web

# Load document
text = extract_text("data/draft.docx", "docx")

# Extract citations
citations = extract_citations(text)

# Load whitelist
with open("config/whitelist.txt", "r") as f:
    whitelist = [line.strip() for line in f.readlines()]

# Simulate verification
results = verify_citations_with_web(citations, whitelist)

print("\n🌐 Web Verification Results:")
for r in results:
    print(f"- {r['citation']} → {'✅ Verified' if r['verified'] else '❌ Not Found'} | Confidence: {r['confidence']}")

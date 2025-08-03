import argparse
import os
from datetime import datetime

from modules.document_parser import extract_text
from modules.citation_extractor import extract_citations
from modules.web_verifier import verify_with_web
from modules.rag_verifier import load_knowledge_base, embed_cases, verify_with_rag
from modules.report_generator import generate_audit_report

def load_whitelist(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def print_console_summary(audit_data):
    print("\n📊 Audit Summary:\n")
    for item in audit_data:
        print(f"📑 Citation: {item['citation']}")
        web = item["web_verification"]
        rag = item["rag_verification"]

        print(f"   🌐 Web Verified: {'✅' if web['verified'] else '❌'} (Confidence: {web['confidence']})")
        print(f"   🧠 RAG Match: {'✅' if rag['match'] else '❌'} (Matched: {rag['matched_case']}, Confidence: {rag['confidence']})")
        print("")

def main():
    parser = argparse.ArgumentParser(description="AI Legal Auditor - Case Draft Verifier")
    parser.add_argument("input_file", help="Path to .docx or .pdf draft document")
    args = parser.parse_args()

    input_path = args.input_file
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        return

    # Determine file type
    file_type = "pdf" if input_path.endswith(".pdf") else "docx"

    # Step 1: Extract text
    text = extract_text(input_path, file_type=file_type)

    # Step 2: Extract citations
    citations = extract_citations(text)

    # Step 3: Web verification
    whitelist = load_whitelist("config/whitelist.txt")
    web_results = verify_with_web(citations, whitelist)

    # Step 4: RAG verification
    cases = load_knowledge_base("data/knowledge_base.json")
    index, embeddings, contents = embed_cases(cases)
    rag_results = verify_with_rag(citations, cases, index, contents)

    # Step 5: Save Report
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_path = f"output/audit_report_{timestamp}.json"
    audit_data = generate_audit_report(citations, web_results, rag_results, output_path)

    print(f"\n✅ Audit report generated at: {output_path}")

    # Step 6: Print summary
    print_console_summary(audit_data)

if __name__ == "__main__":
    main()

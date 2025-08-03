import datetime
from modules.document_parser import extract_text
from modules.citation_extractor import extract_citations
from modules.web_verifier import verify_with_web
from modules.rag_verifier import load_knowledge_base, embed_cases, verify_with_rag
from modules.report_generator import generate_audit_report

def load_whitelist(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def main():
    print("🚀 Starting AI Legal Auditor...\n")

    # Step 1: Extract text from document
    text = extract_text("data/draft.docx", file_type="docx")

    # Step 2: Extract citations
    citations = extract_citations(text)

    # Step 3: Web verification
    whitelist = load_whitelist("config/whitelist.txt")
    web_results = verify_with_web(citations, whitelist)

    # Step 4: RAG verification
    cases = load_knowledge_base("data/knowledge_base.json")
    case_embeddings = embed_cases(cases)
    rag_results = verify_with_rag(citations, cases, case_embeddings)

    # Step 5: Generate timestamped report filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    output_path = f"output/audit_report_{timestamp}.json"

    # Step 6: Generate audit report
    generate_audit_report(
        citations=citations,
        web_results=web_results,
        rag_results=rag_results,
        output_path=output_path
    )

    # Step 7: Print console summary
    total = len(citations)
    web_pass = sum(1 for res in web_results if res.get("verified"))
    rag_pass = sum(1 for res in rag_results if res.get("match"))

    print(f"\n✅ Audit report generated at: {output_path}")
    print("\n📊 Summary:")
    print(f"- Total Citations Analyzed: {total}")
    print(f"- Web Verified: {web_pass}/{total}")
    print(f"- RAG Verified (Strong Match): {rag_pass}/{total}")

if __name__ == "__main__":
    main()

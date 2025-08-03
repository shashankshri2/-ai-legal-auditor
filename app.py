import os
import json
import streamlit as st
from datetime import datetime

from modules.document_parser import extract_text
from modules.citation_extractor import extract_citations
from modules.web_verifier import verify_with_web
from modules.rag_verifier import load_knowledge_base, embed_cases, verify_with_rag_basic
from modules.report_generator import generate_audit_report

st.set_page_config(page_title="AI Legal Auditor", layout="centered")

st.title("⚖️ AI Legal Auditor - Case Draft Verifier")
st.markdown("Upload a legal draft file (.pdf or .docx) to begin the audit process.")

uploaded_file = st.file_uploader("📄 Upload your file", type=["pdf", "docx"])

if uploaded_file is not None:
    file_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ File uploaded successfully.")
    
    with st.spinner("📄 Extracting text from uploaded document..."):
        file_type = "pdf" if uploaded_file.name.endswith(".pdf") else "docx"
        contents = extract_text(file_path, file_type)
    st.success("✅ Text extraction complete.")

    with st.spinner("🔍 Extracting citations..."):
        citations = extract_citations(contents)
    st.success(f"✅ Found {len(citations)} citation(s).")

    with st.spinner("🌐 Performing web verification..."):
        whitelist_path = "config/whitelist.txt"
        whitelist = []
        if os.path.exists(whitelist_path):
            with open(whitelist_path, "r", encoding="utf-8") as f:
                whitelist = [line.strip() for line in f.readlines()]
        web_results = verify_with_web(citations, whitelist)
    st.success("✅ Web verification complete.")

    with st.spinner("🧠 Performing RAG (basic semantic similarity) verification..."):
        knowledge_base_path = "data/knowledge_base.json"
        cases = load_knowledge_base(knowledge_base_path)
        embeddings, contents_embed, filtered_cases = embed_cases(cases)
        rag_results = verify_with_rag_basic(citations, filtered_cases, embeddings, contents_embed)
    st.success("✅ RAG verification complete.")

    with st.spinner("📄 Generating final audit report..."):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        output_path = f"output/audit_report_{timestamp}.json"
        os.makedirs("output", exist_ok=True)
        audit_data = generate_audit_report(citations, web_results, rag_results, output_path)
    st.success("✅ Audit report generated.")

    st.subheader("📊 Audit Summary")
    for item in audit_data:
        st.markdown(f"📑 **Citation:** {item['citation']}")
        st.markdown(f"🌐 **Web Verified:** {'✅' if item['web_verification']['verified'] else '❌'} (Confidence: {item['web_verification']['confidence']})")
        st.markdown(f"🧠 **RAG Match:** {'✅' if item['rag_verification']['match'] else '❌'} (Matched: {item['rag_verification']['matched_case']}, Confidence: {item['rag_verification']['confidence']})")
        st.markdown("---")

    # Add download button
    with open(output_path, "rb") as f:
        st.download_button("💾 Download JSON Report", data=f, file_name=os.path.basename(output_path), mime="application/json")

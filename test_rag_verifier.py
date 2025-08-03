# test_rag_verifier.py

from modules.rag_verifier import load_knowledge_base, embed_cases, verify_with_rag

# Simulate extracted citations
citations_to_check = [
    "ABC vs XYZ, [2015] 2 SCC 305",
    "DEF vs GHI, AIR 2020 SC 123",
    "Unknown vs Case, 2019"
]

# Load knowledge base
kb = load_knowledge_base("data/knowledge_base.json")
embeddings = embed_cases(kb)

print("\n🔎 RAG Verification Results:")
for citation in citations_to_check:
    matched_citation, confidence = verify_with_rag(citation, kb, embeddings)
    status = "✅ Match" if confidence > 0.8 else "❌ Weak Match"
    print(f"- {citation} → {matched_citation} | Confidence: {confidence} | {status}")

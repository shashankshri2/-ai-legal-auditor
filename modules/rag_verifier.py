import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

def load_knowledge_base(path):
    import json
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def embed_cases(cases):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    contents = [case["content"] for case in cases if "content" in case]
    filtered_cases = [case for case in cases if "content" in case]
    
    if not contents:
        return [], [], []
    
    embeddings = model.encode(contents)
    return embeddings, contents, filtered_cases

def verify_with_rag_basic(citations, cases, embeddings, contents):
    from numpy.linalg import norm

    results = []
    
    if len(embeddings) == 0 or len(cases) == 0:
        for citation in citations:
            results.append({
                "citation": citation,
                "match": False,
                "matched_case": "N/A",
                "confidence": 0.0
            })
        return results

    embeddings_np = np.stack(embeddings).astype("float32")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    for citation in citations:
        query_vec = model.encode([citation])
        
        # Ensure query_vec is 2D
        if len(query_vec.shape) == 1:
            query_vec = query_vec.reshape(1, -1)

        sims = cosine_similarity(query_vec, embeddings_np)[0]
        idx = int(np.argmax(sims))
        confidence = float(sims[idx])

        matched_case = cases[idx]["title"] if 0 <= idx < len(cases) and "title" in cases[idx] else "N/A"

        results.append({
            "citation": citation,
            "match": confidence > 0.75,
            "matched_case": matched_case,
            "confidence": round(confidence, 2)
        })

    return results

# modules/web_verifier.py

from typing import List, Dict

def verify_with_web(citations: List[str], whitelist: List[str]) -> List[Dict]:
    """
    Simulates checking each citation against a trusted source.
    Returns verification result with dummy confidence.
    """
    verified_cases = [
        "ABC vs XYZ, [2015] 2 SCC 305",
        "DEF vs GHI, AIR 2020 SC 123"
    ]

    results = []
    for citation in citations:
        found = citation in verified_cases
        results.append({
            "citation": citation,
            "verified": found,
            "source": whitelist[0] if found else None,
            "confidence": 0.95 if found else 0.2
        })
    return results

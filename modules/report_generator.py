import json
import numpy as np

def convert_to_serializable(obj):
    """Convert numpy and other non-serializable types to native Python types."""
    if isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.bool_)):
        return bool(obj)
    elif isinstance(obj, (bytes, bytearray)):
        return obj.decode("utf-8", errors="ignore")
    return obj

def generate_audit_report(citations, web_results, rag_results, output_path):
    report = []

    for citation in citations:
        web_info = next((item for item in web_results if item["citation"] == citation), {})
        rag_info = next((item for item in rag_results if item["citation"] == citation), {})

        # Apply conversion for each dictionary
        web_info_serialized = {k: convert_to_serializable(v) for k, v in web_info.items()}
        rag_info_serialized = {k: convert_to_serializable(v) for k, v in rag_info.items()}

        report.append({
            "citation": citation,
            "web_verification": web_info_serialized,
            "rag_verification": rag_info_serialized
        })

    # Write report to JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return report

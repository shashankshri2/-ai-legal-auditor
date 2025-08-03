# modules/citation_extractor.py

import re
from typing import List

def extract_citations(text: str) -> List[str]:
    """
    Extract clean legal citations like:
    - ABC vs XYZ, [2015] 2 SCC 305
    - DEF vs GHI, AIR 2020 SC 123
    """
    pattern = r"[A-Z][A-Za-z\s]+? vs [A-Z][A-Za-z\s]+?, (?:\[\d{4}\] \d+ [A-Z]+ \d+|AIR \d{4} [A-Z]+ \d+)"
    matches = re.findall(pattern, text)
    return [match.strip() for match in matches]

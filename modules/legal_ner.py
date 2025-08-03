import spacy
from typing import List, Dict

nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str) -> List[Dict]:
    """
    Extract legal entities: case parties and NER types.
    """
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG"]:
            entities.append({"text": ent.text, "label": ent.label_})
    return entities

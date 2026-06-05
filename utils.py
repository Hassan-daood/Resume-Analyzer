import re
import spacy

nlp = None
try:
    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
except:
    nlp = None

def normalize_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9\s\-#.+]", " ", text)
    text = text.strip()

    if nlp:
        doc = nlp(text)
        tokens = [token.lemma_ for token in doc if not token.is_stop]
        return " ".join(tokens)

    return text

from utils import normalize_text
from rapidfuzz import fuzz

# List of skills to detect
SKILL_LIST = [
    "python", "machine learning", "deep learning", "sql", 
    "data analysis", "data cleaning", "communication",
    "excel", "chatgpt", "power bi", "tableau"
]

def extract_skills(text):
    text = text.lower()
    found = [skill for skill in SKILL_LIST if skill.lower() in text]
    return found

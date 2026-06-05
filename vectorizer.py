from utils import normalize_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_text, jd_text):
    vect = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vect.fit_transform([resume_text, jd_text])
    return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])

# OPTIONAL SEMANTIC MATCHING
try:
    from sentence_transformers import SentenceTransformer
    sbert = SentenceTransformer("all-MiniLM-L6-v2")
except:
    sbert = None

def semantic_similarity(resume_text, jd_text):
    if not sbert:
        return calculate_similarity(resume_text, jd_text)
    r = sbert.encode(resume_text)
    j = sbert.encode(jd_text)
    return float(cosine_similarity([r], [j])[0][0])

def combined_match_score(resume_text, jd_text):
    tfidf = calculate_similarity(resume_text, jd_text)
    sem = semantic_similarity(resume_text, jd_text)
    return 0.4 * tfidf + 0.6 * sem

from sentence_transformers import SentenceTransformer, util
from textstat import flesch_reading_ease
import re

# Load sentence transformer for semantic similarity
model = SentenceTransformer('all-MiniLM-L6-v2')

def evaluate_answer(question: str, user_answer: str, ideal_keywords: list = None) -> dict:
    # 1. Semantic similarity between question and answer context (how well answer addresses question)
    q_emb = model.encode(question, convert_to_tensor=True)
    a_emb = model.encode(user_answer, convert_to_tensor=True)
    cosine_score = util.pytorch_cos_sim(q_emb, a_emb).item()
    relevance = round(cosine_score * 100, 1)

    # 2. Grammar check (simple: sentence length, punctuation)
    sentences = re.split(r'[.!?]+', user_answer)
    avg_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    grammar_score = min(100, max(0, 50 + (avg_length - 5) * 5))  # heuristic

    # 3. Flesch Reading Ease (readability)
    readability = flesch_reading_ease(user_answer)
    readability_score = min(100, max(0, readability))

    # 4. Keyword match (if provided)
    keyword_score = 0
    if ideal_keywords:
        words = set(user_answer.lower().split())
        matched = sum(1 for kw in ideal_keywords if kw.lower() in words)
        keyword_score = round(matched / len(ideal_keywords) * 100, 1)

    overall = round(relevance * 0.5 + grammar_score * 0.15 + readability_score * 0.15 + keyword_score * 0.2, 1)

    return {
        "relevance": relevance,
        "grammar": grammar_score,
        "readability": readability_score,
        "keyword_match": keyword_score,
        "overall_score": overall
    }
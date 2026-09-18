from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter
import math
import re


app = FastAPI(
    title="RAG Evaluation & Quality Scoring API",
    description="API for evaluating RAG answers using pure Python text similarity.",
    version="1.0.0"
)


class EvaluationRequest(BaseModel):
    question: str
    answer: str
    sources: list[str]


def tokenize(text):
    return re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())


def tfidf_similarity(text1, text2):
    words1 = tokenize(text1)
    words2 = tokenize(text2)

    if not words1 or not words2:
        return 0.0

    vocabulary = set(words1 + words2)

    count1 = Counter(words1)
    count2 = Counter(words2)

    vector1 = {}
    vector2 = {}

    total1 = len(words1)
    total2 = len(words2)

    for word in vocabulary:
        tf1 = count1[word] / total1
        tf2 = count2[word] / total2

        document_frequency = 0

        if word in count1:
            document_frequency += 1

        if word in count2:
            document_frequency += 1

        idf = math.log((2 + 1) / (document_frequency + 1)) + 1

        vector1[word] = tf1 * idf
        vector2[word] = tf2 * idf

    dot_product = sum(
        vector1[word] * vector2[word]
        for word in vocabulary
    )

    magnitude1 = math.sqrt(
        sum(value * value for value in vector1.values())
    )

    magnitude2 = math.sqrt(
        sum(value * value for value in vector2.values())
    )

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def percentage(score):
    return round(max(0.0, min(1.0, score)) * 100, 2)


@app.get("/")
def home():
    return {
        "project": "RAG Evaluation & Quality Scoring API",
        "status": "running",
        "description": "Evaluate RAG answers using pure Python similarity."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "evaluation_method": "Pure Python TF-IDF Cosine Similarity",
        "external_ml_dependencies": False
    }


@app.post("/evaluate")
def evaluate(request: EvaluationRequest):

    question = request.question.strip()
    answer = request.answer.strip()

    sources = [
        source.strip()
        for source in request.sources
        if source.strip()
    ]

    if not question:
        return {
            "error": "Question cannot be empty."
        }

    if not answer:
        return {
            "error": "Answer cannot be empty."
        }

    if not sources:
        return {
            "error": "At least one source is required."
        }

    # Question → Answer relevance
    answer_relevance = tfidf_similarity(
        question,
        answer
    )

    # Question → Source relevance
    source_question_scores = [
        tfidf_similarity(question, source)
        for source in sources
    ]

    # Answer → Source grounding
    source_answer_scores = [
        tfidf_similarity(answer, source)
        for source in sources
    ]

    answer_relevance_percent = percentage(
        answer_relevance
    )

    source_relevance_percent = percentage(
        sum(source_question_scores)
        / len(source_question_scores)
    )

    grounding_percent = percentage(
        sum(source_answer_scores)
        / len(source_answer_scores)
    )

    # Overall score
    overall_score = round(
        (
            answer_relevance_percent
            + source_relevance_percent
            + grounding_percent
        ) / 3,
        2
    )

    if overall_score >= 80:
        quality = "Excellent"
    elif overall_score >= 60:
        quality = "Good"
    elif overall_score >= 40:
        quality = "Needs Improvement"
    else:
        quality = "Poor"

    source_evaluation = []

    for index, source in enumerate(sources):

        source_evaluation.append(
            {
                "source_number": index + 1,
                "source": source,
                "question_relevance": percentage(
                    source_question_scores[index]
                ),
                "answer_similarity": percentage(
                    source_answer_scores[index]
                )
            }
        )

    return {
        "question": question,
        "answer": answer,
        "evaluation_method": "Pure Python TF-IDF Cosine Similarity",
        "metrics": {
            "answer_relevance": answer_relevance_percent,
            "source_relevance": source_relevance_percent,
            "grounding_score": grounding_percent,
            "overall_quality_score": overall_score
        },
        "quality": quality,
        "source_evaluation": source_evaluation
    }
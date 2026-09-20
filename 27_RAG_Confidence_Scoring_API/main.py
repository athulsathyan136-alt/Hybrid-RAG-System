from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter
import math
import re


app = FastAPI(
    title="RAG Confidence Scoring API",
    description="Calculate confidence scores for RAG answers.",
    version="1.0.0"
)


class ConfidenceRequest(BaseModel):
    question: str
    answer: str
    sources: list[str]


def tokenize(text):
    return re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())


def similarity(text1, text2):
    words1 = tokenize(text1)
    words2 = tokenize(text2)

    if not words1 or not words2:
        return 0.0

    count1 = Counter(words1)
    count2 = Counter(words2)

    vocabulary = set(words1 + words2)

    vector1 = []
    vector2 = []

    for word in vocabulary:
        vector1.append(count1[word])
        vector2.append(count2[word])

    dot_product = sum(
        a * b for a, b in zip(vector1, vector2)
    )

    magnitude1 = math.sqrt(
        sum(a * a for a in vector1)
    )

    magnitude2 = math.sqrt(
        sum(b * b for b in vector2)
    )

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def percentage(value):
    return round(
        max(0.0, min(1.0, value)) * 100,
        2
    )


def split_sentences(text):
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


@app.get("/")
def home():
    return {
        "project": "RAG Confidence Scoring API",
        "status": "running",
        "description": "Calculate confidence scores for RAG answers."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "scoring_method": "Pure Python Similarity",
        "external_ml_dependencies": False
    }


@app.post("/confidence")
def calculate_confidence(request: ConfidenceRequest):

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

    combined_sources = " ".join(sources)

    # Question → Answer relevance
    answer_relevance = similarity(
        question,
        answer
    )

    # Question → Sources relevance
    source_scores = [
        similarity(question, source)
        for source in sources
    ]

    source_relevance = (
        sum(source_scores) / len(source_scores)
    )

    # Answer → Sources grounding
    grounding_scores = [
        similarity(answer, source)
        for source in sources
    ]

    grounding_score = (
        sum(grounding_scores) / len(grounding_scores)
    )

    # Sentence-level source coverage
    sentences = split_sentences(answer)

    supported_sentences = 0

    sentence_scores = []

    for sentence in sentences:

        score = similarity(
            sentence,
            combined_sources
        )

        sentence_scores.append(
            percentage(score)
        )

        if score >= 0.25:
            supported_sentences += 1

    if sentences:
        citation_coverage = (
            supported_sentences / len(sentences)
        )
    else:
        citation_coverage = 0.0

    # Convert metrics to percentages
    answer_relevance_percent = percentage(
        answer_relevance
    )

    source_relevance_percent = percentage(
        source_relevance
    )

    grounding_percent = percentage(
        grounding_score
    )

    citation_coverage_percent = percentage(
        citation_coverage
    )

    # Overall confidence
    confidence_score = round(
        (
            answer_relevance_percent
            + source_relevance_percent
            + grounding_percent
            + citation_coverage_percent
        ) / 4,
        2
    )

    if confidence_score >= 80:
        confidence_level = "High"
    elif confidence_score >= 60:
        confidence_level = "Medium"
    else:
        confidence_level = "Low"

    return {
        "question": question,
        "answer": answer,
        "metrics": {
            "answer_relevance": answer_relevance_percent,
            "source_relevance": source_relevance_percent,
            "grounding_score": grounding_percent,
            "citation_coverage": citation_coverage_percent
        },
        "confidence_score": confidence_score,
        "confidence_level": confidence_level,
        "total_answer_sentences": len(sentences),
        "supported_sentences": supported_sentences,
        "sentence_scores": sentence_scores
    }
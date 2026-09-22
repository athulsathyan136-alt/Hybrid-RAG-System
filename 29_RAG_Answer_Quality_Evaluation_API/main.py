from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter
import math
import re


app = FastAPI(
    title="RAG Answer Quality Evaluation API",
    description="Evaluate the quality of RAG-generated answers.",
    version="1.0.0"
)


class QualityRequest(BaseModel):
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
        "project": "RAG Answer Quality Evaluation API",
        "status": "running",
        "description": "Evaluate the quality of RAG-generated answers."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "evaluation_method": "Pure Python Similarity",
        "external_ml_dependencies": False
    }


@app.post("/evaluate")
def evaluate_quality(request: QualityRequest):

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

    # 1. Answer relevance
    answer_relevance = percentage(
        similarity(question, answer)
    )

    # 2. Source relevance
    source_scores = [
        similarity(question, source)
        for source in sources
    ]

    source_relevance = percentage(
        sum(source_scores) / len(source_scores)
    )

    # 3. Grounding score
    grounding_scores = [
        similarity(answer, source)
        for source in sources
    ]

    grounding_score = percentage(
        sum(grounding_scores) / len(grounding_scores)
    )

    # 4. Citation coverage
    sentences = split_sentences(answer)

    supported_sentences = 0
    sentence_results = []

    for index, sentence in enumerate(sentences, start=1):

        score = similarity(
            sentence,
            combined_sources
        )

        score_percent = percentage(score)

        if score >= 0.25:
            status = "Supported"
            supported_sentences += 1
        else:
            status = "Potentially Unsupported"

        sentence_results.append({
            "sentence_number": index,
            "sentence": sentence,
            "support_score": score_percent,
            "status": status
        })

    if sentences:
        citation_coverage = percentage(
            supported_sentences / len(sentences)
        )
    else:
        citation_coverage = 0.0

    # Overall quality score
    quality_score = round(
        (
            answer_relevance
            + source_relevance
            + grounding_score
            + citation_coverage
        ) / 4,
        2
    )

    # Quality classification
    if quality_score >= 80:
        quality_level = "Excellent"
    elif quality_score >= 60:
        quality_level = "Good"
    elif quality_score >= 40:
        quality_level = "Needs Improvement"
    else:
        quality_level = "Poor"

    return {
        "question": question,
        "answer": answer,
        "metrics": {
            "answer_relevance": answer_relevance,
            "source_relevance": source_relevance,
            "grounding_score": grounding_score,
            "citation_coverage": citation_coverage
        },
        "quality_score": quality_score,
        "quality_level": quality_level,
        "total_sentences": len(sentences),
        "supported_sentences": supported_sentences,
        "sentence_results": sentence_results
    }
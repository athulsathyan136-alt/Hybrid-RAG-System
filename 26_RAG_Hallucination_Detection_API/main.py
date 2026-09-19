from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter
import math
import re


app = FastAPI(
    title="RAG Hallucination Detection API",
    description="Detect unsupported claims in RAG-generated answers.",
    version="1.0.0"
)


class HallucinationRequest(BaseModel):
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
        "project": "RAG Hallucination Detection API",
        "status": "running",
        "description": "Detect unsupported answer statements using source similarity."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "detection_method": "Lexical Cosine Similarity",
        "external_ml_dependencies": False
    }


@app.post("/detect")
def detect_hallucination(request: HallucinationRequest):

    answer = request.answer.strip()

    sources = [
        source.strip()
        for source in request.sources
        if source.strip()
    ]

    if not answer:
        return {
            "error": "Answer cannot be empty."
        }

    if not sources:
        return {
            "error": "At least one source is required."
        }

    sentences = split_sentences(answer)

    source_text = " ".join(sources)

    sentence_results = []

    supported_count = 0
    unsupported_count = 0

    for index, sentence in enumerate(sentences):

        score = similarity(
            sentence,
            source_text
        )

        score_percent = round(
            score * 100,
            2
        )

        if score >= 0.25:
            status = "Supported"
            supported_count += 1
        else:
            status = "Potentially Unsupported"
            unsupported_count += 1

        sentence_results.append(
            {
                "sentence_number": index + 1,
                "sentence": sentence,
                "support_score": score_percent,
                "status": status
            }
        )

    total_sentences = len(sentences)

    if total_sentences > 0:
        grounding_percentage = round(
            (supported_count / total_sentences) * 100,
            2
        )
    else:
        grounding_percentage = 0.0

    hallucination_percentage = round(
        100 - grounding_percentage,
        2
    )

    if hallucination_percentage <= 20:
        risk = "Low"
    elif hallucination_percentage <= 50:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "answer": answer,
        "total_sentences": total_sentences,
        "supported_sentences": supported_count,
        "unsupported_sentences": unsupported_count,
        "grounding_percentage": grounding_percentage,
        "hallucination_percentage": hallucination_percentage,
        "hallucination_risk": risk,
        "sentence_analysis": sentence_results
    }
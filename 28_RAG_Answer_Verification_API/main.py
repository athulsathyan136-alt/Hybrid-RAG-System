from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter
import math
import re


app = FastAPI(
    title="RAG Answer Verification API",
    description="Verify whether a RAG answer is supported by retrieved sources.",
    version="1.0.0"
)


class VerificationRequest(BaseModel):
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
        "project": "RAG Answer Verification API",
        "status": "running",
        "description": "Verify whether a RAG answer is supported by retrieved sources."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "verification_method": "Pure Python Similarity",
        "external_ml_dependencies": False
    }


@app.post("/verify")
def verify_answer(request: VerificationRequest):

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

    sentences = split_sentences(answer)

    verification_results = []

    supported_count = 0

    threshold = 0.25

    for index, sentence in enumerate(sentences, start=1):

        score = similarity(
            sentence,
            combined_sources
        )

        score_percent = percentage(score)

        if score >= threshold:
            status = "Supported"
            supported_count += 1
        else:
            status = "Potentially Unsupported"

        verification_results.append({
            "sentence_number": index,
            "sentence": sentence,
            "support_score": score_percent,
            "status": status
        })

    total_sentences = len(sentences)

    if total_sentences > 0:
        verification_percentage = round(
            (supported_count / total_sentences) * 100,
            2
        )
    else:
        verification_percentage = 0.0

    if verification_percentage >= 80:
        verification_status = "Verified"
    elif verification_percentage >= 50:
        verification_status = "Partially Verified"
    else:
        verification_status = "Not Verified"

    return {
        "question": question,
        "answer": answer,
        "verification_status": verification_status,
        "verification_percentage": verification_percentage,
        "total_sentences": total_sentences,
        "supported_sentences": supported_count,
        "threshold": 25.0,
        "sentence_results": verification_results
    }
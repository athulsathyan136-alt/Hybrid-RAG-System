from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, CrossEncoder
import numpy as np


# ============================================================
# RAG RE-RANKING API
# Project 22
# Author: Athul Sathyan
# B.Tech Computer Engineering
# ============================================================

app = FastAPI(
    title="RAG Re-Ranking API",
    description="Two-stage retrieval system using semantic search and cross-encoder re-ranking",
    version="1.0.0"
)


# ============================================================
# MODELS
# ============================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


print("Loading embedding model...")
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

print("Embedding model loaded!")

print("Loading re-ranking model...")
reranker = CrossEncoder(RERANK_MODEL)

print("Re-ranking model loaded!")


# ============================================================
# DEMO KNOWLEDGE BASE
# ============================================================

DOCUMENTS = [
    "Python is a popular programming language used for web development, automation, data science, and artificial intelligence.",
    "FastAPI is a modern Python framework used for building high-performance REST APIs.",
    "Machine learning allows computers to learn patterns from data without being explicitly programmed.",
    "Deep learning uses neural networks with multiple layers to learn complex patterns from large datasets.",
    "Natural language processing enables computers to understand and process human language.",
    "Docker packages applications and their dependencies into portable containers.",
    "AWS provides cloud computing services such as EC2, S3, Lambda, ECS, and EKS.",
    "Retrieval-Augmented Generation combines information retrieval with language generation to produce grounded answers.",
    "Vector databases store numerical embeddings and support semantic similarity search.",
    "MLOps combines machine learning development with deployment, monitoring, automation, and operations."
]


# ============================================================
# CREATE DOCUMENT EMBEDDINGS
# ============================================================

print("Creating document embeddings...")

document_embeddings = embedding_model.encode(
    DOCUMENTS,
    convert_to_numpy=True,
    normalize_embeddings=True
)

print(f"Created embeddings for {len(DOCUMENTS)} documents")


# ============================================================
# REQUEST MODEL
# ============================================================

class SearchRequest(BaseModel):
    question: str
    top_k: int = 3
    retrieval_k: int = 6


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "project": "RAG Re-Ranking API",
        "project_number": 22,
        "author": "Athul Sathyan",
        "status": "running",
        "description": "Two-stage RAG retrieval using semantic search and cross-encoder re-ranking"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "embedding_model": EMBEDDING_MODEL,
        "reranking_model": RERANK_MODEL,
        "documents": len(DOCUMENTS)
    }


# ============================================================
# DATABASE / KNOWLEDGE BASE INFO
# ============================================================

@app.get("/documents")
def documents():
    return {
        "total_documents": len(DOCUMENTS),
        "documents": DOCUMENTS
    }


# ============================================================
# TWO-STAGE SEARCH
# ============================================================

@app.post("/search")
def search(request: SearchRequest):

    question = request.question.strip()

    if not question:
        return {
            "error": "Question cannot be empty"
        }

    if request.top_k < 1:
        return {
            "error": "top_k must be at least 1"
        }

    if request.retrieval_k < request.top_k:
        retrieval_k = request.top_k
    else:
        retrieval_k = request.retrieval_k

    retrieval_k = min(retrieval_k, len(DOCUMENTS))

    # --------------------------------------------------------
    # STAGE 1 — VECTOR RETRIEVAL
    # --------------------------------------------------------

    query_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )[0]

    semantic_scores = np.dot(
        document_embeddings,
        query_embedding
    )

    initial_indices = np.argsort(
        semantic_scores
    )[::-1][:retrieval_k]

    initial_results = []

    for index in initial_indices:
        initial_results.append(
            {
                "document": DOCUMENTS[index],
                "semantic_score": float(semantic_scores[index])
            }
        )

    # --------------------------------------------------------
    # STAGE 2 — CROSS-ENCODER RE-RANKING
    # --------------------------------------------------------

    pairs = [
        [question, DOCUMENTS[index]]
        for index in initial_indices
    ]

    rerank_scores = reranker.predict(pairs)

    reranked_results = []

    for position, index in enumerate(initial_indices):

        reranked_results.append(
            {
                "document": DOCUMENTS[index],
                "semantic_score": float(
                    semantic_scores[index]
                ),
                "rerank_score": float(
                    rerank_scores[position]
                )
            }
        )

    # --------------------------------------------------------
    # SORT BY RE-RANKING SCORE
    # --------------------------------------------------------

    reranked_results.sort(
        key=lambda item: item["rerank_score"],
        reverse=True
    )

    final_results = reranked_results[:request.top_k]

    # Add final ranking
    for rank, result in enumerate(final_results, start=1):
        result["rank"] = rank

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "question": question,
        "retrieval_method": "Two-Stage Retrieval",
        "stage_1": {
            "method": "Semantic Similarity",
            "retrieved_documents": retrieval_k
        },
        "stage_2": {
            "method": "Cross-Encoder Re-Ranking",
            "reranking_model": RERANK_MODEL
        },
        "results": final_results,
        "total_results": len(final_results)
    }


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8011
    )
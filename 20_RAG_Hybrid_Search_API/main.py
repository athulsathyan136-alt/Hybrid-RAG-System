from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="RAG Hybrid Search API",
    description="Hybrid document retrieval using semantic and keyword search",
    version="1.0.0"
)


# ============================================================
# EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded!")


# ============================================================
# SAMPLE DOCUMENTS
# ============================================================

documents = [
    "Python is a popular programming language used for web development, automation, data science, and artificial intelligence.",

    "FastAPI is a modern Python framework used for building high-performance web APIs.",

    "Machine learning allows computers to learn patterns from data without being explicitly programmed.",

    "Deep learning uses neural networks with multiple layers to learn complex patterns from large datasets.",

    "Natural language processing allows computers to understand and process human language.",

    "Retrieval Augmented Generation combines document retrieval with language model generation.",

    "Vector databases store numerical embeddings and allow semantic similarity searches.",

    "Docker is a platform used to package applications and their dependencies into containers.",

    "AWS provides cloud services such as EC2, S3, Lambda, ECS, and EKS.",

    "MLOps combines machine learning, software engineering, automation, and operations."
]


# ============================================================
# CREATE DOCUMENT EMBEDDINGS
# ============================================================

print("Creating document embeddings...")

document_embeddings = model.encode(
    documents,
    convert_to_numpy=True
)

print(f"Created {len(documents)} document embeddings.")


# ============================================================
# TF-IDF KEYWORD SEARCH
# ============================================================

print("Creating keyword search index...")

tfidf_vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

print("Keyword search index created!")


# ============================================================
# REQUEST MODEL
# ============================================================

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


# ============================================================
# HOME ENDPOINT
# ============================================================

@app.get("/")
def home():
    return {
        "message": "RAG Hybrid Search API is running",
        "documents": len(documents),
        "search_methods": [
            "Semantic Search",
            "Keyword Search",
            "Hybrid Search"
        ]
    }


# ============================================================
# DOCUMENT ENDPOINT
# ============================================================

@app.get("/documents")
def get_documents():
    return {
        "total_documents": len(documents),
        "documents": documents
    }


# ============================================================
# HYBRID SEARCH
# ============================================================

@app.post("/search")
def hybrid_search(request: SearchRequest):

    query = request.query

    if not query.strip():
        return {
            "query": query,
            "results": []
        }

    top_k = max(1, min(request.top_k, len(documents)))

    # --------------------------------------------------------
    # 1. SEMANTIC SEARCH
    # --------------------------------------------------------

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    semantic_scores = cosine_similarity(
        query_embedding,
        document_embeddings
    )[0]

    # --------------------------------------------------------
    # 2. KEYWORD SEARCH
    # --------------------------------------------------------

    query_tfidf = tfidf_vectorizer.transform([query])

    keyword_scores = cosine_similarity(
        query_tfidf,
        tfidf_matrix
    )[0]

    # --------------------------------------------------------
    # 3. NORMALIZE SCORES
    # --------------------------------------------------------

    def normalize(scores):

        minimum = np.min(scores)
        maximum = np.max(scores)

        if maximum - minimum == 0:
            return np.zeros_like(scores)

        return (scores - minimum) / (maximum - minimum)


    normalized_semantic = normalize(semantic_scores)
    normalized_keyword = normalize(keyword_scores)

    # --------------------------------------------------------
    # 4. HYBRID SCORE
    # --------------------------------------------------------

    semantic_weight = 0.7
    keyword_weight = 0.3

    hybrid_scores = (
        semantic_weight * normalized_semantic
        +
        keyword_weight * normalized_keyword
    )

    # --------------------------------------------------------
    # 5. SORT RESULTS
    # --------------------------------------------------------

    ranked_indices = np.argsort(
        hybrid_scores
    )[::-1][:top_k]

    results = []

    for index in ranked_indices:

        results.append({
            "document": documents[index],
            "semantic_score": round(
                float(normalized_semantic[index]),
                4
            ),
            "keyword_score": round(
                float(normalized_keyword[index]),
                4
            ),
            "hybrid_score": round(
                float(hybrid_scores[index]),
                4
            )
        })

    return {
        "query": query,
        "semantic_weight": semantic_weight,
        "keyword_weight": keyword_weight,
        "results": results
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model": "all-MiniLM-L6-v2",
        "documents": len(documents),
        "keyword_index": "TF-IDF",
        "semantic_search": "Sentence Transformers",
        "hybrid_search": "Enabled"
    }
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = FastAPI(
    title="RAG Multi-Query Search API",
    description="Multi-query retrieval API for RAG systems",
    version="1.0.0"
)

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "Python is a popular programming language used for web development, automation, data science, and artificial intelligence.",
    "FastAPI is a modern Python framework for building high-performance APIs.",
    "Machine learning allows computers to learn patterns from data without being explicitly programmed.",
    "Deep learning uses neural networks with multiple layers to learn complex patterns from large datasets.",
    "Retrieval Augmented Generation combines document retrieval with language models to generate grounded answers.",
    "Vector databases store numerical embeddings and allow fast similarity search.",
    "Docker packages applications and their dependencies into portable containers.",
    "AWS provides cloud services such as EC2, S3, Lambda, ECS, and EKS.",
    "MLOps combines machine learning development with DevOps practices for reliable model deployment.",
    "Natural language processing enables computers to understand and process human language."
]

document_embeddings = model.encode(documents)


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


def generate_queries(question: str):
    question = question.strip()

    return [
        question,
        f"Explain {question}",
        f"Give information about {question}",
        f"What are the main uses and applications of {question}?"
    ]

def search(query: str, top_k: int):
    query_embedding = model.encode([query])

    scores = cosine_similarity(
        query_embedding,
        document_embeddings
    )[0]

    ranked_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in ranked_indices:
        results.append({
            "document": documents[index],
            "score": float(scores[index])
        })

    return results


@app.get("/")
def home():
    return {
        "message": "RAG Multi-Query Search API is running",
        "documents": len(documents),
        "model": "all-MiniLM-L6-v2",
        "search_type": "Multi-Query Semantic Search"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "documents": len(documents),
        "embedding_model": "all-MiniLM-L6-v2"
    }


@app.post("/search")
def multi_query_search(request: QueryRequest):

    queries = generate_queries(request.question)

    combined_results = {}

    for query in queries:

        results = search(
            query,
            request.top_k
        )

        for result in results:

            document = result["document"]
            score = result["score"]

            if document not in combined_results:
                combined_results[document] = {
                    "document": document,
                    "best_score": score,
                    "matched_queries": [query]
                }

            else:

                if score > combined_results[document]["best_score"]:
                    combined_results[document]["best_score"] = score

                combined_results[document]["matched_queries"].append(query)

    final_results = sorted(
        combined_results.values(),
        key=lambda x: x["best_score"],
        reverse=True
    )

    final_results = final_results[:request.top_k]

    return {
        "question": request.question,
        "generated_queries": queries,
        "total_queries": len(queries),
        "results": final_results
    }
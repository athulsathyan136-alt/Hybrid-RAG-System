from fastapi import FastAPI
from pydantic import BaseModel

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

import faiss
import torch


app = FastAPI(
    title="RAG Answer Generator API",
    description="RAG API with semantic retrieval and AI answer generation",
    version="1.0.0"
)


# ==========================================
# EMBEDDING MODEL
# ==========================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded!")


# ==========================================
# ANSWER GENERATION MODEL
# ==========================================

MODEL_NAME = "google/flan-t5-small"

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

print("Loading answer generation model...")

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)

print("Answer generation model loaded!")


# ==========================================
# SAMPLE KNOWLEDGE BASE
# ==========================================

documents = [
    {
        "id": 1,
        "text": (
            "Python is a high-level programming language known "
            "for its simple syntax and readability. Python is widely "
            "used in artificial intelligence, machine learning, web "
            "development, automation, and data science."
        )
    },
    {
        "id": 2,
        "text": (
            "Machine learning is a branch of artificial intelligence "
            "that allows computers to learn patterns from data and "
            "make predictions without being explicitly programmed."
        )
    },
    {
        "id": 3,
        "text": (
            "FastAPI is a modern Python framework used for building "
            "high-performance APIs. It supports automatic validation "
            "and interactive API documentation."
        )
    },
    {
        "id": 4,
        "text": (
            "FAISS is a vector similarity search library developed "
            "by Meta. It is commonly used in RAG applications to "
            "search embeddings and retrieve relevant documents."
        )
    },
    {
        "id": 5,
        "text": (
            "Retrieval-Augmented Generation combines document retrieval "
            "with a language model. Relevant documents are retrieved "
            "first and then provided as context to generate an answer."
        )
    }
]


# ==========================================
# CREATE DOCUMENT EMBEDDINGS
# ==========================================

document_texts = [
    document["text"]
    for document in documents
]

print("Creating document embeddings...")

document_embeddings = embedding_model.encode(
    document_texts,
    convert_to_numpy=True
).astype("float32")


# ==========================================
# CREATE FAISS INDEX
# ==========================================

embedding_dimension = document_embeddings.shape[1]

vector_index = faiss.IndexFlatL2(
    embedding_dimension
)

vector_index.add(document_embeddings)

print(
    f"FAISS index created with {len(documents)} documents"
)


# ==========================================
# REQUEST MODEL
# ==========================================

class QuestionRequest(BaseModel):
    question: str
    top_k: int = 3


# ==========================================
# HOME ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "RAG Answer Generator API is running",
        "total_documents": len(documents),
        "generation_model": MODEL_NAME
    }


# ==========================================
# RETRIEVE DOCUMENTS
# ==========================================

def retrieve_documents(question, top_k):

    top_k = min(top_k, len(documents))

    question_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = vector_index.search(
        question_embedding,
        top_k
    )

    results = []

    for distance, index in zip(
        distances[0],
        indices[0]
    ):

        if index == -1:
            continue

        results.append({
            "document": documents[index]["text"],
            "distance": float(distance)
        })

    return results


# ==========================================
# GENERATE ANSWER
# ==========================================

def generate_answer(question, context):

    prompt = (
        "Answer the question using only the provided context.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():

        output_ids = model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=False
        )

    answer = tokenizer.decode(
        output_ids[0],
        skip_special_tokens=True
    )

    return answer


# ==========================================
# RAG QUESTION ENDPOINT
# ==========================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    retrieved_documents = retrieve_documents(
        request.question,
        request.top_k
    )

    context = "\n\n".join(
        item["document"]
        for item in retrieved_documents
    )

    answer = generate_answer(
        request.question,
        context
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": retrieved_documents,
        "total_sources": len(retrieved_documents)
    }


# ==========================================
# RETRIEVAL ONLY ENDPOINT
# ==========================================

@app.post("/search")
def search_documents(request: QuestionRequest):

    results = retrieve_documents(
        request.question,
        request.top_k
    )

    return {
        "question": request.question,
        "results": results,
        "total_results": len(results)
    }


# ==========================================
# LIST DOCUMENTS
# ==========================================

@app.get("/documents")
def get_documents():

    return {
        "documents": documents,
        "total_documents": len(documents)
    }
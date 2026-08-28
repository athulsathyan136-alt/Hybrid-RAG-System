from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="RAG Chat API",
    description="Day 7 - Retrieval Augmented Generation Chat API",
    version="1.0.0"
)


# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded!")


# ==========================================
# KNOWLEDGE BASE
# ==========================================

documents = [
    "Python is a popular programming language used for software development.",

    "Python is widely used in artificial intelligence and machine learning.",

    "Machine learning allows computers to learn patterns from data.",

    "Deep learning uses neural networks to solve complex problems.",

    "FastAPI is a Python framework used for building high-performance APIs.",

    "Docker packages applications into lightweight containers.",

    "AWS provides cloud computing services such as EC2, S3, Lambda, and ECS.",

    "Amazon S3 is an object storage service used to store files and data.",

    "Amazon EC2 provides virtual servers in the cloud.",

    "GitHub is a platform used to store and manage source code.",

    "Git is a version control system used to track changes in code.",

    "RAG combines information retrieval with large language models.",

    "Vector databases store numerical representations of text.",

    "FAISS is a library used for efficient similarity search.",

    "MLOps combines machine learning with software engineering and operations."
]


# ==========================================
# CREATE DOCUMENT EMBEDDINGS
# ==========================================

print("Creating document embeddings...")

document_embeddings = embedding_model.encode(
    documents
)

document_embeddings = np.array(
    document_embeddings
).astype("float32")

print("Document embeddings created!")


# ==========================================
# CREATE FAISS INDEX
# ==========================================

dimension = document_embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(document_embeddings)

print(
    f"FAISS index contains {index.ntotal} documents."
)


# ==========================================
# LOAD FLAN-T5 MODEL
# ==========================================

print("Loading language model...")

model_name = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(
    model_name
)

language_model = AutoModelForSeq2SeqLM.from_pretrained(
    model_name
)

print("Language model loaded!")


# ==========================================
# REQUEST MODEL
# ==========================================

class ChatRequest(BaseModel):

    question: str


# ==========================================
# RETRIEVE DOCUMENTS
# ==========================================

def retrieve_documents(
    query: str,
    top_k: int = 3
):

    query_embedding = embedding_model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, index_number in zip(
        distances[0],
        indices[0]
    ):

        results.append({
            "text": documents[index_number],
            "distance": float(distance)
        })

    return results


# ==========================================
# GENERATE ANSWER
# ==========================================

def generate_answer(
    question: str,
    retrieved_documents: list
):

    context = "\n".join(
        document["text"]
        for document in retrieved_documents
    )

    prompt = f"""
Answer the question using only the information
provided in the context.

Context:
{context}

Question:
{question}

Answer:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = language_model.generate(
        **inputs,
        max_new_tokens=100
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return answer


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "RAG Chat API is running!",
        "version": "1.0.0",
        "endpoint": "/chat"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "documents": index.ntotal,
        "embedding_model": "all-MiniLM-L6-v2",
        "language_model": "google/flan-t5-small"
    }


# ==========================================
# CHAT ENDPOINT
# ==========================================

@app.post("/chat")
def chat(request: ChatRequest):

    question = request.question

    # Search relevant documents
    retrieved_documents = retrieve_documents(
        question,
        top_k=3
    )

    # Generate answer
    answer = generate_answer(
        question,
        retrieved_documents
    )

    # Return sources
    sources = []

    for document in retrieved_documents:

        sources.append({
            "text": document["text"],
            "distance": document["distance"]
        })

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }
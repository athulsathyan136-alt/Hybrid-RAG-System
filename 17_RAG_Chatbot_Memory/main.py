from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = FastAPI(
    title="RAG Chatbot with Conversation Memory",
    description="A RAG chatbot that remembers previous conversations.",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    question: str
    top_k: int = 3


embedding_model = None
tokenizer = None
generation_model = None

documents = [
    "Python is a popular programming language used for web development, automation, data science, and artificial intelligence.",
    "Machine learning allows computers to learn patterns from data without being explicitly programmed.",
    "Retrieval-Augmented Generation combines information retrieval with language models to generate accurate answers.",
    "FAISS is a library for efficient similarity search and clustering of dense vectors.",
    "FastAPI is a modern Python framework for building high-performance APIs."
]

conversation_memory = []


@app.on_event("startup")
def load_models():
    global embedding_model
    global tokenizer
    global generation_model
    global document_embeddings
    global index

    print("Loading embedding model...")

    embedding_model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Embedding model loaded!")

    print("Loading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        "google/flan-t5-small"
    )

    print("Loading answer generation model...")

    generation_model = AutoModelForSeq2SeqLM.from_pretrained(
        "google/flan-t5-small"
    )

    print("Answer generation model loaded!")

    print("Creating document embeddings...")

    document_embeddings = embedding_model.encode(
        documents,
        convert_to_numpy=True
    )

    document_embeddings = np.array(
        document_embeddings
    ).astype("float32")

    dimension = document_embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(document_embeddings)

    print(
        f"FAISS index created with {len(documents)} documents"
    )


@app.get("/")
def home():
    return {
        "message": "RAG Chatbot with Conversation Memory is running",
        "total_documents": len(documents),
        "memory_messages": len(conversation_memory)
    }


@app.post("/chat")
def chat(request: ChatRequest):

    if embedding_model is None:
        raise HTTPException(
            status_code=500,
            detail="Models are not loaded yet"
        )

    question_embedding = embedding_model.encode(
        [request.question],
        convert_to_numpy=True
    )

    question_embedding = np.array(
        question_embedding
    ).astype("float32")

    distances, indices = index.search(
        question_embedding,
        request.top_k
    )

    retrieved_documents = []

    for i, distance in zip(
        indices[0],
        distances[0]
    ):

        if i < len(documents):

            retrieved_documents.append({
                "document": documents[i],
                "distance": float(distance)
            })

    context = "\n".join(
        item["document"]
        for item in retrieved_documents
    )

    recent_memory = conversation_memory[-6:]

    memory_context = "\n".join(
        f"{item['role']}: {item['message']}"
        for item in recent_memory
    )

    prompt = f"""
You are a helpful AI assistant.

Conversation History:
{memory_context}

Context:
{context}

Question:
{request.question}

Answer the question using the context and conversation history.
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    output = generation_model.generate(
        **inputs,
        max_new_tokens=100
    )

    answer = tokenizer.decode(
        output[0],
        skip_special_tokens=True
    )

    conversation_memory.append({
        "role": "user",
        "message": request.question
    })

    conversation_memory.append({
        "role": "assistant",
        "message": answer
    })

    return {
        "question": request.question,
        "answer": answer,
        "sources": retrieved_documents,
        "memory_messages": len(conversation_memory)
    }


@app.get("/memory")
def get_memory():

    return {
        "conversation": conversation_memory,
        "total_messages": len(conversation_memory)
    }


@app.delete("/memory")
def clear_memory():

    conversation_memory.clear()

    return {
        "message": "Conversation memory cleared successfully"
    }


@app.get("/documents")
def get_documents():

    return {
        "documents": documents,
        "total_documents": len(documents)
    }
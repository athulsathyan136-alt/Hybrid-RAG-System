from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import faiss
import numpy as np

from database import Conversation, create_database, get_db


app = FastAPI(
    title="Persistent RAG Chatbot with SQLite",
    description="RAG chatbot with persistent conversation memory",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    conversation_id: str
    question: str
    top_k: int = 3


embedding_model = None
tokenizer = None
generation_model = None
index = None


documents = [
    "Python is a popular programming language used for web development, automation, data science, and artificial intelligence.",
    "Machine learning allows computers to learn patterns from data without being explicitly programmed.",
    "Retrieval-Augmented Generation combines information retrieval with language models to generate accurate answers.",
    "FAISS is a library for efficient similarity search and clustering of dense vectors.",
    "FastAPI is a modern Python framework for building high-performance APIs."
]


@app.on_event("startup")
def startup_event():

    global embedding_model
    global tokenizer
    global generation_model
    global index

    print("Creating database...")
    create_database()

    print("Loading embedding model...")

    embedding_model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Embedding model loaded!")

    print("Loading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        "google/flan-t5-small"
    )

    print("Loading generation model...")

    generation_model = AutoModelForSeq2SeqLM.from_pretrained(
        "google/flan-t5-small"
    )

    print("Generation model loaded!")

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
        "message": "Persistent RAG Chatbot with SQLite is running",
        "total_documents": len(documents)
    }


@app.post("/chat")
def chat(request: ChatRequest):

    db = next(get_db())

    try:

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

        history = db.query(Conversation).filter(
            Conversation.conversation_id == request.conversation_id
        ).order_by(
            Conversation.created_at
        ).all()

        memory_context = "\n".join(
            f"{item.role}: {item.message}"
            for item in history[-6:]
        )

        prompt = f"""
You are a helpful AI assistant.

Conversation History:
{memory_context}

Context:
{context}

Question:
{request.question}

Answer the question clearly using the provided context.
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

        user_message = Conversation(
            conversation_id=request.conversation_id,
            role="user",
            message=request.question
        )

        assistant_message = Conversation(
            conversation_id=request.conversation_id,
            role="assistant",
            message=answer
        )

        db.add(user_message)
        db.add(assistant_message)

        db.commit()

        return {
            "conversation_id": request.conversation_id,
            "question": request.question,
            "answer": answer,
            "sources": retrieved_documents
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:

        db.close()


@app.get("/history/{conversation_id}")
def get_history(conversation_id: str):

    db = next(get_db())

    try:

        history = db.query(Conversation).filter(
            Conversation.conversation_id == conversation_id
        ).order_by(
            Conversation.created_at
        ).all()

        return {
            "conversation_id": conversation_id,
            "messages": [
                {
                    "id": item.id,
                    "role": item.role,
                    "message": item.message,
                    "created_at": item.created_at
                }
                for item in history
            ],
            "total_messages": len(history)
        }

    finally:

        db.close()


@app.delete("/history/{conversation_id}")
def delete_history(conversation_id: str):

    db = next(get_db())

    try:

        deleted = db.query(Conversation).filter(
            Conversation.conversation_id == conversation_id
        ).delete()

        db.commit()

        return {
            "message": "Conversation deleted successfully",
            "conversation_id": conversation_id,
            "deleted_messages": deleted
        }

    finally:

        db.close()


@app.get("/conversations")
def get_conversations():

    db = next(get_db())

    try:

        conversations = db.query(
            Conversation.conversation_id
        ).distinct().all()

        return {
            "conversations": [
                item[0]
                for item in conversations
            ],
            "total_conversations": len(conversations)
        }

    finally:

        db.close()


@app.get("/documents")
def get_documents():

    return {
        "documents": documents,
        "total_documents": len(documents)
    }
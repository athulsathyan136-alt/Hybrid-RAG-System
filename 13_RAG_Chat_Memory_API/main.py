from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="RAG Chat Memory API",
    description="A RAG chatbot API with conversation memory",
    version="1.0.0"
)


# ==========================================
# RAG API CONFIGURATION
# ==========================================

RAG_API_URL = "http://127.0.0.1:8000/query"


# ==========================================
# REQUEST MODEL
# ==========================================

class ChatRequest(BaseModel):
    question: str


# ==========================================
# CONVERSATION MEMORY
# ==========================================

conversation_memory = []


# ==========================================
# HOME ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "RAG Chat Memory API is running"
    }


# ==========================================
# CHAT ENDPOINT
# ==========================================

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        # Send question to Project 12 RAG API
        response = requests.post(
            RAG_API_URL,
            json={
                "question": request.question
            },
            timeout=30
        )

        # Check API response
        response.raise_for_status()

        rag_response = response.json()

        # Get answer from RAG API
        answer = rag_response.get(
            "answer",
            "No answer received from RAG system."
        )

    except requests.exceptions.RequestException as error:

        raise HTTPException(
            status_code=500,
            detail=f"RAG API connection failed: {str(error)}"
        )

    # Save user message
    conversation_memory.append({
        "role": "user",
        "message": request.question
    })

    # Save assistant answer
    conversation_memory.append({
        "role": "assistant",
        "message": answer
    })

    # Return response
    return {
        "question": request.question,
        "answer": answer,
        "memory_messages": len(conversation_memory)
    }


# ==========================================
# GET CONVERSATION HISTORY
# ==========================================

@app.get("/history")
def get_history():

    return {
        "conversation": conversation_memory,
        "total_messages": len(conversation_memory)
    }


# ==========================================
# CLEAR CONVERSATION MEMORY
# ==========================================

@app.delete("/history")
def clear_history():

    conversation_memory.clear()

    return {
        "message": "Conversation memory cleared"
    }
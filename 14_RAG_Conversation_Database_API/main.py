from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import requests

from database import engine, get_db
from models import Base, Conversation
from schemas import QuestionRequest


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

Base.metadata.create_all(bind=engine)


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="RAG Conversation Database API",
    description="Store RAG conversations permanently using SQLite.",
    version="1.0.0"
)


# ==========================================
# PROJECT 12 URL
# ==========================================

RAG_QUERY_API = "http://127.0.0.1:8000/query"


# ==========================================
# HOME ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "RAG Conversation Database API is running",
        "database": "SQLite",
        "rag_backend": RAG_QUERY_API
    }


# ==========================================
# CHAT ENDPOINT
# ==========================================

@app.post("/chat")
def chat(
    request: QuestionRequest,
    db: Session = Depends(get_db)
):

    try:

        # Send question to Project 12

        response = requests.post(
            RAG_QUERY_API,
            json={
                "question": request.question
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get(
            "answer",
            "No answer received from RAG system."
        )


    except requests.exceptions.RequestException as error:

        raise HTTPException(
            status_code=500,
            detail=f"Could not connect to RAG system: {str(error)}"
        )


    # ==========================================
    # SAVE USER QUESTION
    # ==========================================

    user_message = Conversation(

        role="user",

        message=request.question
    )

    db.add(user_message)


    # ==========================================
    # SAVE AI ANSWER
    # ==========================================

    assistant_message = Conversation(

        role="assistant",

        message=answer
    )

    db.add(assistant_message)


    # Save to database

    db.commit()


    # Refresh database objects

    db.refresh(user_message)

    db.refresh(assistant_message)


    # Return response

    return {

        "question": request.question,

        "answer": answer,

        "user_message_id": user_message.id,

        "assistant_message_id": assistant_message.id
    }


# ==========================================
# GET CONVERSATION HISTORY
# ==========================================

@app.get("/history")
def get_history(
    db: Session = Depends(get_db)
):

    conversations = db.query(
        Conversation
    ).order_by(
        Conversation.id
    ).all()


    return {

        "conversation": conversations,

        "total_messages": len(conversations)
    }


# ==========================================
# CLEAR CONVERSATION HISTORY
# ==========================================

@app.delete("/history")
def clear_history(
    db: Session = Depends(get_db)
):

    db.query(
        Conversation
    ).delete()

    db.commit()


    return {

        "message": "Conversation history deleted from database"
    }
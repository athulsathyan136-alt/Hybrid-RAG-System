from fastapi import FastAPI
from pydantic import BaseModel
import requests


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="RAG Query API",
    description="Query API connected to the RAG Document Upload API.",
    version="1.0.0"
)


# ==========================================
# PROJECT 11 API
# ==========================================

PROJECT_11_URL = "http://127.0.0.1:8001"


# ==========================================
# REQUEST MODEL
# ==========================================

class QueryRequest(BaseModel):

    question: str


# ==========================================
# HOME ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "RAG Query API is running",
        "backend": PROJECT_11_URL
    }


# ==========================================
# QUERY ENDPOINT
# ==========================================

@app.post("/query")
def query(request: QueryRequest):

    question = request.question.strip()

    if not question:

        return {
            "error": "Question cannot be empty"
        }

    try:

        response = requests.post(
            f"{PROJECT_11_URL}/ask",
            json={
                "question": question
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        return {
            "question": question,
            "answer": result.get(
                "answer",
                "No answer returned."
            )
        }

    except requests.exceptions.ConnectionError:

        return {
            "error": "Could not connect to Project 11 RAG API.",
            "backend": PROJECT_11_URL
        }

    except requests.exceptions.Timeout:

        return {
            "error": "Request timed out while waiting for the RAG API."
        }

    except requests.exceptions.HTTPError as error:

        return {
            "error": "Project 11 returned an HTTP error.",
            "details": str(error)
        }

    except Exception as error:

        return {
            "error": "Unexpected error.",
            "details": str(error)
        }
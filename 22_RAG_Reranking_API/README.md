# Project 22 — RAG Re-Ranking API

## Author

Athul Sathyan  
B.Tech Computer Engineering

## Overview

This project implements a Two-Stage Retrieval-Augmented Generation (RAG) retrieval system using semantic similarity search followed by Cross-Encoder re-ranking.

The system first retrieves candidate documents using vector embeddings and then uses a Cross-Encoder model to calculate a more detailed relevance score and produce the final ranking.

## Architecture

User Question
↓
Sentence Transformer Embedding
↓
Semantic Similarity Search
↓
Retrieve Candidate Documents
↓
Cross-Encoder Re-Ranking
↓
Final Top-K Results

## Technologies

- Python 3.13
- FastAPI
- Uvicorn
- Sentence Transformers
- Cross-Encoder
- PyTorch
- NumPy
- REST API
- Semantic Search
- RAG
- Information Retrieval

## AI Models

### Embedding Model

sentence-transformers/all-MiniLM-L6-v2

This model converts questions and documents into numerical vector embeddings for semantic similarity search.

### Re-Ranking Model

cross-encoder/ms-marco-MiniLM-L-6-v2

This model compares the question and retrieved documents together and produces relevance scores for re-ranking.

## Project Structure

22_RAG_Reranking_API/
│
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
└── venv/

## Installation

Open PowerShell and navigate to the project:

cd C:\Users\LENOVO\Hybrid-RAG-System\22_RAG_Reranking_API

Create the Python 3.13 virtual environment:

py -3.13 -m venv venv

Upgrade pip:

.\venv\Scripts\python.exe -m pip install --upgrade pip

Install dependencies:

.\venv\Scripts\python.exe -m pip install -r requirements.txt

## Requirements

The project requires:

fastapi
uvicorn
sentence-transformers
torch
numpy

## Run the Application

PowerShell activation is not required.

Start the FastAPI server:

.\venv\Scripts\python.exe -m uvicorn main:app --port 8011

The API will be available at:

http://127.0.0.1:8011

## Swagger Documentation

Open the following URL in your browser:

http://127.0.0.1:8011/docs

Swagger provides an interactive interface for testing the API endpoints.

## API Endpoints

### GET /

Returns basic information about the application.

### GET /health

Checks whether the API and AI models are running correctly.

### GET /documents

Returns the documents available in the demonstration knowledge base.

### POST /search

Performs two-stage retrieval using semantic search and Cross-Encoder re-ranking.

## Search Request

Example request:

{
  "question": "What is Python used for?",
  "top_k": 3,
  "retrieval_k": 6
}

### Parameters

question

The user's search question.

top_k

The number of final documents returned after re-ranking.

retrieval_k

The number of candidate documents retrieved during the first semantic search stage.

## PowerShell Test

After starting the API, open another PowerShell window and run:

Invoke-RestMethod `
  -Uri http://127.0.0.1:8011/search `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"question":"What is Python used for?","top_k":3,"retrieval_k":6}' |
  ConvertTo-Json -Depth 10

## Tested Result

The API was successfully tested with:

Question:

What is Python used for?

Retrieval Method:

Two-Stage Retrieval

Stage 1:

Semantic Similarity

Retrieved Documents:

6

Stage 2:

Cross-Encoder Re-Ranking

Re-Ranking Model:

cross-encoder/ms-marco-MiniLM-L-6-v2

Final Results:

3

## Example Result

Rank 1:

Python is a popular programming language used for web development, automation, data science, and artificial intelligence.

Semantic Score:

0.8261523842811584

Re-Rank Score:

9.850030899047852

Rank 2:

FastAPI is a modern Python framework used for building high-performance REST APIs.

Semantic Score:

0.47834357619285583

Re-Rank Score:

3.620431900024414

Rank 3:

Natural language processing enables computers to understand and process human language.

Semantic Score:

0.3124847412109375

Re-Rank Score:

-8.72563362121582

## Example API Response

{
  "question": "What is Python used for?",
  "retrieval_method": "Two-Stage Retrieval",
  "stage_1": {
    "method": "Semantic Similarity",
    "retrieved_documents": 6
  },
  "stage_2": {
    "method": "Cross-Encoder Re-Ranking",
    "reranking_model": "cross-encoder/ms-marco-MiniLM-L-6-v2"
  },
  "results": [
    {
      "document": "Python is a popular programming language used for web development, automation, data science, and artificial intelligence.",
      "semantic_score": 0.8261523842811584,
      "rerank_score": 9.850030899047852,
      "rank": 1
    },
    {
      "document": "FastAPI is a modern Python framework used for building high-performance REST APIs.",
      "semantic_score": 0.47834357619285583,
      "rerank_score": 3.620431900024414,
      "rank": 2
    },
    {
      "document": "Natural language processing enables computers to understand and process human language.",
      "semantic_score": 0.3124847412109375,
      "rerank_score": -8.72563362121582,
      "rank": 3
    }
  ],
  "total_results": 3
}

## How the System Works

The system uses two retrieval stages.

Stage 1 — Semantic Similarity

The user's question is converted into an embedding using the Sentence Transformer model.

The system compares the question embedding with the document embeddings and retrieves the most semantically similar candidate documents.

Stage 2 — Cross-Encoder Re-Ranking

The retrieved documents are then passed together with the original question to the Cross-Encoder.

The Cross-Encoder calculates a relevance score for every question-document pair.

The documents are sorted according to the re-ranking scores.

## Why Re-Ranking Is Useful

Semantic search is very effective for quickly finding candidate documents, but the initial similarity ranking may not always represent the best final relevance order.

Cross-Encoder re-ranking provides a second, more detailed relevance evaluation.

This creates a practical retrieval pipeline:

Large Document Collection
↓
Fast Semantic Search
↓
Small Candidate Set
↓
Cross-Encoder
↓
Accurate Final Ranking

## Semantic Search

Semantic search uses embeddings to understand the meaning of text.

Example:

Question:

What is Python used for?

The system can retrieve documents related to Python even when the wording is not exactly the same.

## Cross-Encoder Re-Ranking

The Cross-Encoder evaluates the question and document together.

Example:

Question + Document
↓
Cross-Encoder
↓
Relevance Score

Higher relevance scores generally indicate stronger relevance to the query.

## Two-Stage Retrieval

The main concept demonstrated by this project is:

Stage 1:

Semantic Retrieval

Stage 2:

Cross-Encoder Re-Ranking

This approach is commonly useful in modern search and RAG systems because the expensive re-ranking model only needs to evaluate a smaller candidate set.

## Benefits

- Better document ranking
- Improved retrieval relevance
- Combines fast retrieval with detailed scoring
- Suitable for RAG applications
- Demonstrates modern information retrieval
- Provides a foundation for production RAG systems

## Knowledge Base

The demonstration knowledge base contains information related to:

- Python
- FastAPI
- Machine Learning
- Deep Learning
- Natural Language Processing
- Docker
- AWS
- RAG
- Vector Databases
- MLOps

## Troubleshooting

### PowerShell Activation Error

If you receive:

running scripts is disabled on this system

when using:

.\venv\Scripts\Activate.ps1

you do not need to activate the virtual environment.

Run Python directly:

.\venv\Scripts\python.exe -m uvicorn main:app --port 8011

### Port Error

If port 8011 is already being used, check it with:

netstat -ano | findstr :8011

You can use another port:

.\venv\Scripts\python.exe -m uvicorn main:app --port 8012

Then open:

http://127.0.0.1:8012/docs

### Hugging Face Warning

You may see a message saying:

Warning: You are sending unauthenticated requests to the HF Hub.

This is a Hugging Face authentication/rate-limit warning.

If the models successfully download and the server starts, the warning does not mean that the application has failed.

## .gitignore

The project should not upload the virtual environment or temporary Python files.

Recommended .gitignore:

venv/
__pycache__/
*.pyc
.env
.vscode/

## Files

### main.py

Contains the FastAPI application, embedding model, semantic retrieval, Cross-Encoder model, re-ranking logic, knowledge base, and API endpoints.

### requirements.txt

Contains the Python packages required to run the project.

### .gitignore

Prevents unnecessary local files from being uploaded to GitHub.

### README.md

Contains the complete project documentation.

## Skills Demonstrated

This project demonstrates:

- Python
- FastAPI
- REST APIs
- Sentence Transformers
- Vector Embeddings
- Semantic Search
- Cross-Encoder Models
- Re-Ranking
- Information Retrieval
- RAG Architecture
- Two-Stage Retrieval
- AI Engineering
- API Testing
- Virtual Environments
- Git
- GitHub

## RAG Learning Progression

This project continues the RAG development path:

Text Extraction
↓
Text Chunking
↓
Embedding Generation
↓
Vector Search
↓
RAG Pipeline
↓
Persistent Storage
↓
ChromaDB
↓
Hybrid Search
↓
Multi-Query Search
↓
Re-Ranking

Project 22 adds Cross-Encoder re-ranking to improve the quality of retrieved results.

## Future Improvements

Future versions can include:

- PDF document upload
- FAISS vector database
- ChromaDB integration
- Persistent document storage
- Multi-query generation
- Hybrid retrieval
- LLM answer generation
- Source citations
- Conversation memory
- Authentication
- Docker deployment
- AWS deployment
- CI/CD
- Monitoring
- MLOps
- Production document ingestion

## Project Status

Project Number: 22

Project Name: RAG Re-Ranking API

Status: Completed

FastAPI: Completed

Semantic Retrieval: Completed

Cross-Encoder Re-Ranking: Completed

Two-Stage Retrieval: Completed

REST API: Completed

Swagger Documentation: Completed

Testing: Successful

GitHub Ready: Yes

## Conclusion

Project 22 demonstrates how a modern RAG retrieval system can combine fast semantic search with Cross-Encoder re-ranking.

Instead of relying only on embedding similarity, the system uses:

Semantic Search
+
Cross-Encoder Re-Ranking
=
Improved Retrieval Ranking

This project provides practical experience with an important technique used in modern AI search, enterprise RAG, knowledge assistants, and AI engineering systems.

## Author

Athul Sathyan

B.Tech Computer Engineering

AI/ML Engineer | GenAI | RAG | Cloud | MLOps
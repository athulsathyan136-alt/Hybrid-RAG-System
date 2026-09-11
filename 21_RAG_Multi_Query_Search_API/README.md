# Project 21 — RAG Multi-Query Search API

**Author:** Athul Sathyan  
**Degree:** B.Tech Computer Engineering  
**Project:** Hybrid-RAG-System  
**Project Number:** 21  
**Status:** Completed ✅

## Overview

RAG Multi-Query Search API is an advanced Retrieval-Augmented Generation (RAG) retrieval project built with Python and FastAPI.

The system takes a user's question, generates multiple related search queries, converts the queries into embeddings, performs semantic similarity search against a knowledge base, combines the retrieved results, removes duplicates, ranks the documents using their best similarity score, and returns the most relevant results through a REST API.

This project demonstrates how multi-query retrieval can improve the recall and coverage of information in modern RAG applications.

## Objectives

The main objectives of this project are:

- Build a Multi-Query Retrieval system
- Generate multiple variations of a user's question
- Create semantic embeddings for queries and documents
- Perform semantic similarity search
- Combine results from multiple queries
- Remove duplicate documents
- Track matched queries
- Select the best similarity score
- Rank retrieved documents
- Return configurable Top-K results
- Build a production-style REST API with FastAPI
- Test the API using PowerShell and Swagger UI

## How Multi-Query Retrieval Works

A traditional semantic search system normally follows this process:

User Question → Embedding → Vector Search → Results

This project improves the retrieval process by generating multiple search queries:

User Question → Multi-Query Generation → Multiple Query Embeddings → Semantic Search → Result Combination → Duplicate Removal → Ranking → Top-K Results

For example, the user can send:

What is Python used for?

The system can generate related queries such as:

What is Python used for?

Explain What is Python used for?

Give information about What is Python used for?

What are the main uses and applications of What is Python used for?

Each query is searched independently and the results are combined.

## System Architecture

Client

↓

FastAPI REST API

↓

Question Processing

↓

Multi-Query Generation

↓

Sentence Transformer

↓

Query Embeddings

↓

Semantic Similarity Search

↓

Result Combination

↓

Duplicate Removal

↓

Best Score Selection

↓

Ranking

↓

Top-K Results

↓

JSON Response

## Technologies Used

- Python 3.13
- FastAPI
- Uvicorn
- Sentence Transformers
- all-MiniLM-L6-v2
- NumPy
- SciPy
- Scikit-learn
- Cosine Similarity
- REST API
- JSON
- Swagger / OpenAPI
- Git
- GitHub

## Project Structure

21_RAG_Multi_Query_Search_API/

├── main.py

├── requirements.txt

├── README.md

├── .gitignore

└── venv/

The `venv` directory is used for the Python virtual environment and should not be uploaded to GitHub.

## main.py

The `main.py` file contains the main FastAPI application.

It is responsible for:

- Starting the FastAPI application
- Loading the embedding model
- Creating the document knowledge base
- Generating document embeddings
- Generating multiple queries
- Creating query embeddings
- Performing semantic search
- Combining search results
- Removing duplicate documents
- Calculating best similarity scores
- Ranking results
- Returning Top-K results
- Providing API endpoints

## requirements.txt

The `requirements.txt` file contains the Python packages required by this project.

Typical dependencies include:

- fastapi
- uvicorn
- sentence-transformers
- numpy
- scipy
- scikit-learn

## .gitignore

The `.gitignore` file prevents unnecessary files from being uploaded to GitHub.

Example contents:

venv/

__pycache__/

*.pyc

.env

.vscode/

## Knowledge Base

The project contains a demonstration knowledge base with information about technologies such as:

- Python
- FastAPI
- Machine Learning
- Natural Language Processing
- Docker
- Artificial Intelligence
- RAG
- Cloud Computing

Example document:

Python is a popular programming language used for web development, automation, data science, and artificial intelligence.

Another example:

FastAPI is a modern Python framework for building high-performance APIs.

Another example:

Machine learning allows computers to learn patterns from data without being explicitly programmed.

## Embedding Model

The project uses the Sentence Transformers model:

all-MiniLM-L6-v2

The model converts text into numerical vectors.

Text

↓

Sentence Transformer

↓

Numerical Embedding

These embeddings allow the application to compare the semantic meaning of questions and documents.

## Semantic Similarity

The system uses semantic similarity to determine which documents are most relevant to a user's question.

The basic process is:

Query

↓

Query Embedding

↓

Compare with Document Embeddings

↓

Similarity Scores

↓

Rank Results

Higher similarity scores indicate stronger semantic relationships between the query and document.

## Result Aggregation

Each generated query performs semantic retrieval.

The results from all generated queries are then combined.

If the same document is returned by multiple queries, the system avoids returning duplicate copies of the document.

The system keeps information such as:

- Document
- Best similarity score
- Matched queries

This provides more useful retrieval information.

## Best Score

When the same document is retrieved by multiple generated queries, the system keeps the strongest similarity score.

For example:

Query 1 → Document A → 0.72

Query 2 → Document A → 0.83

Query 3 → Document A → 0.76

The final score becomes:

Document A → 0.83

The document is then ranked using this best score.

## Top-K Retrieval

The API supports a `top_k` parameter.

Example request:

{
  "question": "What is Python used for?",
  "top_k": 5
}

This means the API should return the five highest-ranked results.

## Installation

First, clone the repository:

git clone https://github.com/athulsathyan136-alt/Hybrid-RAG-System.git

Then enter the project directory:

cd Hybrid-RAG-System/21_RAG_Multi_Query_Search_API

Create a Python 3.13 virtual environment:

py -3.13 -m venv venv

Windows PowerShell activation can sometimes be blocked by the system execution policy.

Activation is not required.

The virtual environment Python executable can be used directly.

Upgrade pip:

.\venv\Scripts\python.exe -m pip install --upgrade pip

Install dependencies:

.\venv\Scripts\python.exe -m pip install -r requirements.txt

## Running the API

Start the FastAPI server with:

.\venv\Scripts\python.exe -m uvicorn main:app --port 8010

When the server starts successfully, the terminal displays:

INFO: Application startup complete.

INFO: Uvicorn running on http://127.0.0.1:8010

The API is now available locally.

## Swagger UI

FastAPI automatically provides interactive API documentation.

Open:

http://127.0.0.1:8010/docs

Swagger UI can be used to test the API without writing PowerShell commands.

## API Endpoints

The main endpoints are:

GET /

GET /health

POST /search

## Home Endpoint

Request:

GET http://127.0.0.1:8010/

This endpoint provides basic information about the application.

## Health Endpoint

Request:

GET http://127.0.0.1:8010/health

This endpoint verifies that the application is running correctly.

## Search Endpoint

The main endpoint is:

POST /search

Example request:

{
  "question": "What is Python used for?",
  "top_k": 5
}

The system then:

1. Receives the question
2. Generates multiple search queries
3. Creates embeddings
4. Searches the knowledge base
5. Combines results
6. Removes duplicate documents
7. Calculates the best score
8. Ranks the documents
9. Returns the Top-K results

## PowerShell API Test

The following command was successfully used to test the API:

Invoke-RestMethod `
  -Uri http://127.0.0.1:8010/search `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"question":"What is Python used for?","top_k":5}' |
  ConvertTo-Json -Depth 10

## Example Response

The API returns information similar to:

{
  "question": "What is Python used for?",
  "generated_queries": [
    "What is Python used for?",
    "Explain What is Python used for?",
    "Give information about What is Python used for?",
    "What are the main uses and applications of What is Python used for?"
  ],
  "total_queries": 4,
  "results": [
    {
      "document": "Python is a popular programming language used for web development, automation, data science, and artificial intelligence.",
      "best_score": 0.826152503490448,
      "matched_queries": [
        "What is Python used for?",
        "Explain What is Python used for?",
        "Give information about What is Python used for?",
        "What are the main uses and applications of What is Python used for?"
      ]
    }
  ]
}

## Successful Test

The API was successfully started on:

http://127.0.0.1:8010

The search endpoint was successfully tested with:

What is Python used for?

The system successfully generated multiple queries and returned ranked semantic search results.

The most relevant document was:

Python is a popular programming language used for web development, automation, data science, and artificial intelligence.

The response also included:

- Generated queries
- Total number of queries
- Retrieved documents
- Best similarity scores
- Matched queries

This confirms that the Multi-Query Search pipeline is working successfully.

## Hugging Face Warning

When the embedding model is downloaded, Hugging Face may display a warning similar to:

Warning: You are sending unauthenticated requests to the HF Hub.

This is a warning and does not mean that the application failed.

The model can still download and the API can operate normally.

A Hugging Face token can be configured when authenticated access or higher download limits are required.

## Learning Outcomes

This project provided practical experience with:

- Python
- FastAPI
- REST API development
- Sentence Transformers
- Text embeddings
- Semantic search
- Cosine similarity
- Query expansion
- Multi-query retrieval
- Result aggregation
- Duplicate removal
- Ranking
- Top-K retrieval
- JSON APIs
- Swagger
- Virtual environments
- Dependency management
- Git
- GitHub

## RAG Architecture

Multi-query retrieval is an important component of modern RAG systems.

A complete RAG architecture can be represented as:

User Question

↓

Query Expansion / Multi-Query Generation

↓

Query Embeddings

↓

Vector Search

↓

Relevant Documents

↓

Context Construction

↓

Large Language Model

↓

Final Answer

This project focuses primarily on the retrieval and query expansion stages.

## Future Improvements

Possible future improvements include:

- ChromaDB integration
- FAISS integration
- PDF document ingestion
- Automatic document chunking
- Persistent vector databases
- LLM-based query generation
- Cross-encoder reranking
- Metadata filtering
- Conversation memory
- Authentication
- Rate limiting
- Docker containerization
- AWS deployment
- Automated testing
- CI/CD
- Monitoring
- MLOps
- LLMOps

## Cloud Deployment

The project can later be deployed to AWS.

Possible architecture:

User

↓

AWS Load Balancer

↓

FastAPI Application

↓

RAG Retrieval Service

↓

Vector Database

↓

Embedding Model

↓

LLM

↓

Final Response

Possible AWS services include:

- Amazon EC2
- Amazon ECS
- Amazon EKS
- Amazon ECR
- Amazon S3
- AWS Lambda
- AWS IAM
- Amazon CloudWatch

## Production Improvements

For production usage, the following should be added:

- Authentication
- HTTPS
- Secure secret management
- Input validation
- Rate limiting
- Error handling
- Logging
- Monitoring
- Persistent storage
- Docker
- Automated tests
- CI/CD
- Cloud deployment

## Portfolio Progression

This project is part of the Hybrid-RAG-System portfolio.

The RAG projects are progressively becoming more advanced.

Project 18:

Persistent RAG Chatbot with SQLite

↓

Project 19:

RAG PDF Chatbot with ChromaDB

↓

Project 20:

RAG Hybrid Search API

↓

Project 21:

RAG Multi-Query Search API

This progression demonstrates practical development from basic RAG concepts toward more advanced retrieval architectures.

## Project Features

| Feature | Status |
|---|---|
| FastAPI | ✅ Completed |
| REST API | ✅ Completed |
| Multi-Query Generation | ✅ Completed |
| Sentence Transformers | ✅ Completed |
| Text Embeddings | ✅ Completed |
| Semantic Search | ✅ Completed |
| Similarity Scoring | ✅ Completed |
| Result Aggregation | ✅ Completed |
| Duplicate Removal | ✅ Completed |
| Best Score Ranking | ✅ Completed |
| Top-K Retrieval | ✅ Completed |
| Health Endpoint | ✅ Completed |
| Swagger Documentation | ✅ Completed |
| Python 3.13 | ✅ Completed |
| API Testing | ✅ Completed |
| GitHub Ready | ✅ Completed |


## Author

Athul Sathyan

B.Tech Computer Engineering

AI/ML + Cloud Engineering Portfolio
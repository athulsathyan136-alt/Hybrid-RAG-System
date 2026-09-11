# Project 20 - RAG Hybrid Search API

A Hybrid Retrieval API that combines Semantic Search and Keyword Search to retrieve the most relevant documents for a user query.

This project is part of my AI/ML + Cloud Engineering Portfolio.

PROJECT INFORMATION

Project Number: 20
Project Name: RAG Hybrid Search API
Category: AI/ML + RAG + NLP
Language: Python 3.13
Framework: FastAPI
Server: Uvicorn
Embedding Model: all-MiniLM-L6-v2
Semantic Search: Sentence Transformers
Keyword Search: TF-IDF
Similarity: Cosine Similarity
Semantic Weight: 70%
Keyword Weight: 30%
API Port: 8009
Documentation: Swagger
Status: Completed


PROJECT OBJECTIVE

The objective of this project is to build a Hybrid Search system that combines two retrieval techniques:

1. Semantic Search
2. Keyword Search

The system combines both search results and calculates a Hybrid Score to rank documents according to their relevance.

Hybrid Search is an important component of modern Retrieval Augmented Generation (RAG) systems.


WHAT IS HYBRID SEARCH?

Hybrid Search combines semantic understanding with exact keyword matching.

User Query
    |
    v
Hybrid Search
    |
    +-------------------+
    |                   |
    v                   v
Semantic Search     Keyword Search
    |                   |
    v                   v
Embeddings             TF-IDF
    |                   |
    v                   v
Semantic Score      Keyword Score
    |                   |
    +---------+---------+
              |
              v
      Score Normalization
              |
              v
       Hybrid Scoring
              |
              v
        Ranked Results


SYSTEM ARCHITECTURE

                         USER QUERY
                             |
                             v
                    +----------------+
                    |    FastAPI     |
                    |      API       |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    | Hybrid Search  |
                    +-------+--------+
                            |
              +-------------+-------------+
              |                           |
              v                           v
     +------------------+        +------------------+
     | Semantic Search  |        | Keyword Search   |
     +--------+---------+        +--------+---------+
              |                           |
              v                           v
     Sentence Transformers             TF-IDF
              |                           |
              v                           v
      Semantic Score              Keyword Score
              |                           |
              +-------------+-------------+
                            |
                            v
                  Score Normalization
                            |
                            v
                     Hybrid Score
                            |
                            v
                    Ranked Results
                            |
                            v
                     API Response


SEARCH PIPELINE

Documents
    |
    v
Document Indexing
    |
    +-----------------------+
    |                       |
    v                       v
Semantic Index          TF-IDF Index
    |                       |
    +-----------+-----------+
                |
                v
            User Query
                |
        +-------+-------+
        |               |
        v               v
Semantic Search    Keyword Search
        |               |
        v               v
Semantic Score     Keyword Score
        |               |
        +-------+-------+
                |
                v
        Score Normalization
                |
                v
          Hybrid Scoring
                |
                v
          Result Ranking
                |
                v
             Top-K


SEMANTIC SEARCH

Semantic Search is implemented using Sentence Transformers.

The model used is:

all-MiniLM-L6-v2

The model converts text into numerical vectors called embeddings.

Text
 |
 v
Embedding Model
 |
 v
Numerical Vector

Semantic Search allows the system to find documents based on meaning rather than only exact words.


EMBEDDINGS

Embeddings are numerical representations of text.

For example, a sentence such as:

Python is useful for AI

is converted into a numerical vector.

The system creates embeddings for documents and user queries and compares them to identify semantically related content.


COSINE SIMILARITY

Cosine Similarity is used to compare the query embedding with document embeddings.

A higher similarity score generally means that the vectors are more closely related.

Query Vector
     |
     v
Cosine Similarity
     |
     v
Document Vector


KEYWORD SEARCH

Keyword Search is implemented using TF-IDF.

TF-IDF stands for:

Term Frequency-Inverse Document Frequency

TF-IDF identifies important words in documents and compares them with words in the user query.

For example, a query containing:

AWS EC2

can strongly match a document containing:

AWS provides cloud services such as EC2, S3, Lambda, ECS, and EKS.


HYBRID SCORING

The project combines Semantic Search and Keyword Search.

Current weights:

Semantic Search = 70%
Keyword Search  = 30%

Formula:

Hybrid Score =
(0.7 x Semantic Score)
+
(0.3 x Keyword Score)

This allows semantic relevance and exact keyword matching to contribute to the final ranking.


SCORE PROCESSING

Semantic Scores
      |
      v
Normalization
      |
      v
Normalized Semantic Scores


Keyword Scores
      |
      v
Normalization
      |
      v
Normalized Keyword Scores


Normalized Scores
      |
      v
Weighted Combination
      |
      v
Hybrid Score
      |
      v
Sorting
      |
      v
Top-K Results


KNOWLEDGE BASE

The current application contains sample documents related to:

- Python
- FastAPI
- Machine Learning
- Deep Learning
- Natural Language Processing
- Retrieval Augmented Generation
- Vector Databases
- Docker
- AWS
- MLOps


TECHNOLOGIES USED

Python 3.13
FastAPI
Uvicorn
Sentence Transformers
all-MiniLM-L6-v2
Scikit-learn
TF-IDF
Cosine Similarity
NumPy
Swagger


PROJECT STRUCTURE

20_RAG_Hybrid_Search_API/
|
+-- main.py
+-- requirements.txt
+-- README.md
+-- .gitignore
+-- venv/


The venv directory is excluded from GitHub.


INSTALLATION

STEP 1 - Open the project

cd C:\Users\LENOVO\Hybrid-RAG-System\20_RAG_Hybrid_Search_API


STEP 2 - Check Python

py -3.13 --version

Expected:

Python 3.13.x


STEP 3 - Create virtual environment

py -3.13 -m venv venv


STEP 4 - Upgrade pip

.\venv\Scripts\python.exe -m pip install --upgrade pip


STEP 5 - Install dependencies

.\venv\Scripts\python.exe -m pip install -r requirements.txt


RUN THE API

Start the server:

.\venv\Scripts\python.exe -m uvicorn main:app --port 8009

The API will run at:

http://127.0.0.1:8009


SWAGGER DOCUMENTATION

Open the following URL in your browser:

http://127.0.0.1:8009/docs

Swagger provides an interactive interface for testing the API.


API ENDPOINTS

GET /

Returns API information.

GET /documents

Returns all documents in the knowledge base.

POST /search

Performs Hybrid Search.

GET /health

Checks the health of the API.


GET /

Example response:

{
    "message": "RAG Hybrid Search API is running",
    "documents": 10,
    "search_methods": [
        "Semantic Search",
        "Keyword Search",
        "Hybrid Search"
    ]
}


GET /documents

Returns the documents stored in the knowledge base.


POST /search

This is the main endpoint.

It performs:

1. Semantic Search
2. Keyword Search
3. Score Normalization
4. Hybrid Scoring
5. Result Ranking


Example request:

{
    "query": "How is Python used in artificial intelligence?",
    "top_k": 5
}


Example response:

{
    "query": "How is Python used in artificial intelligence?",
    "semantic_weight": 0.7,
    "keyword_weight": 0.3,
    "results": [
        {
            "document": "Python is a popular programming language used for web development, automation, data science, and artificial intelligence.",
            "semantic_score": 1.0,
            "keyword_score": 1.0,
            "hybrid_score": 1.0
        }
    ]
}


GET /health

Example response:

{
    "status": "healthy",
    "model": "all-MiniLM-L6-v2",
    "documents": 10,
    "keyword_index": "TF-IDF",
    "semantic_search": "Sentence Transformers",
    "hybrid_search": "Enabled"
}


TESTING WITH SWAGGER

Open:

http://127.0.0.1:8009/docs

Select:

POST /search

Click:

Try it out

Enter:

{
    "query": "What is Python used for?",
    "top_k": 5
}

Click:

Execute

The API will return ranked results.


TEST QUERIES

Python:

{
    "query": "What is Python used for?",
    "top_k": 5
}


Machine Learning:

{
    "query": "How does machine learning work?",
    "top_k": 5
}


Deep Learning:

{
    "query": "What is deep learning?",
    "top_k": 5
}


RAG:

{
    "query": "What is Retrieval Augmented Generation?",
    "top_k": 5
}


Docker:

{
    "query": "What is Docker?",
    "top_k": 5
}


AWS:

{
    "query": "What AWS cloud services are available?",
    "top_k": 5
}


MLOps:

{
    "query": "What is MLOps?",
    "top_k": 5
}


CONNECTION TO RAG

Hybrid Search is an important retrieval component of a modern RAG system.

A complete RAG architecture can look like:

USER QUESTION
      |
      v
Query Processing
      |
      v
Hybrid Retrieval
      |
      +------------------+
      |                  |
      v                  v
Semantic Search     Keyword Search
      |                  |
      +--------+---------+
               |
               v
        Ranked Results
               |
               v
        Relevant Context
               |
               v
              LLM
               |
               v
         Final Answer


COMPLETE RAG PIPELINE

PDF Documents
      |
      v
Text Extraction
      |
      v
Text Chunking
      |
      v
Embedding Generation
      |
      +------------------+
      |                  |
      v                  v
Vector Index        Keyword Index
      |                  |
      +--------+---------+
               |
               v
         Hybrid Search
               |
               v
      Relevant Documents
               |
               v
             Context
               |
               v
              LLM
               |
               v
          Final Answer


LEARNING OBJECTIVES

This project provides practical experience with:

- Python
- FastAPI
- REST API development
- Natural Language Processing
- Information Retrieval
- Semantic Search
- Keyword Search
- TF-IDF
- Text Embeddings
- Sentence Transformers
- Cosine Similarity
- Score Normalization
- Hybrid Retrieval
- Search Ranking
- RAG Architecture
- Swagger API Testing
- AI/ML Backend Development


CONCEPTS LEARNED

Embeddings

Representing text as numerical vectors.

Vector Similarity

Comparing vectors to find semantically related content.

TF-IDF

Finding important terms within documents.

Cosine Similarity

Measuring similarity between vectors.

Hybrid Retrieval

Combining multiple retrieval strategies.

Ranking

Ordering documents according to relevance.


FUTURE IMPROVEMENTS

Future versions can include:

- PDF upload
- Automatic text extraction
- Advanced text chunking
- FAISS integration
- ChromaDB integration
- LLM answer generation
- Complete RAG chatbot
- Conversation memory
- Redis caching
- PostgreSQL
- Docker
- AWS deployment
- Authentication
- Monitoring
- Search analytics


FUTURE DOCKER ARCHITECTURE

Source Code
     |
     v
Dockerfile
     |
     v
Docker Image
     |
     v
Docker Container
     |
     v
FastAPI Application


FUTURE AWS ARCHITECTURE

The production version can use:

- AWS S3
- AWS EC2
- AWS ECR
- AWS ECS
- AWS EKS
- AWS Lambda
- AWS RDS
- AWS IAM
- AWS CloudWatch

Possible architecture:

                         USER
                           |
                           v
                    Load Balancer
                           |
                           v
                      FastAPI API
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
            S3        PostgreSQL     Vector DB
             |             |             |
             +-------------+-------------+
                           |
                           v
                     Hybrid Search
                           |
                           v
                          LLM
                           |
                           v
                     Final Answer


PRODUCTION SECURITY

Before production deployment, the following should be added:

- API authentication
- Authorization
- API keys or OAuth
- HTTPS
- Secure CORS configuration
- Rate limiting
- Input validation
- Secret management
- Environment variables
- Logging
- Monitoring


PERFORMANCE IMPROVEMENTS

Future versions can improve performance using:

- FAISS
- ChromaDB
- Redis caching
- Batch embeddings
- Asynchronous processing
- Database indexing
- GPU acceleration
- Query caching
- Document preprocessing


SCALABILITY

The current version uses a small in-memory knowledge base.

A production system can evolve into:

Large Knowledge Base
        |
        v
Vector Database
        +
Keyword Search
        |
        v
Hybrid Retrieval
        |
        v
FastAPI
        |
        v
Cloud Infrastructure


PROJECT PROGRESSION

This project continues the RAG portfolio progression:

PDF Processing
      |
      v
Text Extraction
      |
      v
Text Chunking
      |
      v
Embeddings
      |
      v
Vector Search
      |
      v
RAG
      |
      v
RAG Chatbot
      |
      v
Chat Memory
      |
      v
Persistent Memory
      |
      v
ChromaDB
      |
      v
Hybrid Search


PORTFOLIO SKILLS

This project demonstrates practical experience with:

Python
+
FastAPI
+
NLP
+
Machine Learning
+
Embeddings
+
Information Retrieval
+
RAG
+
API Development
+
Cloud-ready Architecture


RELEVANT CAREER ROLES

The skills demonstrated by this project are relevant to:

- AI/ML Engineer
- Machine Learning Engineer
- GenAI Engineer
- RAG Engineer
- AI Backend Engineer
- NLP Engineer
- MLOps Engineer
- Cloud AI Engineer


TROUBLESHOOTING

Check Python:

.\venv\Scripts\python.exe --version


Check installed packages:

.\venv\Scripts\python.exe -m pip list


Test imports:

.\venv\Scripts\python.exe -c "import fastapi, sentence_transformers, sklearn, numpy; print('Project 20 environment OK')"

Expected:

Project 20 environment OK


PORT 8009 ALREADY IN USE

Check the port:

netstat -ano | findstr :8009

If a process is using the port, identify its PID and stop it:

taskkill /PID YOUR_PID /F

Then start the API again:

.\venv\Scripts\python.exe -m uvicorn main:app --port 8009


GITHUB UPLOAD

From the repository root:

cd C:\Users\LENOVO\Hybrid-RAG-System


Check Git status:

git status


Add Project 20:

git add 20_RAG_Hybrid_Search_API


Commit:

git commit -m "Add Project 20 RAG Hybrid Search API"


Push:

git push origin main


GITHUB REPOSITORY

Repository:

https://github.com/athulsathyan136-alt/Hybrid-RAG-System

Project folder:

20_RAG_Hybrid_Search_API


FINAL PROJECT SUMMARY

PROJECT 20
RAG HYBRID SEARCH API

Project:
RAG Hybrid Search API

Category:
AI/ML + RAG + NLP

Language:
Python 3.13

Framework:
FastAPI

Server:
Uvicorn

Semantic Search:
Sentence Transformers

Embedding Model:
all-MiniLM-L6-v2

Keyword Search:
TF-IDF

Similarity:
Cosine Similarity

Semantic Weight:
70%

Keyword Weight:
30%

API Port:
8009

Documentation:
Swagger

Knowledge Base:
10 Sample Documents

Status:
COMPLETED


PROJECT 20 RESULT

The completed system can:

- Store documents
- Generate semantic embeddings
- Build TF-IDF keyword index
- Accept user queries
- Perform semantic search
- Perform keyword search
- Normalize search scores
- Calculate hybrid scores
- Rank documents
- Return Top-K results
- Expose results through FastAPI
- Provide Swagger documentation
- Provide a RAG-ready retrieval layer


KEY ACHIEVEMENT

Project 20 demonstrates how to build a Hybrid Retrieval System by combining:

SEMANTIC SEARCH
        +
KEYWORD SEARCH
        |
        v
  HYBRID SCORE
        |
        v
 RANKED RESULTS
        |
        v
     FASTAPI
        |
        v
 RAG RETRIEVAL


AUTHOR

Athul Sathyan

B.Tech Computer Engineering

AI/ML + Cloud Engineering Portfolio



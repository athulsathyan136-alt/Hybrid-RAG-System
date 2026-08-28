# 🚀 Day 7 — RAG Chat API

A Retrieval-Augmented Generation (RAG) Chat API built with Python, FastAPI, Sentence Transformers, FAISS, and Google's FLAN-T5 model.

This project converts the RAG pipeline from Day 6 into a REST API that can receive questions, retrieve relevant information, generate an answer, and return the sources used.

---

## 📌 Project Overview

This project demonstrates how to build an AI-powered question-answering API.

The user sends a question to the `/chat` endpoint.

The system then:

1. Converts the question into an embedding.
2. Searches the FAISS vector index.
3. Retrieves the most relevant documents.
4. Sends the retrieved context to FLAN-T5.
5. Generates an answer.
6. Returns the answer and source documents.

---

## 🧠 What is RAG?

RAG stands for **Retrieval-Augmented Generation**.

Instead of asking an AI model to answer only from its trained knowledge, RAG first retrieves relevant information from a knowledge base.

The retrieved information is then provided to the language model.

### RAG Flow

```text
User Question
      ↓
Embedding Model
      ↓
Question Vector
      ↓
FAISS Similarity Search
      ↓
Relevant Documents
      ↓
Context + Question
      ↓
FLAN-T5 Language Model
      ↓
Generated Answer
      ↓
FastAPI Response
```

---

## 🎯 Features

- REST API using FastAPI
- AI-powered question answering
- Sentence Transformer embeddings
- FAISS vector similarity search
- FLAN-T5 language model
- Source document retrieval
- Health check endpoint
- Swagger API documentation
- Local AI inference
- No external database required

---

## 🛠️ Technologies Used

- Python
- FastAPI
- Uvicorn
- Sentence Transformers
- Hugging Face Transformers
- FAISS
- NumPy
- Scikit-learn
- SciPy
- PyTorch
- Google FLAN-T5

---

## 📁 Project Structure

```text
07_RAG_Chat_API/
│
├── main.py
├── README.md
├── .gitignore
└── venv/
```

### main.py

Contains the complete FastAPI RAG application.

### README.md

Project documentation.

### .gitignore

Prevents virtual environment and Python cache files from being uploaded to GitHub.

### venv/

Python virtual environment used for the project.

---

## ⚙️ How the System Works

### Step 1 — User asks a question

Example:

```text
What is Docker?
```

### Step 2 — Convert question into an embedding

The Sentence Transformer converts the question into a numerical vector.

```text
"What is Docker?"
        ↓
[0.12, -0.45, 0.78, ...]
```

### Step 3 — Search FAISS

FAISS compares the question vector with document vectors.

The most similar documents are retrieved.

### Step 4 — Build context

The retrieved documents are combined into context.

Example:

```text
Docker packages applications into lightweight containers.
```

### Step 5 — Generate answer

FLAN-T5 receives:

```text
Context:
Docker packages applications into lightweight containers.

Question:
What is Docker?
```

and generates an answer.

### Step 6 — Return API response

The API returns:

```json
{
  "question": "What is Docker?",
  "answer": "Docker packages applications into lightweight containers.",
  "sources": [
    {
      "text": "Docker packages applications into lightweight containers.",
      "distance": 0.0
    }
  ]
}
```

---

# 🔌 API Endpoints

## GET `/`

Checks whether the API is running.

### Example

```text
http://127.0.0.1:8000/
```

### Response

```json
{
  "message": "RAG Chat API is running!",
  "version": "1.0.0",
  "endpoint": "/chat"
}
```

---

## GET `/health`

Checks the health of the RAG system.

### Example

```text
http://127.0.0.1:8000/health
```

### Response

```json
{
  "status": "healthy",
  "documents": 15,
  "embedding_model": "all-MiniLM-L6-v2",
  "language_model": "google/flan-t5-small"
}
```

---

# 🤖 POST `/chat`

Main RAG question-answering endpoint.

### Request

```json
{
  "question": "What is Docker?"
}
```

### Response

```json
{
  "question": "What is Docker?",
  "answer": "Docker packages applications into lightweight containers.",
  "sources": [
    {
      "text": "Docker packages applications into lightweight containers.",
      "distance": 0.0
    }
  ]
}
```

---

# 📖 Example Questions

You can test the API with:

```text
What is Python?
```

```text
What is Docker?
```

```text
What is AWS?
```

```text
What is Amazon S3?
```

```text
What is FAISS?
```

```text
What is machine learning?
```

```text
What is MLOps?
```

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/athulsathyan136-alt/Hybrid-RAG-System.git
```

Move into the project:

```bash
cd Hybrid-RAG-System/07_RAG_Chat_API
```

---

## 2. Create virtual environment

Windows:

```powershell
python -m venv venv
```

---

## 3. Install dependencies

```powershell
.\venv\Scripts\python.exe -m pip install fastapi uvicorn sentence-transformers faiss-cpu numpy transformers torch scikit-learn scipy
```

---

## 4. Run the API

```powershell
.\venv\Scripts\python.exe -m uvicorn main:app
```

The API will start at:

```text
http://127.0.0.1:8000
```

---

# 📚 Swagger Documentation

FastAPI automatically creates interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can test all endpoints directly from the browser.

---

# 🧪 Testing the API

Open:

```text
http://127.0.0.1:8000/docs
```

Find:

```text
POST /chat
```

Click:

```text
Try it out
```

Enter:

```json
{
  "question": "What is Docker?"
}
```

Click:

```text
Execute
```

The API will retrieve relevant information and generate an answer.

---

# 🔐 Security

This project is currently designed for local development and learning.

Production deployments should add:

- Authentication
- API keys
- HTTPS
- Rate limiting
- Input validation
- Secret management
- Logging
- Monitoring
- IAM permissions

---

# 📈 Future Improvements

Possible improvements include:

- PDF document upload
- Persistent vector database
- Pinecone integration
- PostgreSQL integration
- Redis caching
- AWS S3 storage
- AWS Lambda processing
- AWS Bedrock
- Docker deployment
- ECS deployment
- GitHub Actions CI/CD
- Authentication
- Streaming responses
- Conversation memory
- Hybrid BM25 + vector search
- RAG evaluation
- Monitoring

---

# 🏗️ Future Architecture

```text
User
 │
 ▼
Frontend
 │
 ▼
FastAPI
 │
 ├───────────────┐
 ▼               ▼
Embedding       Authentication
Model
 │
 ▼
Vector Database
 │
 ▼
Retriever
 │
 ▼
Relevant Context
 │
 ▼
LLM
 │
 ▼
Generated Answer
 │
 ▼
User
```

---

# 🎓 Learning Outcomes

By completing this project, I learned:

- What RAG is
- How embeddings work
- How vector similarity search works
- How FAISS works
- How language models generate answers
- How FastAPI works
- How REST APIs work
- How to create API endpoints
- How to use Pydantic request models
- How to retrieve documents
- How to connect an AI model to an API
- How to test APIs using Swagger
- How to structure an AI project

---

# 💼 Portfolio Value

This project demonstrates practical skills in:

```text
Python
   ↓
Machine Learning
   ↓
Embeddings
   ↓
Vector Search
   ↓
RAG
   ↓
LLM
   ↓
FastAPI
   ↓
AI API Development
```

It is part of a larger **30 Days, 30 Projects — AI/ML + Cloud Portfolio Builder**.

---

# 📅 Project Series

| Day | Project |
|---|---|
| Day 1 | PDF Text Extractor API |
| Day 2 | Smart Text Chunker |
| Day 3 | Embedding Generator |
| Day 4 | Vector Database |
| Day 5 | Semantic Search Engine |
| Day 6 | RAG Pipeline |
| **Day 7** | **RAG Chat API** |
| Day 8 | Streamlit RAG Frontend |
| Day 9 | AWS S3 Integration |
| Day 10 | AWS SQS Queue |

---

# 👨‍💻 Author

**Amal Sathyan**

GitHub:

https://github.com/athulsathyan136-alt

---

# ⭐ Conclusion

The Day 7 project transforms a local RAG pipeline into a usable REST API.

The system combines:

```text
FastAPI
+
Sentence Transformers
+
FAISS
+
FLAN-T5
=
RAG Chat API
```


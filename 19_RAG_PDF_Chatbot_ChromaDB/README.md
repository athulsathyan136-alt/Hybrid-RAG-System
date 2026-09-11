# 🚀 RAG PDF Chatbot with ChromaDB

A Retrieval-Augmented Generation (RAG) PDF chatbot built with **FastAPI, ChromaDB, Sentence Transformers, PyPDF2, and FLAN-T5**.

The application allows users to upload PDF documents, convert their content into vector embeddings, store them in ChromaDB, retrieve relevant information using semantic search, and generate AI-powered answers using a local language model.

---

## 🧠 Architecture

```text
PDF Document
     ↓
PyPDF2
     ↓
Text Extraction
     ↓
Text Chunking
     ↓
Sentence Transformers
     ↓
Vector Embeddings
     ↓
ChromaDB
     ↓
Semantic Search
     ↓
Relevant Context
     ↓
FLAN-T5
     ↓
AI Generated Answer
     ↓
Sources
```

---

## ✨ Features

* 📄 Upload one or multiple PDF files
* 🔍 Extract text from PDF documents
* 🧩 Split documents into searchable chunks
* 🧠 Generate embeddings using Sentence Transformers
* 🗄️ Store vectors in persistent ChromaDB
* 🔎 Perform semantic similarity search
* 🤖 Generate answers using Google's FLAN-T5
* 📚 Return source documents and chunk information
* ⚡ FastAPI REST API
* 📖 Interactive Swagger API documentation
* 🧹 Clear the vector database
* 💾 Persistent local vector storage

---

## 🛠️ Technologies

| Technology            | Purpose                 |
| --------------------- | ----------------------- |
| Python                | Programming language    |
| FastAPI               | REST API framework      |
| PyPDF2                | PDF text extraction     |
| Sentence Transformers | Text embeddings         |
| ChromaDB              | Vector database         |
| FLAN-T5               | Local answer generation |
| Uvicorn               | ASGI server             |
| Pydantic              | Request validation      |

---

## 📁 Project Structure

```text
19_RAG_PDF_Chatbot_ChromaDB/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── chroma_db/          # Generated locally - not committed
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/athulsathyan136-alt/Hybrid-RAG-System.git
```

### 2. Enter Project 19

```bash
cd Hybrid-RAG-System/19_RAG_PDF_Chatbot_ChromaDB
```

### 3. Create virtual environment

```bash
python -m venv venv
```

### 4. Activate virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the Python executable directly:

```powershell
.\venv\Scripts\python.exe
```

### 5. Install dependencies

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## ▶️ Run the Application

Start the FastAPI server:

```powershell
.\venv\Scripts\python.exe -m uvicorn main:app --port 8008
```

The API will run at:

```text
http://127.0.0.1:8008
```

---

## 📖 Swagger Documentation

Open:

```text
http://127.0.0.1:8008/docs
```

Swagger provides an interactive interface for testing all API endpoints.

---

## 🔌 API Endpoints

### `GET /`

Check application status.

Example response:

```json
{
  "message": "RAG PDF Chatbot with ChromaDB is running",
  "version": "2.0.0",
  "database_chunks": 5
}
```

---

### `POST /upload`

Upload one or multiple PDF documents.

The system:

1. Reads the PDF
2. Extracts text
3. Splits the text into chunks
4. Generates embeddings
5. Stores the data in ChromaDB

---

### `POST /ask`

Ask a question about the uploaded documents.

Example request:

```json
{
  "question": "What is the study timetable?",
  "top_k": 3
}
```

Example response:

```json
{
  "question": "What is the study timetable?",
  "answer": "A rigorous 5:00 AM – 11:00 PM schedule optimized for Python fluency, SQL data handling, Linux environments, and core Machine Learning foundations.",
  "sources": [
    {
      "filename": "AIML_Engineer_Study_Timetable.pdf",
      "chunk_number": 1,
      "distance": 1.09
    }
  ],
  "total_results": 3
}
```

---

### `GET /database`

Returns the number of stored document chunks.

---

### `DELETE /clear`

Deletes the existing ChromaDB collection and creates a new empty collection.

---

## 🧪 Example Workflow

```text
1. Start API
       ↓
2. Open Swagger
       ↓
3. Upload PDF
       ↓
4. PDF → Text
       ↓
5. Text → Chunks
       ↓
6. Chunks → Embeddings
       ↓
7. Embeddings → ChromaDB
       ↓
8. Ask Question
       ↓
9. Retrieve Relevant Chunks
       ↓
10. FLAN-T5 Generates Answer
       ↓
11. Return Answer + Sources
```

---

## 🔐 Security & GitHub

The following files and folders should **not** be committed:

```text
venv/
chroma_db/
.env
__pycache__/
*.pyc
```

These are excluded using `.gitignore`.

---

## 🎯 Learning Objectives

This project demonstrates practical knowledge of:

* Retrieval-Augmented Generation
* Vector databases
* Semantic search
* Embeddings
* Natural Language Processing
* Large Language Models
* FastAPI
* REST API development
* PDF processing
* Local AI inference
* AI application architecture

---

## 🚀 Future Improvements

Planned improvements include:

* Page-level source citations
* Better sentence-aware chunking
* Reranking
* Conversation memory
* Streaming responses
* Authentication
* Docker deployment
* AWS deployment
* Cloud vector database
* Production monitoring
* CI/CD with GitHub Actions
* Frontend chatbot interface

---

## 👨‍💻 Author

**Athul Sathyan**


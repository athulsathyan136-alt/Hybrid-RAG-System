# RAG Chatbot with Conversation Memory

A Retrieval-Augmented Generation (RAG) chatbot built with FastAPI, FAISS, Sentence Transformers, and Google's FLAN-T5 model.

The chatbot retrieves relevant information from a knowledge base, generates AI-powered responses, and stores conversation history in memory.

## Features

- Retrieval-Augmented Generation (RAG)
- Semantic search using vector embeddings
- FAISS similarity search
- AI answer generation with FLAN-T5
- Conversation memory
- Chat history API
- Memory clearing functionality
- FastAPI REST API
- Interactive Swagger documentation

## Architecture

```text
User Question
      │
      ▼
Conversation Memory
      │
      ▼
Sentence Transformer
      │
      ▼
Question Embedding
      │
      ▼
FAISS Vector Search
      │
      ▼
Relevant Documents
      │
      ▼
Context + Chat History
      │
      ▼
FLAN-T5 Language Model
      │
      ▼
Generated Answer
      │
      ▼
Store Conversation Memory
```

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Sentence Transformers
- FAISS
- Hugging Face Transformers
- PyTorch
- FLAN-T5

## Project Structure

```text
17_RAG_Chatbot_Memory/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── venv/
```

## Installation

Clone the repository:

```bash
git clone https://github.com/athulsathyan136-alt/Hybrid-RAG-System.git
```

Navigate to the project:

```bash
cd Hybrid-RAG-System/17_RAG_Chatbot_Memory
```

Create a virtual environment:

```bash
python -m venv venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

Windows:

```powershell
.\venv\Scripts\python.exe -m uvicorn main:app --port 8006
```

API URL:

```text
http://127.0.0.1:8006
```

Swagger documentation:

```text
http://127.0.0.1:8006/docs
```

## API Endpoints

### GET /

Check API status.

### POST /chat

Send a question to the RAG chatbot.

Example request:

```json
{
  "question": "What is Python?",
  "top_k": 3
}
```

Example response:

```json
{
  "question": "What is Python?",
  "answer": "Python is a popular programming language used for web development, automation, data science, and artificial intelligence.",
  "sources": [],
  "memory_messages": 2
}
```

### GET /memory

Retrieve the complete conversation history.

Example response:

```json
{
  "conversation": [
    {
      "role": "user",
      "message": "What is Python?"
    },
    {
      "role": "assistant",
      "message": "Python is a programming language."
    }
  ],
  "total_messages": 2
}
```

### DELETE /memory

Clear all conversation history.

### GET /documents

View all documents in the knowledge base.

## RAG Workflow

1. The user sends a question.
2. The question is converted into a vector embedding.
3. FAISS searches for relevant documents.
4. Relevant documents are retrieved.
5. Previous conversation messages are collected.
6. Documents and chat history are combined into context.
7. FLAN-T5 generates an answer.
8. The user question and AI answer are stored in memory.

## Learning Objectives

This project demonstrates:

- RAG architecture
- Vector embeddings
- Semantic search
- FAISS vector indexing
- LLM integration
- Conversation memory
- Context management
- FastAPI API development
- AI application architecture

## Future Improvements

- Persistent conversation database
- SQLite or PostgreSQL memory storage
- User authentication
- Multiple chat sessions
- PDF document upload
- Persistent vector database
- Streaming responses
- Docker support
- Cloud deployment
- AWS integration

## Author

Athul Sathyan


# Persistent RAG Chatbot with SQLite

A Retrieval-Augmented Generation (RAG) chatbot built with FastAPI, FAISS, Sentence Transformers, Hugging Face FLAN-T5, and SQLite.

This project extends a basic RAG chatbot by adding persistent conversation memory. Chat conversations are stored in a SQLite database and remain available even after the API server is restarted.

## Features

- Retrieval-Augmented Generation (RAG)
- Semantic search using vector embeddings
- FAISS vector similarity search
- Sentence Transformers embeddings
- AI answer generation using FLAN-T5
- SQLite persistent database
- Persistent conversation memory
- Multiple conversation sessions
- Conversation IDs
- Retrieve conversation history
- Delete conversation history
- FastAPI REST API
- Interactive Swagger API documentation

## Architecture

```text
User Question
     |
     v
FastAPI REST API
     |
     v
Sentence Transformer
     |
     v
Question Embedding
     |
     v
FAISS Vector Search
     |
     v
Relevant Documents
     |
     v
SQLite Conversation History
     |
     v
Context + Chat Memory
     |
     v
FLAN-T5 Language Model
     |
     v
Generated Answer
     |
     v
Store Messages in SQLite

Technologies Used
Python
FastAPI
Uvicorn
SQLAlchemy
SQLite
Sentence Transformers
FAISS
Hugging Face Transformers
PyTorch
Google FLAN-T5

18_RAG_Persistent_Chatbot_SQLite/
│
├── main.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
├── rag_chatbot.db
└── venv/

How the RAG System Works
The user sends a question through the API.
The question is converted into a vector embedding.
FAISS searches the vector index.
Relevant documents are retrieved.
Previous conversation history is retrieved from SQLite.
Documents and conversation memory are combined.
FLAN-T5 generates an answer.
The user question is stored in SQLite.
The AI answer is stored in SQLite.
The conversation remains available after server restart.

User Message
     |
     v
SQLite Database
     |
     v
Server Restart
     |
     v
Conversation Still Available

Learning Objectives

This project demonstrates:

Retrieval-Augmented Generation
Vector embeddings
Semantic search
FAISS indexing
LLM integration
Persistent conversation memory
SQLite databases
SQLAlchemy ORM
REST API development
AI backend architecture
Future Improvements
PostgreSQL database support
User authentication
JWT authentication
User-specific conversations
PDF document upload
Persistent vector database
ChromaDB or Pinecone integration
Streaming AI responses
Docker containerization
AWS deployment
CI/CD pipeline
Production logging and monitoring
Author

Athul Sathyan
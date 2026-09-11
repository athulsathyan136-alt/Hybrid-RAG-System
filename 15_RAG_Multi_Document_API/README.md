# 🚀 RAG Multi-Document API

A FastAPI-based Retrieval-Augmented Generation (RAG) document retrieval system that allows users to upload multiple PDF documents, extract their text, generate embeddings, store them in a FAISS vector database, and perform semantic search across all uploaded documents.

## 📌 Features

- Upload multiple PDF documents
- Extract text using PyPDF2
- Automatic text chunking
- Generate embeddings using Sentence Transformers
- Store vector embeddings using FAISS
- Semantic similarity search
- Search across multiple documents
- Persistent document metadata
- REST API built with FastAPI
- Interactive API documentation with Swagger UI
- Delete all indexed documents and vector data

## 🏗️ Architecture

```text
                USER
                  │
                  ▼
          FastAPI Application
                  │
                  ▼
        Upload Multiple PDFs
                  │
                  ▼
           PyPDF2 Extraction
                  │
                  ▼
            Text Chunking
                  │
                  ▼
     SentenceTransformer Embeddings
                  │
                  ▼
           FAISS Vector Store
                  │
                  ▼
            Semantic Query
                  │
                  ▼
       Ranked Document Results
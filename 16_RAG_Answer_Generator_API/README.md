# RAG Answer Generator API

A Retrieval-Augmented Generation (RAG) API built with FastAPI, FAISS, Sentence Transformers, and Google's FLAN-T5 model.

The API retrieves relevant documents using vector similarity search and generates an AI-powered answer based on the retrieved context.

## Features

- Semantic document search
- Vector embeddings using Sentence Transformers
- FAISS similarity search
- AI answer generation using FLAN-T5
- FastAPI REST API
- Automatic Swagger documentation
- Source document retrieval
- Configurable top-k search results

## Architecture

```text
User Question
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
Context Construction
      │
      ▼
FLAN-T5 Language Model
      │
      ▼
Generated Answer
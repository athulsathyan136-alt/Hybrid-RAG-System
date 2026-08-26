# 🔎 Day 5 — Semantic Search Engine

A semantic search engine built with Python, Sentence Transformers, NumPy, and FAISS.

## Features

- Convert documents into embeddings
- Convert user queries into embeddings
- Search using FAISS
- Return top 5 relevant documents
- Display similarity distance
- Interactive command-line interface

## Technologies

- Python
- Sentence Transformers
- FAISS
- NumPy

## Architecture

User Query
↓
Embedding Model
↓
FAISS Vector Search
↓
Top 5 Relevant Results

## Run

```powershell
.\venv\Scripts\python.exe semantic_search.py
# 🔎 Day 4 — Vector Database Search with FAISS

A beginner-friendly AI project that converts text into embeddings and stores those embeddings in a FAISS vector index for similarity search.

This project is Day 4 of the 30 Days, 30 AI/ML + Cloud Projects portfolio challenge.

---

## 📌 Project Overview

The first four projects build the foundation of a Retrieval-Augmented Generation (RAG) system.

Day 1:

PDF → Text

Day 2:

Text → Chunks

Day 3:

Chunks → Embeddings

Day 4:

Embeddings → Vector Database → Similarity Search

The complete future RAG pipeline will become:

PDF
↓
Text Extraction
↓
Text Chunking
↓
Embedding Generation
↓
Vector Database
↓
Semantic Search
↓
Relevant Context
↓
LLM
↓
Final Answer

---

## 🎯 Project Goal

The goal of this project is to learn how to:

- Generate text embeddings
- Understand vector representations
- Store embeddings
- Create a FAISS vector index
- Perform similarity search
- Find semantically similar text
- Understand vector databases
- Understand semantic search
- Build a foundation for RAG systems

---

## 🚀 Features

- Sentence Transformer embeddings
- FAISS vector index
- Similarity search
- Top-K search results
- Interactive search query
- Distance scores
- Local vector search
- No cloud account required
- RAG foundation

---

## 🧠 What Is an Embedding?

An embedding is a numerical representation of text.

For example:

Python is a popular programming language.

can be converted into a numerical vector:

[0.021, -0.145, 0.087, 0.312, ...]

The vector represents the meaning of the text numerically.

This project uses:

all-MiniLM-L6-v2

The model produces:

384-dimensional embeddings

Conceptually:

Text
↓
Embedding Model
↓
Vector

---

## 🔍 What Is a Vector Database?

A vector database stores numerical vectors and allows applications to search for similar vectors.

Traditional keyword search:

Keyword
↓
Exact matching

Vector search:

Text
↓
Embedding
↓
Meaning
↓
Similarity

Vector search is useful for:

- RAG systems
- AI assistants
- Document search
- Recommendation systems
- Semantic search
- Knowledge bases

---

## 🧠 What Is FAISS?

FAISS stands for:

Facebook AI Similarity Search

FAISS is a library designed for efficient similarity search over vectors.

In this project, FAISS is used to:

1. Create a vector index
2. Store embeddings
3. Convert a query into an embedding
4. Search for similar vectors
5. Return relevant text chunks

---

## 🔄 Project Architecture

DOCUMENT
↓
Text Chunks
↓
Sentence Transformer
↓
Embeddings
↓
FAISS Index
↓
User Question
↓
Query Embedding
↓
FAISS Search
↓
Top K Results
↓
Relevant Chunks

---

## 🛠️ Technologies Used

- Python
- Sentence Transformers
- FAISS
- NumPy
- Git
- GitHub

---


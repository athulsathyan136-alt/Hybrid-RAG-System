# 🚀 Project 20 — RAG Hybrid Search API

A Hybrid Retrieval API that combines **Semantic Search** and **Keyword Search** to provide better document retrieval results.

---

## 📌 Overview

Traditional keyword search finds documents based on matching words.

Semantic search finds documents based on the meaning of the query.

This project combines both approaches into a **Hybrid Search System**.

```text
                 Documents
                     │
                     ▼
               Text Documents
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
   Semantic Search        Keyword Search
          │                     │
 Sentence Transformers        TF-IDF
          │                     │
          └──────────┬──────────┘
                     ▼
              Score Normalization
                     │
                     ▼
               Hybrid Scoring
                     │
                     ▼
               Ranked Results
                     │
                     ▼
                  FastAPI
                     │
                     ▼
                  Swagger
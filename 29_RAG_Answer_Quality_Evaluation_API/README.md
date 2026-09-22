# RAG Answer Quality Evaluation API

## Project 29 — RAG Answer Quality Evaluation API

A lightweight FastAPI project that evaluates the quality of Retrieval-Augmented Generation (RAG) answers using multiple evaluation metrics.

The API analyzes the relationship between the question, generated answer, and retrieved source documents to calculate an overall RAG answer quality score.

## Author

Athul Sathyan

## Overview

A RAG system should not only retrieve information and generate an answer. The generated answer should also be evaluated for relevance, grounding, and source support.

This project combines several RAG evaluation techniques into a single API.

The API evaluates:

* Answer relevance
* Source relevance
* Grounding score
* Citation coverage
* Sentence-level source support
* Overall quality score
* Quality level

The implementation uses pure Python text similarity and does not require heavy machine-learning libraries.

## Features

* FastAPI REST API
* RAG answer quality evaluation
* Answer relevance scoring
* Source relevance scoring
* Grounding score calculation
* Citation coverage calculation
* Sentence-level verification
* Overall quality score
* Quality classification
* Supported sentence detection
* Health check endpoint
* Swagger UI
* Pure Python implementation
* Lightweight dependencies
* No external ML models required

## Architecture

The API follows this workflow:

```
User Question
      |
      v
Generated Answer
      |
      v
Retrieved Sources
      |
      v
+-----------------------------+
|     RAG Evaluation Engine   |
+-----------------------------+
      |
      +--------------------+
      |                    |
      v                    v
Answer Relevance      Source Relevance
      |                    |
      +---------+----------+
                |
                v
          Grounding Score
                |
                v
         Citation Coverage
                |
                v
         Quality Score
                |
                v
   Excellent / Good / Needs Improvement / Poor
```

## Evaluation Metrics

### 1. Answer Relevance

Measures the similarity between the user's question and the generated answer.

A higher value indicates that the generated answer shares more relevant terms with the question.

### 2. Source Relevance

Measures how closely the retrieved sources relate to the original question.

The API calculates the similarity between the question and each source and averages the results.

### 3. Grounding Score

Measures how strongly the generated answer matches the retrieved sources.

The answer is compared against each source and the scores are averaged.

### 4. Citation Coverage

The generated answer is divided into individual sentences.

Each sentence is compared with the combined retrieved sources.

A sentence is considered supported when its similarity score reaches at least 25%.

Citation coverage is calculated as:

```
Supported Sentences / Total Sentences × 100
```

## Quality Score

The overall quality score is calculated using the four evaluation metrics:

```
Quality Score =
(Answer Relevance
 + Source Relevance
 + Grounding Score
 + Citation Coverage) / 4
```

The resulting score is between 0 and 100.

## Quality Levels

The API classifies the final quality score as:

```
80% - 100%   = Excellent
60% - 79.99% = Good
40% - 59.99% = Needs Improvement
0% - 39.99%  = Poor
```

## Technology Stack

* Python
* FastAPI
* Uvicorn
* Pydantic
* Regular Expressions
* Python Counter
* Python Math
* Cosine Similarity
* REST API
* Swagger UI

## Project Structure

```
29_RAG_Answer_Quality_Evaluation_API/
|
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
└── venv/
```

## Installation

Open PowerShell and navigate to the project:

```
cd C:\Users\LENOVO\Hybrid-RAG-System\29_RAG_Answer_Quality_Evaluation_API
```

Create a Python 3.13 virtual environment:

```
py -3.13 -m venv venv
```

Install the dependencies:

```
.\venv\Scripts\python.exe -m pip install --upgrade pip

.\venv\Scripts\python.exe -m pip install fastapi uvicorn
```

## Run the API

Start the FastAPI server:

```
.\venv\Scripts\python.exe -m uvicorn main:app --port 8018
```

The API will run at:

```
http://127.0.0.1:8018
```

## Swagger Documentation

Open the following URL:

```
http://127.0.0.1:8018/docs
```

Swagger UI provides an interactive interface for testing the API.

## API Endpoints

### GET /

Returns basic project information.

Example response:

```
{
  "project": "RAG Answer Quality Evaluation API",
  "status": "running",
  "description": "Evaluate the quality of RAG-generated answers."
}
```

### GET /health

Returns the health status of the API.

Example response:

```
{
  "status": "healthy",
  "evaluation_method": "Pure Python Similarity",
  "external_ml_dependencies": false
}
```

### POST /evaluate

Evaluates the quality of a generated RAG answer.

Request body:

```
{
  "question": "What is Python used for?",
  "answer": "Python is used for web development, automation, data science, and artificial intelligence.",
  "sources": [
    "Python is a popular programming language used for web development, automation, data science, and artificial intelligence.",
    "FastAPI is a modern Python framework used for building high-performance REST APIs.",
    "Docker packages applications and their dependencies into portable containers."
  ]
}
```

## Test Result

The API was tested using a Python-related question and retrieved source documents.

Response:

```
{
  "question": "What is Python used for?",
  "answer": "Python is used for web development, automation, data science, and artificial intelligence.",
  "metrics": {
    "answer_relevance": 51.64,
    "source_relevance": 31.45,
    "grounding_score": 42.75,
    "citation_coverage": 100
  },
  "quality_score": 56.46,
  "quality_level": "Needs Improvement",
  "total_sentences": 1,
```

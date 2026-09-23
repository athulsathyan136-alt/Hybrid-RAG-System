# RAG Evaluation Dashboard API

## Project 30 — RAG Evaluation Dashboard API

A lightweight FastAPI project that provides a complete evaluation dashboard for Retrieval-Augmented Generation (RAG) answers.

This final project combines multiple RAG evaluation concepts developed throughout the project series, including answer relevance, source relevance, grounding, citation coverage, hallucination estimation, confidence scoring, answer verification, and overall quality evaluation.

## Author

Athul Sathyan

## Overview

A RAG application should not only retrieve documents and generate an answer. The generated answer should also be evaluated to determine how well it is supported by the retrieved information.

Project 30 combines multiple evaluation metrics into one API response.

The dashboard evaluates:

* Answer relevance
* Source relevance
* Grounding score
* Citation coverage
* Hallucination percentage
* Confidence score
* Answer verification
* Overall quality score
* Sentence-level source support

The implementation uses pure Python text similarity and does not require heavy machine-learning libraries.

## Features

* FastAPI REST API
* Complete RAG evaluation dashboard
* Answer relevance scoring
* Source relevance scoring
* Grounding evaluation
* Citation coverage calculation
* Hallucination percentage estimation
* Confidence scoring
* Answer verification
* Overall quality scoring
* Sentence-level analysis
* Supported and unsupported sentence detection
* Configurable support threshold
* Confidence classification
* Quality classification
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
+--------------------------------+
|     RAG Evaluation Engine      |
+--------------------------------+
      |
      +--------------------------+
      |                          |
      v                          v
Answer Relevance          Source Relevance
      |                          |
      +------------+-------------+
                   |
                   v
            Grounding Score
                   |
                   v
           Sentence Analysis
                   |
                   v
            Citation Coverage
                   |
                   v
         Hallucination Estimate
                   |
                   v
           Confidence Score
                   |
                   v
          Verification Status
                   |
                   v
            Quality Score
                   |
                   v
            Final Dashboard
```

## Evaluation Metrics

### 1. Answer Relevance

Measures the similarity between the user's question and the generated answer.

A higher score indicates greater lexical overlap between the question and answer.

### 2. Source Relevance

Measures the similarity between the user's question and the retrieved source documents.

The API calculates a similarity score for each source and averages the results.

### 3. Grounding Score

Measures how strongly the generated answer matches the retrieved sources.

The answer is compared against each retrieved source and the scores are averaged.

### 4. Citation Coverage

The answer is divided into individual sentences.

Each sentence is compared against the combined retrieved sources.

A sentence is considered supported when its similarity score is at least 25%.

Citation coverage is calculated as:

```
Supported Sentences / Total Sentences × 100
```

### 5. Hallucination Percentage

The project estimates unsupported content using citation coverage.

The calculation is:

```
Hallucination Percentage =
100 - Citation Coverage
```

This is a similarity-based estimate and is not a factual guarantee.

### 6. Confidence Score

The confidence score combines:

* Answer relevance
* Source relevance
* Grounding score
* Citation coverage

The calculation is:

```
Confidence Score =
(Answer Relevance
 + Source Relevance
 + Grounding Score
 + Citation Coverage) / 4
```

Confidence levels:

```
80% - 100% = High
60% - 79.99% = Medium
0% - 59.99% = Low
```

### 7. Answer Verification

The API determines whether the answer is sufficiently supported.

Verification levels:

```
80% - 100% = Verified
50% - 79.99% = Partially Verified
0% - 49.99% = Not Verified
```

### 8. Quality Score

The overall quality score combines the four primary evaluation metrics:

```
Quality Score =
(Answer Relevance
 + Source Relevance
 + Grounding Score
 + Citation Coverage) / 4
```

Quality levels:

```
80% - 100% = Excellent
60% - 79.99% = Good
40% - 59.99% = Needs Improvement
0% - 39.99% = Poor
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
30_RAG_Evaluation_Dashboard_API/
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
cd C:\Users\LENOVO\Hybrid-RAG-System\30_RAG_Evaluation_Dashboard_API
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
.\venv\Scripts\python.exe -m uvicorn main:app --port 8019
```

The API will run at:

```
http://127.0.0.1:8019
```

## Swagger Documentation

Open:

```
http://127.0.0.1:8019/docs
```

Swagger UI provides an interactive interface for testing the API.

## API Endpoints

### GET /

Returns basic project information.

Example response:

```
{
  "project": "RAG Evaluation Dashboard API",
  "status": "running",
  "description": "Complete evaluation dashboard for RAG answers."
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

Evaluates a RAG answer and returns the complete evaluation dashboard.

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

## Final Test Result

The final Project 30 API was tested successfully.

Response:

```
{
  "project": "RAG Evaluation Dashboard API",
  "question": "What is Python used for?",
  "answer": "Python is used for web development, automation, data science, and artificial intelligence.",
  "dashboard": {
    "answer_relevance": 51.64,
    "source_relevance": 31.45,
    "grounding_score": 42.75,
    "citation_coverage": 100,
    "hallucination_percentage": 0,
    "confidence_score": 56.46,
    "quality_score": 56.46
  },
  "classification": {
    "confidence_level": "Low",
    "verification_status": "Verified",
    "quality_level": "Needs Improvement"
  },
  "sentence_analysis": {
    "total_sentences": 1,
    "supported_sentences": 1,
    "unsupported_sentences": 0,
    "support_threshold": 25,
    "sentence_results": [
      {
        "sentence_number": 1,
        "sentence": "Python is used for web development, automation, data science, and artificial intelligence.",
        "support_score": 69.4,
        "status": "Supported"
      }
    ]
  }
}
```

## Final Test Summary

The Project 30 test produced:

```
Answer Relevance: 51.64%
Source Relevance: 31.45%
Grounding Score: 42.75%
Citation Coverage: 100%
Hallucination Percentage: 0%
Confidence Score: 56.46%
Quality Score: 56.46%
```

Classification:

```
Confidence Level: Low
Verification Status: Verified
Quality Level: Needs Improvement
```

Sentence analysis:

```
Total Sentences: 1
Supported Sentences: 1
Unsupported Sentences: 0
Support Score: 69.4%
```

## Result Interpretation

The test answer contains one sentence.

The sentence achieved a support score of 69.4%, which is above the 25% support threshold.

Therefore, the sentence was classified as:

```
Supported
```

Because all answer sentences were supported, citation coverage was:

```
100%
```

The similarity-based hallucination estimate was:

```
0%
```

The four primary evaluation metrics produced an overall confidence and quality score of:

```
56.46%
```

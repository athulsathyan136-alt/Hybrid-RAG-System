# RAG Answer Verification API

## Project 28 — RAG Answer Verification API

A lightweight FastAPI project that verifies whether a Retrieval-Augmented Generation (RAG) answer is supported by retrieved source documents.

The API analyzes each sentence in the generated answer, compares it with the available sources, and determines whether the answer is supported.

## Author

Athul Sathyan

## Overview

In a RAG system, retrieving documents is not enough. The generated answer should also be checked against the retrieved information.

This project provides an answer verification layer that checks:

* Answer sentences
* Source support
* Similarity scores
* Supported sentence count
* Verification percentage
* Overall verification status

The project uses a pure Python similarity algorithm and does not require heavy machine-learning libraries.

## Features

* FastAPI REST API
* RAG answer verification
* Sentence-level analysis
* Source support detection
* Similarity scoring
* Verification percentage
* Supported sentence counting
* Configurable verification threshold
* Verified / Partially Verified / Not Verified status
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
Split Answer into Sentences
      |
      v
Compare Sentences
      |
      v
Retrieved Sources
      |
      v
Similarity Calculation
      |
      v
Support Detection
      |
      v
Verification Percentage
      |
      v
Verification Status
```

## Verification Process

### Step 1 — Receive Input

The API receives:

* Question
* Generated answer
* Retrieved sources

### Step 2 — Split Answer

The generated answer is divided into individual sentences.

### Step 3 — Compare Sentences

Each answer sentence is compared against the combined retrieved sources.

### Step 4 — Calculate Similarity

The project uses token-based cosine similarity to calculate how closely the answer sentence matches the source information.

### Step 5 — Determine Support

A sentence is considered supported when its similarity score is at least 25%.

The current threshold is:

```
0.25
```

or:

```
25%
```

### Step 6 — Calculate Verification Percentage

The API calculates:

```
Verification Percentage =
Supported Sentences / Total Sentences × 100
```

### Step 7 — Determine Verification Status

The API classifies the answer using:

```
80% - 100%  = Verified
50% - 79.99% = Partially Verified
0% - 49.99% = Not Verified
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
28_RAG_Answer_Verification_API/
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
cd C:\Users\LENOVO\Hybrid-RAG-System\28_RAG_Answer_Verification_API
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
.\venv\Scripts\python.exe -m uvicorn main:app --port 8017
```

The API will run at:

```
http://127.0.0.1:8017
```

## Swagger Documentation

Open:

```
http://127.0.0.1:8017/docs
```

Swagger UI provides an interactive interface for testing the API.

## API Endpoints

### GET /

Returns basic information about the project.

Example response:

```
{
  "project": "RAG Answer Verification API",
  "status": "running",
  "description": "Verify whether a RAG answer is supported by retrieved sources."
}
```

### GET /health

Returns the health status of the API.

Example response:

```
{
  "status": "healthy",
  "verification_method": "Pure Python Similarity",
  "external_ml_dependencies": false
}
```

### POST /verify

Verifies whether the generated answer is supported by the retrieved sources.

Request:

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

The API was tested with the Python question and retrieved sources.

Response:

```
{
  "question": "What is Python used for?",
  "answer": "Python is used for web development, automation, data science, and artificial intelligence.",
  "verification_status": "Verified",
  "verification_percentage": 100,
  "total_sentences": 1,
  "supported_sentences": 1,
  "threshold": 25,
  "sentence_results": [
    {
      "sentence_number": 1,
      "sentence": "Python is used for web development, automation, data science, and artificial intelligence.",
      "support_score": 69.4,
      "status": "Supported"
    }
  ]
}
```

## Result Interpretation

The test produced:

```
Verification Status: Verified
Verification Percentage: 100%
Total Sentences: 1
Supported Sentences: 1
Support Score: 69.4%
Threshold: 25%
```

The answer contains one sentence.

The sentence achieved a support score of 69.4%, which is above the 25% threshold.

Therefore, the sentence was classified as:

```
Supported
```

Because all answer sentences were supported, the final verification result was:

```
Verified
```

## Similarity Algorithm

The project uses token-based cosine similarity.

The input text is converted into lowercase tokens.

Example:

```
Python is used for data science.
```

The text is converted into individual words and their frequencies are counted.

The API then creates numerical vectors and calculates cosine similarity between the answer sentence and the retrieved sources.

The similarity value is converted into a percentage between 0 and 100.

## Verification Threshold

The current support threshold is:

```
25%
```

If:

```
similarity >= 25%
```

the sentence is classified as:

```
Supported
```

If:

```
similarity < 25%
```

the sentence is classified as:

```
Potentially Unsupported
```

The threshold can be changed in the application depending on the desired evaluation strictness.

## Advantages

* Lightweight
* Easy to understand
* Easy to run locally
* No GPU required
* No large AI model required
* No external database required
* No heavy numerical dependencies
* Sentence-level verification
* Useful for learning RAG evaluation
* Easy to integrate with other RAG projects

## Limitations

This project uses lexical similarity rather than semantic embeddings.

Two sentences with the same meaning but different vocabulary may receive a lower similarity score.

The system also does not determine whether the source information itself is factually correct.

Therefore, the verification result should be treated as a supporting evaluation signal rather than a guarantee of factual correctness.

## Future Improvements

Possible improvements include:

* SentenceTransformer semantic embeddings
* Cross-Encoder verification
* LLM-based fact checking
* Claim extraction
* Source-specific verification
* Citation validation
* Hallucination detection integration
* Confidence score integration
* Semantic contradiction detection
* Knowledge graph verification
* RAG monitoring dashboard
* Database storage
* Docker deployment
* AWS deployment
* Production API deployment

## Relation to Previous Projects

This project builds on previous RAG evaluation concepts.

Project 26:

```
RAG Hallucination Detection API
```

Project 27:

```
RAG Confidence Scoring API
```

Project 28:

```
RAG Answer Verification API
```

Together, these projects create multiple evaluation layers for a RAG system.

## Learning Objectives

This project demonstrates:

* FastAPI development
* RAG evaluation
* Answer verification
* Sentence-level processing
* Text similarity
* Cosine similarity
* Source grounding
* Verification thresholds
* REST API design
* Swagger API testing
* Lightweight AI evaluation
* Python text processing

## Project Series

This project is part of:

```
30 Days, 30 Projects: AI/ML + Cloud
```

The series focuses on building practical AI, ML, RAG, Cloud, and MLOps projects for an AI/ML engineering portfolio.

## GitHub

Repository:

```
https://github.com/athulsathyan136-alt/Hybrid-RAG-System
```

Project folder:

```
28_RAG_Answer_Verification_API
```

## Status

Project 28 completed and tested successfully.

API:

```
RAG Answer Verification API
```

Port:

```
8017
```

Verification:

```
Successful
```

Test Result:

```
100% Verified
```

Author:

```
Athul Sathyan
```

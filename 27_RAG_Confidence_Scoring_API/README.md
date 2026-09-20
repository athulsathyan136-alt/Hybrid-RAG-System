# RAG Confidence Scoring API

## Project 27 — RAG Confidence Scoring API

A lightweight FastAPI project that calculates a confidence score for Retrieval-Augmented Generation (RAG) answers using multiple evaluation metrics.

This project analyzes the relationship between the user's question, generated answer, and retrieved source documents to estimate how well-supported the answer is.

## Author

Athul Sathyan

## Overview

The RAG Confidence Scoring API evaluates an answer using four main metrics:

1. Answer Relevance
2. Source Relevance
3. Grounding Score
4. Citation Coverage

These metrics are combined into an overall confidence score.

The project uses a pure Python similarity calculation and does not require heavy machine-learning libraries such as PyTorch, NumPy, SciPy, or scikit-learn.

## Features

* FastAPI REST API
* RAG answer confidence scoring
* Question-to-answer relevance calculation
* Question-to-source relevance calculation
* Answer-to-source grounding calculation
* Sentence-level citation coverage
* Supported sentence detection
* Confidence score calculation
* Confidence level classification
* Health check endpoint
* Pure Python similarity algorithm
* Lightweight dependencies
* Easy to test using Swagger UI

## Architecture

The API follows this workflow:

```
User Question
      |
      v
RAG Answer
      |
      v
Retrieved Sources
      |
      v
Similarity Analysis
      |
      +----------------------+
      |                      |
      v                      v
Answer Relevance       Source Relevance
      |                      |
      +----------+-----------+
                 |
                 v
          Grounding Score
                 |
                 v
         Citation Coverage
                 |
                 v
         Confidence Score
                 |
                 v
      High / Medium / Low
```

## Confidence Metrics

### 1. Answer Relevance

Measures the similarity between the user's question and the generated answer.

Higher similarity indicates that the answer is more closely related to the question.

### 2. Source Relevance

Measures how closely the retrieved sources relate to the original question.

The API calculates similarity between the question and each source and averages the results.

### 3. Grounding Score

Measures how strongly the generated answer is supported by the retrieved sources.

The answer is compared against the available source documents.

### 4. Citation Coverage

The answer is split into individual sentences.

Each sentence is compared with the combined source documents.

A sentence is considered supported when its similarity score is at least 25%.

The API then calculates the percentage of supported sentences.

## Confidence Score

The overall confidence score is calculated using the average of the four metrics:

```
Confidence Score =
(Answer Relevance
 + Source Relevance
 + Grounding Score
 + Citation Coverage) / 4
```

Confidence levels:

```
80% - 100%  = High
60% - 79.99% = Medium
0% - 59.99% = Low
```

## Technology Stack

* Python
* FastAPI
* Uvicorn
* Pydantic
* Regular Expressions
* Python Counter
* Pure Python mathematics
* REST API
* Swagger UI

## Project Structure

```
27_RAG_Confidence_Scoring_API/
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
cd C:\Users\LENOVO\Hybrid-RAG-System\27_RAG_Confidence_Scoring_API
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
.\venv\Scripts\python.exe -m uvicorn main:app --port 8016
```

The API will run at:

```
http://127.0.0.1:8016
```

## Swagger Documentation

Open the following URL in your browser:

```
http://127.0.0.1:8016/docs
```

Swagger UI allows you to test all API endpoints interactively.

## API Endpoints

### GET /

Returns basic project information.

Example response:

```
{
  "project": "RAG Confidence Scoring API",
  "status": "running",
  "description": "Calculate confidence scores for RAG answers."
}
```

### GET /health

Returns the health status of the API.

Example response:

```
{
  "status": "healthy",
  "scoring_method": "Pure Python Similarity",
  "external_ml_dependencies": false
}
```

### POST /confidence

Calculates the confidence score of a RAG answer.

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

Example response from testing:

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
  "confidence_score": 56.46,
  "confidence_level": "Low",
  "total_answer_sentences": 1,
  "supported_sentences": 1,
  "sentence_scores": [
    69.4
  ]
}
```

## Example Interpretation

For the tested question:

```
What is Python used for?
```

The API returned:

```
Answer Relevance: 51.64%
Source Relevance: 31.45%
Grounding Score: 42.75%
Citation Coverage: 100%
Confidence Score: 56.46%
Confidence Level: Low
```

The single answer sentence was detected as supported because its similarity with the combined source documents was above the 25% support threshold.

The overall confidence score was lower because answer relevance, source relevance, and grounding were lower than the citation coverage score.

## Testing

Start the API:

```
.\venv\Scripts\python.exe -m uvicorn main:app --port 8016
```

Then open:

```
http://127.0.0.1:8016/docs
```

Select:

```
POST /confidence
```

Click:

```
Try it out
```

Enter the test JSON and click:

```
Execute
```

The API will return the confidence metrics and overall confidence level.

## How the Algorithm Works

The project uses token-based cosine similarity.

The text is converted into lowercase tokens.

Example:

```
Python is used for data science.
```

becomes approximately:

```
python
is
used
for
data
science
```

The frequency of each word is counted.

The API then calculates the cosine similarity between two text vectors.

The similarity value is converted into a percentage between 0 and 100.

## Sentence Support Threshold

For citation coverage, a sentence is considered supported when:

```
similarity >= 0.25
```

This threshold is currently configured in the application.

The threshold can be modified later to make the evaluation more or less strict.

## Advantages

* Very lightweight
* Easy to understand
* Easy to deploy
* No GPU required
* No large ML model required
* No external database required
* No heavy numerical dependencies
* Useful for understanding RAG evaluation concepts
* Provides multiple confidence metrics

## Limitations

This project uses lexical similarity rather than a semantic embedding model.

Therefore, two sentences with similar meaning but different vocabulary may receive a lower similarity score.

The confidence score should therefore be treated as an evaluation signal rather than a guaranteed measure of factual correctness.

The current implementation also does not verify whether a source is factually correct.

## Future Improvements

Possible improvements include:

* SentenceTransformer embeddings
* Semantic similarity
* Cross-Encoder scoring
* LLM-based evaluation
* Source quality scoring
* Hallucination detection integration
* Citation verification
* Retrieval quality evaluation
* Confidence calibration
* Database storage
* RAG pipeline integration
* Monitoring dashboard
* Production deployment
* AWS deployment
* Docker containerization

## Learning Objectives

This project demonstrates:

* FastAPI API development
* RAG evaluation concepts
* Text similarity
* Cosine similarity
* Sentence-level analysis
* Source grounding
* Citation coverage
* Confidence scoring
* API testing
* Python data processing
* Building lightweight AI evaluation tools

## Project Series

This project is part of the:

```
30 Days, 30 Projects: AI/ML + Cloud
```

The project series focuses on building practical AI, ML, RAG, cloud, and MLOps projects for a professional portfolio.

## GitHub

Repository:

```
https://github.com/athulsathyan136-alt/Hybrid-RAG-System
```

Project folder:

```
27_RAG_Confidence_Scoring_API
```

## Status

Project 27 completed and tested successfully.

API:

```
RAG Confidence Scoring API
```

Port:

```
8016
```

Testing:

```
Successful
```

Author:

```
Athul Sathyan
```

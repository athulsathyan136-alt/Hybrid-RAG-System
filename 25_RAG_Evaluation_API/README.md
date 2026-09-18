# Project 25 — RAG Evaluation & Quality Scoring API

## Author

Athul Sathyan — B.Tech Computer Engineering

## Overview

Project 25 is a **RAG Evaluation & Quality Scoring API** built with FastAPI.

The project evaluates the quality of a Retrieval-Augmented Generation (RAG) answer by comparing:

* The question with the generated answer
* The question with the retrieved sources
* The answer with the retrieved sources
* Overall answer quality

This project demonstrates an important step beyond building RAG systems: **evaluating whether a RAG system is producing relevant and grounded answers**.

## Objectives

The main objectives are:

* Evaluate RAG answer relevance
* Measure source relevance
* Measure answer grounding
* Calculate an overall quality score
* Classify the result as Excellent, Good, Needs Improvement, or Poor
* Evaluate individual retrieved sources
* Build a REST API using FastAPI
* Provide interactive Swagger API documentation
* Avoid heavy machine-learning dependencies for reliable Windows execution

## Architecture

Question + Answer + Sources
→
Text Tokenization
→
TF-IDF Similarity Calculation
→
Question/Answer Relevance
→
Question/Source Relevance
→
Answer/Source Grounding
→
Quality Score
→
Evaluation Result

## Evaluation Metrics

### 1. Answer Relevance

Measures how closely the answer is related to the question.

A higher score means the answer is more relevant to the question.

### 2. Source Relevance

Measures how closely the provided sources relate to the question.

This helps determine whether the RAG retriever selected useful documents.

### 3. Grounding Score

Measures how closely the answer matches the provided sources.

A higher grounding score indicates that the answer is better supported by the retrieved information.

### 4. Overall Quality Score

The overall score is calculated from:

Answer Relevance + Source Relevance + Grounding Score

The three metrics are averaged to produce the final quality score.

## Quality Classification

The API classifies the overall score using these thresholds:

* 80–100: Excellent
* 60–79.99: Good
* 40–59.99: Needs Improvement
* Below 40: Poor

These labels are simple project-level evaluation categories rather than standardized industry benchmarks.

## Technology Stack

* Python
* FastAPI
* Uvicorn
* Pydantic
* TF-IDF-style text weighting
* Cosine similarity
* Regular expressions
* Python Counter
* Python math library

## Why Pure Python?

Earlier RAG projects in this portfolio use libraries such as PyTorch, Sentence Transformers, NumPy, SciPy, and Transformers.

This project uses a lightweight pure-Python similarity implementation instead.

This avoids native machine-learning DLL dependencies and makes the evaluation API easier to run in restricted Windows environments.

The goal of this project is to demonstrate the **evaluation workflow**, not to provide a production-grade embedding benchmark.

## Project Structure

```
25_RAG_Evaluation_API/
│
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
└── venv/
```

## Installation

Navigate to the project directory:

```
cd C:\Users\LENOVO\Hybrid-RAG-System\25_RAG_Evaluation_API
```

Create the virtual environment:

```
py -3.13 -m venv venv
```

Install the dependencies:

```
.\venv\Scripts\python.exe -m pip install --upgrade pip

.\venv\Scripts\python.exe -m pip install fastapi uvicorn
```

## Requirements

The requirements.txt file contains:

```
fastapi
uvicorn
```

## Running the API

Start the FastAPI server:

```
.\venv\Scripts\python.exe -m uvicorn main:app --port 8014
```

The API runs at:

```
http://127.0.0.1:8014
```

## Swagger Documentation

Open:

```
http://127.0.0.1:8014/docs
```

Swagger provides an interactive interface for testing the API.

## API Endpoints

### GET /

Returns basic project information.

Example response:

```
{
    "project": "RAG Evaluation & Quality Scoring API",
    "status": "running",
    "description": "Evaluate RAG answers using pure Python similarity."
}
```

### GET /health

Returns API health information.

Example response:

```
{
    "status": "healthy",
    "evaluation_method": "Pure Python TF-IDF Cosine Similarity",
    "external_ml_dependencies": false
}
```

### POST /evaluate

Evaluates a RAG answer using the supplied question, answer, and source documents.

## Evaluation Request

Example:

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

## Evaluation Process

The `/evaluate` endpoint performs the following operations:

1. Cleans the question and answer
2. Removes empty sources
3. Tokenizes the text
4. Calculates term frequency
5. Calculates inverse-document-frequency-style weights
6. Builds numerical text representations
7. Calculates cosine similarity
8. Measures question-answer relevance
9. Measures question-source relevance
10. Measures answer-source grounding
11. Calculates the overall quality score
12. Classifies the answer quality
13. Evaluates each individual source

## Example Evaluation Result

A successful response contains:

```
{
    "question": "What is Python used for?",
    "answer": "Python is used for web development, automation, data science, and artificial intelligence.",
    "evaluation_method": "Pure Python TF-IDF Cosine Similarity",
    "metrics": {
        "answer_relevance": 80.0,
        "source_relevance": 60.0,
        "grounding_score": 70.0,
        "overall_quality_score": 70.0
    },
    "quality": "Good",
    "source_evaluation": []
}
```

The exact scores depend on the supplied question, answer, and sources.

## Source Evaluation

Each source receives two measurements:

### Question Relevance

How closely the source relates to the original question.

### Answer Similarity

How closely the source matches the generated answer.

Example structure:

```
{
    "source_number": 1,
    "source": "Python is a popular programming language...",
    "question_relevance": 82.5,
    "answer_similarity": 91.2
}
```

## RAG Evaluation Pipeline

The project can be represented as:

```
User Question
      │
      ▼
RAG Generated Answer
      │
      ▼
Retrieved Sources
      │
      ▼
┌─────────────────────────┐
│     Evaluation Engine   │
└─────────────────────────┘
      │
      ├── Answer Relevance
      │
      ├── Source Relevance
      │
      └── Grounding Score
      │
      ▼
Overall Quality Score
      │
      ▼
Quality Classification
```

## Difference Between Retrieval and Evaluation

RAG retrieval answers:

```
"Which documents are relevant to the question?"
```

RAG generation answers:

```
"What answer can be generated using those documents?"
```

RAG evaluation answers:

```
"How relevant and well-grounded is the resulting answer?"
```

This project focuses on the third stage.

## Project Progression

The portfolio RAG projects progressively introduce different capabilities:

```
Project 19
RAG PDF Chatbot + ChromaDB
      ↓
Project 20
Hybrid Search
      ↓
Project 21
Multi-Query Search
      ↓
Project 22
Re-Ranking
      ↓
Project 23
Answer Generation
      ↓
Project 24
Citation & Source Attribution
      ↓
Project 25
RAG Evaluation & Quality Scoring
```

Project 25 therefore adds an evaluation layer to the previous RAG pipeline.

## Error Handling

The API checks for:

* Empty questions
* Empty answers
* Missing sources
* Empty source entries

Examples:

```
{
    "error": "Question cannot be empty."
}

{
    "error": "Answer cannot be empty."
}

{
    "error": "At least one source is required."
}
```

## .gitignore

The project ignores the virtual environment and Python cache files.

Example:

```
venv/
__pycache__/
*.pyc
.env
```

## Skills Demonstrated

This project demonstrates:

* Python programming
* FastAPI development
* REST API design
* Pydantic models
* Text processing
* Tokenization
* TF-IDF-style weighting
* Cosine similarity
* RAG evaluation concepts
* Answer relevance measurement
* Source relevance measurement
* Grounding evaluation
* API testing
* Swagger documentation
* Virtual environment management
* Git and GitHub workflow

## Portfolio Value

This project demonstrates that the developer understands that building a RAG system is not only about retrieving documents and generating answers.

A complete RAG workflow can also require:

* Retrieval
* Generation
* Citation
* Evaluation
* Quality monitoring

This project provides the foundation for adding automated RAG evaluation to larger AI systems.

## Limitations

This implementation is designed for learning and portfolio demonstration.

It does not replace production evaluation frameworks or human evaluation.

The similarity algorithm is based on lexical text similarity. It does not understand semantic meaning as deeply as modern embedding models.

For production systems, evaluation can be extended with:

* Sentence embeddings
* Cross-encoder evaluation
* LLM-as-a-judge
* Faithfulness evaluation
* Context precision
* Context recall
* Answer correctness
* Human evaluation
* Automated benchmark datasets

## Future Improvements

Possible future improvements include:

* Add embedding-based evaluation
* Add LLM-as-a-judge
* Add faithfulness scoring
* Add context precision
* Add context recall
* Add answer correctness
* Add evaluation datasets
* Add batch evaluation
* Add evaluation history
* Store results in PostgreSQL
* Add monitoring dashboards
* Add authentication
* Dockerize the API
* Deploy to AWS
* Add CI/CD with GitHub Actions
* Integrate evaluation into an MLOps pipeline

## Status

Project 25 is a working RAG evaluation API designed for learning, experimentation, and AI/ML portfolio development.

## Summary

Project 25 adds an important evaluation layer to the RAG portfolio.

The system accepts:

```
Question
Answer
Sources
```

and produces:

```
Answer Relevance
Source Relevance
Grounding Score
Overall Quality Score
Quality Classification
Individual Source Evaluation
```

This project provides a foundation for future RAG observability, evaluation, and MLOps systems.

## Author

**Athul Sathyan**

B.Tech Computer Engineering

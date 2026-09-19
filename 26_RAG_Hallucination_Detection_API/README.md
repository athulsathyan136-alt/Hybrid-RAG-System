# Project 26 — RAG Hallucination Detection API

## Author

**Athul Sathyan**

B.Tech Computer Engineering

## Overview

Project 26 is a **RAG Hallucination Detection API** built with FastAPI.

The purpose of this project is to identify potentially unsupported statements in a Retrieval-Augmented Generation (RAG) answer.

A RAG system can retrieve relevant documents and generate an answer, but the generated answer may sometimes contain information that is not supported by the retrieved sources.

This project checks each sentence in the answer against the provided source documents and calculates:

- Sentence support score
- Supported sentences
- Potentially unsupported sentences
- Grounding percentage
- Hallucination percentage
- Hallucination risk level

## Project Objective

The main objective is to build an evaluation layer that can identify potentially unsupported claims in RAG-generated answers.

The system receives:

- A generated answer
- One or more source documents

It then compares the answer sentences against the combined source information.

## RAG Hallucination Detection Pipeline

    RAG Generated Answer
            |
            v
    Split Answer into Sentences
            |
            v
    Compare Each Sentence
            |
            v
    Provided Source Documents
            |
            v
    Similarity Calculation
            |
            v
    Support Score
            |
            +----------------------+
            |                      |
            v                      v
       Supported          Potentially Unsupported
            |                      |
            +----------+-----------+
                       |
                       v
              Grounding Percentage
                       |
                       v
             Hallucination Percentage
                       |
                       v
               Hallucination Risk

## Technologies

- Python
- FastAPI
- Uvicorn
- Pydantic
- Python Regular Expressions
- Python Counter
- Python Math
- Cosine Similarity

## Why Pure Python?

This project intentionally uses a lightweight pure-Python similarity implementation.

It does not require:

- PyTorch
- NumPy
- SciPy
- scikit-learn
- Transformers
- Sentence Transformers

This makes the project easier to run in restricted Windows environments where native machine-learning DLLs may be blocked.

The implementation is designed for learning and portfolio demonstration rather than production-grade semantic evaluation.

## Features

- FastAPI REST API
- Swagger documentation
- Health endpoint
- Hallucination detection endpoint
- Sentence-level analysis
- Source support scoring
- Grounding percentage
- Hallucination percentage
- Risk classification
- Input validation
- Lightweight dependencies

## Project Structure

    26_RAG_Hallucination_Detection_API/
    |
    ├── main.py
    ├── requirements.txt
    ├── .gitignore
    ├── README.md
    └── venv/

## Installation

Navigate to the project:

    cd C:\Users\LENOVO\Hybrid-RAG-System\26_RAG_Hallucination_Detection_API

Create the virtual environment:

    py -3.13 -m venv venv

Upgrade pip:

    .\venv\Scripts\python.exe -m pip install --upgrade pip

Install dependencies:

    .\venv\Scripts\python.exe -m pip install fastapi uvicorn

## Requirements

The `requirements.txt` file contains:

    fastapi
    uvicorn

## Running the API

Start the FastAPI server:

    .\venv\Scripts\python.exe -m uvicorn main:app --port 8015

The API will run at:

    http://127.0.0.1:8015

## Swagger Documentation

Open the following URL in your browser:

    http://127.0.0.1:8015/docs

Swagger provides an interactive interface for testing the API.

## API Endpoints

### GET /

Returns basic information about the project.

Example response:

    {
        "project": "RAG Hallucination Detection API",
        "status": "running",
        "description": "Detect unsupported answer statements using source similarity."
    }

### GET /health

Checks the health of the API.

Example response:

    {
        "status": "healthy",
        "detection_method": "Lexical Cosine Similarity",
        "external_ml_dependencies": false
    }

### POST /detect

Analyzes an answer against the supplied sources.

The endpoint returns:

- Total sentences
- Supported sentences
- Unsupported sentences
- Grounding percentage
- Hallucination percentage
- Hallucination risk
- Sentence-level analysis

## Request Format

Example request:

    {
        "answer": "Python is a programming language used for web development and data science. Python was created by NASA in 1985. Python is also widely used in artificial intelligence.",
        "sources": [
            "Python is a popular programming language used for web development, automation, data science, and artificial intelligence."
        ]
    }

## Testing with Swagger

Open:

    http://127.0.0.1:8015/docs

Select:

    POST /detect

Click:

    Try it out

Paste the example request and click:

    Execute

## Example Detection Scenario

Consider this answer:

    Python is a programming language used for web development and data science.
    Python was created by NASA in 1985.
    Python is also widely used in artificial intelligence.

And the source:

    Python is a popular programming language used for web development,
    automation, data science, and artificial intelligence.

The first and third statements contain information that overlaps strongly with the source.

The NASA statement is not supported by the supplied source.

The system therefore marks that sentence as:

    Potentially Unsupported

This demonstrates how unsupported information can be identified in a RAG response.

## Response Structure

A successful response contains fields similar to:

    {
        "answer": "Python is a programming language...",
        "total_sentences": 3,
        "supported_sentences": 2,
        "unsupported_sentences": 1,
        "grounding_percentage": 66.67,
        "hallucination_percentage": 33.33,
        "hallucination_risk": "Medium",
        "sentence_analysis": [
            {
                "sentence_number": 1,
                "sentence": "Python is a programming language...",
                "support_score": 70.0,
                "status": "Supported"
            }
        ]
    }

The exact values depend on the supplied answer and source documents.

## Similarity Calculation

The project uses a simple lexical cosine similarity algorithm.

The process is:

    Text
      |
      v
    Tokenization
      |
      v
    Word Frequency
      |
      v
    Numerical Vectors
      |
      v
    Cosine Similarity
      |
      v
    Support Score

The score is converted into a percentage for easier interpretation.

## Support Threshold

A sentence is considered:

    Supported

when its similarity score is at least:

    0.25

A sentence below this threshold is classified as:

    Potentially Unsupported

This threshold is a simple project-level rule and can be adjusted depending on the application.

It should not be treated as a universal hallucination-detection standard.

## Grounding Percentage

Grounding percentage represents the proportion of answer sentences that meet the support threshold.

For example:

    Total sentences = 4
    Supported sentences = 3

Then:

    Grounding Percentage = 75%

## Hallucination Percentage

The project calculates:

    Hallucination Percentage =
    100 - Grounding Percentage

For example:

    Grounding Percentage = 75%

Then:

    Hallucination Percentage = 25%

This is an indicator of potentially unsupported content, not proof that a statement is factually false.

## Hallucination Risk

The API assigns a simple risk level:

    0–20%       Low
    20.01–50%   Medium
    Above 50%   High

These thresholds are project-level heuristics.

## Sentence-Level Analysis

Every answer sentence is evaluated independently.

Example:

    {
        "sentence_number": 1,
        "sentence": "Python is used for web development.",
        "support_score": 72.5,
        "status": "Supported"
    }

This makes it possible to identify exactly which parts of an answer may require additional verification.

## Difference Between Hallucination Detection and Fact Checking

Hallucination detection and fact checking are not exactly the same.

Hallucination detection in this project asks:

    "Is this answer statement supported by the provided sources?"

Fact checking asks:

    "Is this statement actually true in the real world?"

A statement may be factually true but still be flagged as unsupported if the provided RAG sources do not contain enough information to support it.

Therefore, this project measures **source grounding**, not universal factual truth.

## RAG Evaluation Progression

This project continues the RAG portfolio progression:

    Project 19
    RAG PDF Chatbot + ChromaDB
          |
          v
    Project 20
    Hybrid Search
          |
          v
    Project 21
    Multi-Query Search
          |
          v
    Project 22
    Re-Ranking
          |
          v
    Project 23
    Answer Generation
          |
          v
    Project 24
    Citation & Source Attribution
          |
          v
    Project 25
    RAG Evaluation & Quality Scoring
          |
          v
    Project 26
    RAG Hallucination Detection

Project 26 adds another important evaluation capability: detecting potentially unsupported answer content.

## Error Handling

The API checks for:

- Empty answers
- Missing sources
- Empty source entries

Example:

    {
        "error": "Answer cannot be empty."
    }

Another example:

    {
        "error": "At least one source is required."
    }

## .gitignore

The project uses:

    venv/
    __pycache__/
    *.pyc
    .env

This prevents virtual-environment files and temporary Python files from being uploaded to GitHub.

## Skills Demonstrated

This project demonstrates:

- Python programming
- FastAPI development
- REST API development
- Pydantic models
- Text processing
- Regular expressions
- Tokenization
- Word-frequency analysis
- Cosine similarity
- Sentence splitting
- RAG evaluation
- Grounding analysis
- Hallucination detection concepts
- API testing
- Swagger documentation
- Virtual environments
- Git and GitHub

## Portfolio Value

Project 26 demonstrates an understanding that RAG systems need more than retrieval and generation.

A production-oriented RAG architecture can include:

    Retrieval
       |
       v
    Re-Ranking
       |
       v
    Generation
       |
       v
    Citation
       |
       v
    Evaluation
       |
       v
    Hallucination Detection
       |
       v
    Monitoring

This project provides the foundation for building more advanced RAG observability and evaluation systems.

## Limitations

This implementation has several limitations.

### Lexical Similarity

The system primarily compares overlapping words.

It does not have the full semantic understanding of modern embedding models.

### No External Knowledge

The system only checks the provided sources.

It does not search the internet or external databases.

### No LLM Judge

The project does not use an LLM to judge whether a statement is supported.

### No Guaranteed Fact Verification

A supported statement is not automatically a verified fact.

The system only measures similarity to the supplied sources.

### Threshold-Based Classification

The 0.25 support threshold is a simple heuristic.

Real-world systems should calibrate thresholds using evaluation datasets.

## Future Improvements

Possible future improvements include:

- Sentence Transformer embeddings
- Cross-encoder support evaluation
- LLM-as-a-judge
- Fact-checking integration
- Web search verification
- Citation-level verification
- Claim extraction
- Entity-level verification
- RAGAS integration
- TruLens integration
- LangSmith integration
- Evaluation datasets
- Automated regression testing
- RAG monitoring dashboard
- PostgreSQL evaluation history
- Docker deployment
- AWS deployment
- GitHub Actions CI/CD
- MLOps monitoring

## Production RAG Evaluation

A more advanced production architecture could be:

    User Question
          |
          v
    Document Retrieval
          |
          v
    Re-Ranking
          |
          v
    Answer Generation
          |
          v
    Claim Extraction
          |
          v
    Source Verification
          |
          v
    Hallucination Detection
          |
          v
    Confidence Score
          |
          v
    Monitoring Dashboard

Project 26 represents the hallucination-detection stage of this architecture.

## Security Considerations

For production deployment, additional security should be implemented:

- Authentication
- Authorization
- Input validation
- Rate limiting
- Logging
- API key management
- Secure environment variables
- HTTPS
- Request size limits
- Monitoring

## Learning Outcome

After completing this project, the developer understands:

- Why RAG answers need grounding checks
- How unsupported statements can occur
- How source grounding can be measured
- How to evaluate individual answer sentences
- How similarity can be used for basic support detection
- Why hallucination detection is different from fact checking
- How evaluation can be added to a RAG pipeline

## Project Status

**Project 26 — RAG Hallucination Detection API**

Status:

    Completed

The API provides a lightweight demonstration of source-grounding and potentially unsupported statement detection.

## Summary

Project 26 extends the RAG portfolio from answer evaluation into hallucination detection.

The API accepts:

    Answer
    Sources

and produces:

    Sentence Analysis
    Support Scores
    Supported Sentence Count
    Unsupported Sentence Count
    Grounding Percentage
    Hallucination Percentage
    Hallucination Risk

This project provides a foundation for future work in:

- RAG evaluation
- AI reliability
- AI observability
- LLM evaluation
- MLOps
- Production AI monitoring

## Author

**Athul Sathyan**

B.Tech Computer Engineering
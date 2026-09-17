# 🚀 Project 24 — RAG Citation & Source Attribution API

A Retrieval-Augmented Generation (RAG) API built with FastAPI that retrieves relevant documents using semantic similarity, generates answers using a language model, and provides structured source citations with similarity scores.

## 👨‍💻 Author

**Athul Sathyan**
B.Tech Computer Engineering

GitHub: https://github.com/athulsathyan136-alt

## 📌 Project Overview

Traditional RAG systems retrieve information and generate an answer, but users may not know where the answer came from.

This project adds a citation and source attribution layer to the RAG pipeline.

The API returns:

* Generated answer
* Retrieval method
* Generation model
* Number of retrieved documents
* Citation identifiers
* Source IDs
* Source titles
* Similarity scores
* Original source content

## 🎯 Project Goals

* Build a RAG-based API using FastAPI.
* Retrieve relevant documents using semantic similarity.
* Generate answers from retrieved information.
* Provide source citations with answers.
* Return similarity scores for retrieved sources.
* Make generated answers traceable to their sources.
* Provide interactive Swagger API documentation.

## 🏗️ System Architecture

```text
User Question
      │
      ▼
FastAPI REST API
      │
      ▼
Semantic Retrieval
      │
      ▼
Relevant Documents
      │
      ▼
Similarity Scores
      │
      ▼
Answer Generation
      │
      ▼
Citation & Source Attribution
      │
      ▼
Structured JSON Response
```

## 🔄 RAG Pipeline

```text
Question
   ↓
Semantic Retrieval
   ↓
Similarity Search
   ↓
Top Relevant Documents
   ↓
Context Construction
   ↓
Language Model
   ↓
Generated Answer
   ↓
Citation Mapping
   ↓
Final JSON Response
```

## 🧠 Key Features

### 🔎 Semantic Retrieval

The system retrieves relevant documents using semantic similarity.

### 📚 Source Attribution

Each retrieved document receives a citation identifier.

Example:

```text
[1] Python
[2] FastAPI
[4] Natural Language Processing
```

### 📊 Similarity Scores

Each source includes a similarity score representing its relevance to the question.

Example:

```text
Python
Similarity Score: 0.8262
```

### 🤖 Answer Generation

The current project uses:

```text
distilgpt2
```

for answer generation.

### 🌐 FastAPI

FastAPI provides the REST API and automatic Swagger/OpenAPI documentation.

### 📦 Structured JSON

The API returns the answer together with citation and source information.

## 🛠️ Technologies Used

* Python
* FastAPI
* Uvicorn
* Retrieval-Augmented Generation
* Semantic Similarity
* Natural Language Processing
* DistilGPT2
* Vector Retrieval
* REST API
* Swagger / OpenAPI
* JSON

## 📁 Project Structure

```text
24_RAG_Citation_Source_Attribution_API/
│
├── main.py
├── rag_citation.py
├── requirements.txt
├── README.md
│
├── documents/
│
└── chroma_db/
```

## ⚙️ Requirements

* Python 3.10+
* pip
* FastAPI
* Uvicorn
* PyTorch
* Transformers
* Sentence Transformers
* ChromaDB

## 🚀 Installation

Navigate to the project directory:

```powershell
cd C:\Users\LENOVO\Hybrid-RAG-System\24_RAG_Citation_Source_Attribution_API
```

Install the required packages:

```powershell
..\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## ▶️ Run the API

Start the FastAPI server:

```powershell
..\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8009
```

The API will run at:

```text
http://127.0.0.1:8009
```

## 📖 Swagger Documentation

Open:

```text
http://127.0.0.1:8009/docs
```

Swagger provides an interactive interface for testing the API.

## 🧪 API Test

Example question:

```text
What is Python used for?
```

The API performs semantic retrieval and generates a response with citations and source information.

## 📤 Example API Response

```json
{
  "question": "What is Python used for?",
  "answer": "Python is a popular programming language used for web development, automation, data science, and artificial intelligence.\n[Source 5] Python: Python is a popular programming language used for web development, automation, data science, and artificial intelligence.\n[Source 6] Python: Python is a popular programming language used for web development, automation, data science, and artificial intelligence.\n[Source 7] Python: Python is a popular programming language used for web development, automation, data science, and artificial",
  "retrieval_method": "Semantic Similarity",
  "generation_model": "distilgpt2",
  "retrieved_documents": 3,
  "citations": [
    {
      "citation": "[1]",
      "source_id": 1,
      "title": "Python",
      "similarity_score": 0.8262
    },
    {
      "citation": "[2]",
      "source_id": 2,
      "title": "FastAPI",
      "similarity_score": 0.4783
    },
    {
      "citation": "[4]",
      "source_id": 4,
      "title": "Natural Language Processing",
      "similarity_score": 0.3125
    }
  ],
  "sources": [
    {
      "source_id": 1,
      "title": "Python",
      "content": "Python is a popular programming language used for web development, automation, data science, and artificial intelligence.",
      "similarity_score": 0.8262
    },
    {
      "source_id": 2,
      "title": "FastAPI",
      "content": "FastAPI is a modern Python framework used for building high-performance REST APIs.",
      "similarity_score": 0.4783
    },
    {
      "source_id": 4,
      "title": "Natural Language Processing",
      "content": "Natural language processing enables computers to understand and process human language.",
      "similarity_score": 0.3125
    }
  ]
}
```

## 📊 Retrieved Sources

### Source 1 — Python

```text
Source ID: 1
Title: Python
Similarity Score: 0.8262
```

Content:

```text
Python is a popular programming language used for web development, automation, data science, and artificial intelligence.
```

### Source 2 — FastAPI

```text
Source ID: 2
Title: FastAPI
Similarity Score: 0.4783
```

Content:

```text
FastAPI is a modern Python framework used for building high-performance REST APIs.
```

### Source 4 — Natural Language Processing

```text
Source ID: 4
Title: Natural Language Processing
Similarity Score: 0.3125
```

Content:

```text
Natural language processing enables computers to understand and process human language.
```

## 🔗 Citation System

The citation system connects the generated answer with the retrieved sources.

```text
Generated Answer
       │
       ├── [1]
       │     └── Python
       │
       ├── [2]
       │     └── FastAPI
       │
       └── [4]
             └── Natural Language Processing
```

Each citation contains:

* Citation ID
* Source ID
* Title
* Similarity Score

This makes the retrieved information traceable to its source.

## 📈 Retrieval Results

For the test question:

```text
What is Python used for?
```

The system returned:

```text
Retrieval Method: Semantic Similarity
Generation Model: distilgpt2
Retrieved Documents: 3
```

Top retrieved source:

```text
Title: Python
Similarity Score: 0.8262
```

The Python source was the most similar retrieved document for the test question.

## 💡 Why Citation Matters in RAG

A RAG system can generate useful answers, but without source attribution it can be difficult to understand where information originated.

Citation-based RAG provides:

```text
Answer
   +
Source
   +
Similarity
   +
Traceability
```

This is useful for:

* Enterprise AI
* Document search
* Knowledge bases
* Research assistants
* Customer support
* Internal AI assistants
* AI copilots
* Compliance-oriented applications

## 🧩 RAG Components

```text
┌──────────────────────────────┐
│          User Query          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Semantic Retrieval       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Relevant Documents       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Context Creation        │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Language Model         │
│          distilgpt2          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│    Citation Attribution      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       JSON API Response      │
└──────────────────────────────┘
```

## 🧪 Testing Checklist

```text
☑ FastAPI starts successfully
☑ Swagger UI opens
☑ Question endpoint works
☑ Semantic retrieval works
☑ Relevant documents are returned
☑ Similarity scores are returned
☑ Citations are returned
☑ Source content is returned
☑ Answer generation works
☑ JSON response is valid
```

## ⚠️ Current Citation Improvement

The current generated answer contains model-generated source labels such as:

```text
[Source 5]
[Source 6]
[Source 7]
```

while the structured citation system uses:

```text
[1]
[2]
[4]
```

The next improvement is to make the generated answer use the same citation identifiers as the structured citation array.

For example:

```text
Python is used for web development, automation,
data science, and artificial intelligence. [1]
```

with:

```text
[1] Python
Similarity Score: 0.8262
```

This will make the citation system more consistent and production-ready.

## 🚀 Future Improvements

* Consistent citation numbering
* PDF document upload
* Multiple document support
* Page-level citations
* Chunk-level citations
* ChromaDB persistence
* Improved generation models
* Reranking
* Hybrid search
* Metadata filtering
* Authentication
* API key security
* Docker deployment
* AWS deployment
* CI/CD pipeline
* Cloud monitoring
* Frontend chat interface
* Citation highlighting
* Source preview
* RAG evaluation metrics

## ☁️ Future Cloud Deployment

The API can later be deployed using:

```text
FastAPI
   ↓
Docker
   ↓
Amazon ECR
   ↓
AWS ECS / EKS
   ↓
Cloud RAG API
```

Possible deployment platforms:

* AWS
* Microsoft Azure
* Google Cloud
* Render
* Hugging Face Spaces

## 💼 Career Relevance

This project demonstrates practical skills relevant to:

* AI/ML Engineering
* Generative AI
* RAG Engineering
* LLM Applications
* NLP
* Backend Engineering
* FastAPI Development
* Vector Search
* Cloud AI Engineering
* MLOps

The project demonstrates how an AI application can provide an answer together with information about the sources used during retrieval.

## 📚 Concepts Learned

Through this project, I practiced:

* Retrieval-Augmented Generation
* Semantic Similarity
* Vector Retrieval
* Source Attribution
* Citation Generation
* Natural Language Processing
* Language Models
* FastAPI
* REST APIs
* JSON APIs
* Swagger
* AI Application Architecture

## 🧪 Example Run

```text
Question:
What is Python used for?

Retrieval Method:
Semantic Similarity

Generation Model:
distilgpt2

Retrieved Documents:
3

Top Source:
Python

Similarity Score:
0.8262
```

## 📌 Project Status

```text
Project: 24
Name: RAG Citation & Source Attribution API
Status: Completed
API: Working
Semantic Retrieval: Working
Answer Generation: Working
Citations: Working
Source Attribution: Working
Swagger: Working
```

## 📈 Portfolio Progress

This project is part of my:

```text
30 Days, 30 Projects
AI/ML + Cloud Engineering Portfolio
```

The portfolio focuses on practical skills across:

```text
Python
SQL
Machine Learning
Deep Learning
Generative AI
RAG
LLMs
FastAPI
Docker
AWS
Cloud
MLOps
```

## 👨‍💻 Author

**Athul Sathyan**

B.Tech Computer Engineering

GitHub:

https://github.com/athulsathyan136-alt

## 📄 License

This project is intended for educational and portfolio purposes.

## ⭐ Project 24 Complete

**RAG Citation & Source Attribution API**

Built with:

```text
Python + FastAPI + RAG + Semantic Retrieval + distilgpt2 + Source Citations
```

🚀 **Built by Athul Sathyan**

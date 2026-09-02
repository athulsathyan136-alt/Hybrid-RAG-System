\# 🚀 RAG Query API



A production-style \*\*FastAPI query service\*\* that connects to a Retrieval-Augmented Generation (RAG) backend and provides a clean API for asking questions about uploaded documents.



This project is \*\*Project 12\*\* in the Hybrid RAG System portfolio.



\---



\## 📌 Project Overview



The RAG Query API acts as a dedicated query layer between the user and the RAG Document Upload API.



Instead of directly loading the embedding model and FAISS index, this service sends questions to \*\*Project 11 — RAG Document Upload API\*\*, which performs:



\* Semantic search

\* FAISS vector retrieval

\* Context extraction

\* LLM-based answer generation



The Query API then returns the final answer to the client.



\---



\## 🏗️ Architecture



```text

&#x20;               User

&#x20;                 │

&#x20;                 ▼

&#x20;       ┌───────────────────┐

&#x20;       │   RAG Query API   │

&#x20;       │    Port: 8000     │

&#x20;       └─────────┬─────────┘

&#x20;                 │

&#x20;                 │ POST /ask

&#x20;                 ▼

&#x20;       ┌───────────────────────┐

&#x20;       │ RAG Document Upload   │

&#x20;       │       API             │

&#x20;       │     Port: 8001        │

&#x20;       └──────────┬────────────┘

&#x20;                  │

&#x20;                  ▼

&#x20;           Semantic Search

&#x20;                  │

&#x20;                  ▼

&#x20;            FAISS Index

&#x20;                  │

&#x20;                  ▼

&#x20;         Relevant Documents

&#x20;                  │

&#x20;                  ▼

&#x20;            FLAN-T5 LLM

&#x20;                  │

&#x20;                  ▼

&#x20;              Answer

```



\---



\## ✨ Features



\* FastAPI-based REST API

\* Dedicated query endpoint

\* Communication with another FastAPI service

\* Pydantic request validation

\* HTTP error handling

\* Connection error handling

\* Request timeout handling

\* Clean JSON responses

\* Swagger API documentation

\* Microservice-style architecture



\---



\## 🛠️ Technologies



| Technology                | Purpose                  |

| ------------------------- | ------------------------ |

| Python                    | Programming language     |

| FastAPI                   | API framework            |

| Uvicorn                   | ASGI server              |

| Pydantic                  | Request validation       |

| Requests                  | API-to-API communication |

| FAISS                     | Vector similarity search |

| Sentence Transformers     | Embeddings               |

| Hugging Face Transformers | LLM generation           |

| FLAN-T5                   | Answer generation        |



\---



\## 📁 Project Structure



```text

12\_RAG\_Query\_API/

│

├── data/

│   ├── chunks.json

│   └── faiss.index

│

├── main.py

├── requirements.txt

├── README.md

├── .gitignore

└── venv/

```



> `venv/` is excluded from GitHub using `.gitignore`.



\---



\## ⚙️ Installation



Clone the repository:



```bash

git clone https://github.com/athulsathyan136-alt/Hybrid-RAG-System.git

```



Go to the Project 12 directory:



```bash

cd Hybrid-RAG-System/12\_RAG\_Query\_API

```



Create a virtual environment:



```bash

python -m venv venv

```



Activate it on Windows PowerShell:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



Install dependencies:



```bash

pip install -r requirements.txt

```



\---



\## 🔗 Project 11 Dependency



This project communicates with:



```text

http://127.0.0.1:8001

```



Therefore, \*\*Project 11 must be running before testing `/query`.\*\*



Start Project 11:



```powershell

cd ..\\11\_RAG\_Document\_Upload\_API

.\\venv\\Scripts\\python.exe -m uvicorn main:app --reload --port 8001

```



\---



\## ▶️ Run Project 12



Open another PowerShell terminal:



```powershell

cd C:\\Users\\LENOVO\\Hybrid-RAG-System\\12\_RAG\_Query\_API

```



Run:



```powershell

.\\venv\\Scripts\\python.exe -m uvicorn main:app --reload --port 8000

```



The API will be available at:



```text

http://127.0.0.1:8000

```



\---



\## 📚 Swagger Documentation



Open:



```text

http://127.0.0.1:8000/docs

```



Swagger provides an interactive interface for testing the API.



\---



\## 🔍 API Endpoints



\### GET `/`



Checks whether the API is running.



Example response:



```json

{

&#x20; "message": "RAG Query API is running",

&#x20; "backend": "http://127.0.0.1:8001"

}

```



\---



\### POST `/query`



Sends a question to the RAG backend.



Request:



```json

{

&#x20; "question": "What is Python?"

}

```



Example response:



```json

{

&#x20; "question": "What is Python?",

&#x20; "answer": "Python"

}

```



\---



\## 🧪 Testing with PowerShell



Test the home endpoint:



```powershell

Invoke-RestMethod http://127.0.0.1:8000/

```



Test the query endpoint:



```powershell

Invoke-RestMethod `

&#x20; -Uri http://127.0.0.1:8000/query `

&#x20; -Method POST `

&#x20; -ContentType "application/json" `

&#x20; -Body '{"question":"What is Python?"}'

```



\---



\## 🔄 Request Flow



1\. User sends a question to `/query`.

2\. Project 12 validates the request.

3\. Project 12 sends the question to Project 11.

4\. Project 11 performs semantic search.

5\. FAISS retrieves relevant document chunks.

6\. Relevant context is sent to FLAN-T5.

7\. FLAN-T5 generates an answer.

8\. Project 11 returns the answer.

9\. Project 12 returns the final response to the user.



\---



\## 🧠 RAG Pipeline



```text

Question

&#x20;  ↓

Query API

&#x20;  ↓

RAG Backend

&#x20;  ↓

Embedding

&#x20;  ↓

FAISS Similarity Search

&#x20;  ↓

Relevant Chunks

&#x20;  ↓

Context

&#x20;  ↓

FLAN-T5

&#x20;  ↓

Generated Answer

```



\---



\## ⚠️ Error Handling



The API handles:



\* Empty questions

\* Backend connection failures

\* Backend timeouts

\* HTTP errors

\* Unexpected exceptions



Example:



```json

{

&#x20; "error": "Could not connect to Project 11 RAG API.",

&#x20; "backend": "http://127.0.0.1:8001"

}

```



\---



\## 🎯 Learning Objectives



This project demonstrates:



\* FastAPI microservices

\* REST API design

\* API-to-API communication

\* Pydantic validation

\* RAG architecture

\* Vector search integration

\* Error handling

\* Service separation

\* AI backend integration



\---



\## 🚀 Future Improvements



\* Authentication

\* API keys

\* Docker containerization

\* Redis caching

\* PostgreSQL integration

\* Streaming responses

\* Cloud deployment

\* AWS ECS deployment

\* AWS API Gateway

\* CI/CD with GitHub Actions

\* Monitoring and logging



\---



\## 👨‍💻 Author



\*\*Athul Sathyan\*\*



GitHub:



https://github.com/athulsathyan136-alt



\---



\## ⭐ Portfolio Project



Part of the \*\*Hybrid RAG System — AI/ML + Cloud Portfolio\*\*.



Project 12 focuses on building a dedicated query microservice for a Retrieval-Augmented Generation system.




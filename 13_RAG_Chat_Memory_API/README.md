\# 🚀 RAG Chat Memory API



A FastAPI-based conversational API that connects to a Retrieval-Augmented Generation (RAG) system and maintains conversation history.



This is \*\*Project 13\*\* in the Hybrid RAG System portfolio.



\## 📌 Project Overview



The RAG Chat Memory API provides a chatbot interface on top of the existing RAG services.



It receives a user's question, sends it to the RAG Query API, receives the generated answer, and stores both the question and answer in conversation memory.



\## 🏗️ Architecture



```text

User

&#x20;↓

RAG Chat Memory API

Port 8002

&#x20;↓

RAG Query API

Port 8000

&#x20;↓

RAG Document Upload API

Port 8001

&#x20;↓

FAISS Vector Search

&#x20;↓

Relevant Document Chunks

&#x20;↓

FLAN-T5

&#x20;↓

Generated Answer

```



\## ✨ Features



\* FastAPI REST API

\* Conversational chat endpoint

\* Conversation memory

\* Conversation history endpoint

\* Clear conversation endpoint

\* API-to-API communication

\* Pydantic request validation

\* Error handling

\* Swagger documentation

\* Microservice-style RAG architecture



\## 🛠️ Technologies



| Technology                | Purpose               |

| ------------------------- | --------------------- |

| Python                    | Programming language  |

| FastAPI                   | REST API framework    |

| Uvicorn                   | ASGI server           |

| Pydantic                  | Request validation    |

| Requests                  | Service communication |

| FAISS                     | Vector search         |

| Sentence Transformers     | Embeddings            |

| Hugging Face Transformers | Text generation       |

| FLAN-T5                   | Answer generation     |



\## 📁 Project Structure



```text

13\_RAG\_Chat\_Memory\_API/

│

├── main.py

├── requirements.txt

├── README.md

├── .gitignore

└── venv/

```



The `venv/` directory is excluded from Git using `.gitignore`.



\## ⚙️ Installation



Clone the repository:



```bash

git clone https://github.com/athulsathyan136-alt/Hybrid-RAG-System.git

```



Enter the project:



```bash

cd Hybrid-RAG-System/13\_RAG\_Chat\_Memory\_API

```



Create a virtual environment:



```bash

python -m venv venv

```



Install dependencies:



```bash

pip install -r requirements.txt

```



\## 🔗 Required Services



Project 13 communicates with Project 12:



```text

http://127.0.0.1:8000/query

```



Project 12 communicates with Project 11:



```text

http://127.0.0.1:8001

```



Therefore, Project 11 and Project 12 must be running before using the chat API.



\## ▶️ Run the API



Start Project 13:



```powershell

.\\venv\\Scripts\\python.exe -m uvicorn main:app --port 8002

```



The API will be available at:



```text

http://127.0.0.1:8002

```



\## 📚 Swagger Documentation



Open:



```text

http://127.0.0.1:8002/docs

```



Swagger provides an interactive interface for testing the API.



\## 💬 Chat Endpoint



\### POST `/chat`



Send a question to the RAG system.



Request:



```json

{

&#x20; "question": "Why is Python useful?"

}

```



Example response:



```json

{

&#x20; "question": "Why is Python useful?",

&#x20; "answer": "Python is useful...",

&#x20; "memory\_messages": 2

}

```



The question and answer are stored in conversation memory.



\## 🧠 Conversation History



\### GET `/history`



Returns the stored conversation.



Example:



```json

{

&#x20; "conversation": \[

&#x20;   {

&#x20;     "role": "user",

&#x20;     "message": "Why is Python useful?"

&#x20;   },

&#x20;   {

&#x20;     "role": "assistant",

&#x20;     "message": "Python is useful..."

&#x20;   }

&#x20; ],

&#x20; "total\_messages": 2

}

```



\## 🗑️ Clear Conversation



\### DELETE `/history`



Clears the current conversation memory.



Example response:



```json

{

&#x20; "message": "Conversation memory cleared"

}

```



After clearing:



```json

{

&#x20; "conversation": \[],

&#x20; "total\_messages": 0

}

```



\## 🧪 PowerShell Testing



Test the API:



```powershell

Invoke-RestMethod http://127.0.0.1:8002/

```



Ask a question:



```powershell

Invoke-RestMethod `

&#x20; -Uri http://127.0.0.1:8002/chat `

&#x20; -Method POST `

&#x20; -ContentType "application/json" `

&#x20; -Body '{"question":"Why is Python useful?"}'

```



View history:



```powershell

Invoke-RestMethod http://127.0.0.1:8002/history

```



Clear history:



```powershell

Invoke-RestMethod `

&#x20; -Uri http://127.0.0.1:8002/history `

&#x20; -Method DELETE

```



\## 🔄 Request Flow



1\. User sends a question to `/chat`.

2\. Project 13 validates the request.

3\. Project 13 sends the question to Project 12.

4\. Project 12 sends the query to the RAG backend.

5\. Relevant document information is retrieved.

6\. The RAG system generates an answer.

7\. Project 13 receives the answer.

8\. The question and answer are stored in memory.

9\. The API returns the answer and memory count.



\## 🎯 Learning Objectives



This project demonstrates:



\* Conversational AI APIs

\* FastAPI development

\* REST API communication

\* Microservice architecture

\* RAG integration

\* Conversation state management

\* API error handling

\* Pydantic validation

\* Swagger/OpenAPI

\* Multi-service AI architecture



\## ⚠️ Current Limitation



Conversation memory is currently stored in Python memory.



Therefore:



\* Memory is temporary.

\* Restarting the API clears the conversation.

\* Memory is not shared between multiple server instances.



\## 🚀 Future Improvements



\* Redis conversation memory

\* PostgreSQL conversation storage

\* User authentication

\* User-specific chat sessions

\* Streaming responses

\* Conversation summarization

\* Long-term memory

\* Docker deployment

\* AWS ECS deployment

\* API Gateway

\* GitHub Actions CI/CD

\* Monitoring and logging



\## 👨‍💻 Author



\*\*Athul Sathyan\*\*



GitHub:



https://github.com/athulsathyan136-alt



\## ⭐ Portfolio



Part of the \*\*Hybrid RAG System — AI/ML + Cloud Portfolio\*\*.



Project 13 demonstrates how a RAG system can be extended into a conversational AI service with temporary conversation memory.




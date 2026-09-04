# RAG Conversation Database API

A FastAPI-based application that integrates a Retrieval-Augmented Generation (RAG) system with a SQLite database to permanently store user questions and AI-generated responses.

## Project Overview

This project extends the previous RAG API by adding persistent conversation storage.

When a user sends a question:

1. The question is sent to the RAG Query API.
2. The RAG system retrieves relevant information.
3. An AI-generated answer is returned.
4. Both the user question and AI answer are stored in a SQLite database.

Unlike an in-memory chat application, conversation data remains available even after restarting the API server.

## Architecture

```text
User
 │
 ▼
Project 14 - Conversation Database API
Port: 8003
 │
 ▼
Project 12 - RAG Query API
Port: 8000
 │
 ▼
Project 11 - RAG Document Upload API
Port: 8001
 │
 ▼
Document Processing and Retrieval
 │
 ▼
AI Answer
 │
 ▼
SQLite Database
```

## Features

* FastAPI REST API
* SQLite database integration
* SQLAlchemy ORM
* Persistent conversation storage
* Integration with RAG Query API
* Save user questions
* Save AI-generated answers
* Retrieve conversation history
* Delete conversation history
* Automatic database table creation

## Technologies Used

* Python
* FastAPI
* SQLite
* SQLAlchemy
* Pydantic
* Requests
* Uvicorn

## Project Structure

```text
14_RAG_Conversation_Database_API
│
├── database.py
├── main.py
├── models.py
├── schemas.py
├── requirements.txt
├── .gitignore
├── README.md
└── conversations.db
```

## Installation

Clone the repository:

```bash
git clone https://github.com/athulsathyan136-alt/Hybrid-RAG-System.git
```

Navigate to the project:

```bash
cd Hybrid-RAG-System/14_RAG_Conversation_Database_API
```

Create a virtual environment:

```bash
python -m venv venv
```

Install dependencies:

```bash
venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Running the API

Start the server:

```bash
venv\Scripts\python.exe -m uvicorn main:app --port 8003
```

The API will be available at:

```text
http://127.0.0.1:8003
```

Interactive API documentation:

```text
http://127.0.0.1:8003/docs
```

## API Endpoints

### Home

```http
GET /
```

Returns the API status.

### Chat

```http
POST /chat
```

Example request:

```json
{
  "question": "Why is Python useful?"
}
```

The API sends the question to the RAG system and stores both the question and answer in the SQLite database.

### Get Conversation History

```http
GET /history
```

Returns all stored conversation messages.

### Clear Conversation History

```http
DELETE /history
```

Deletes all stored conversation records.

## Example Conversation Record

```json
{
  "message": "Why is Python useful?",
  "role": "user",
  "id": 1
}
```

```json
{
  "message": "Python community is essential to program",
  "role": "assistant",
  "id": 2
}
```

## Database

The project uses SQLite for persistent storage.

The database file is automatically created when the application starts:

```text
conversations.db
```

The database stores:

* Message ID
* User or assistant role
* Message content
* Creation timestamp

## Related Projects

This project is part of the Hybrid RAG System portfolio.

* Project 11: RAG Document Upload API
* Project 12: RAG Query API
* Project 13: RAG Chat Memory API
* Project 14: RAG Conversation Database API

## Author

Athul Sathyan

GitHub: https://github.com/athulsathyan136-alt

## License

This project is created for educational and portfolio purposes.

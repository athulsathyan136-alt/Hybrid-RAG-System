# 📄 PDF Text Extractor API

A simple REST API built with Python and FastAPI that allows users to upload PDF files and automatically extract their text.

This project is Day 1 of the 30 Days, 30 AI/ML + Cloud Projects portfolio challenge.

## 🚀 Features

- Upload PDF files
- Extract text from PDF pages
- Count total PDF pages
- Count extracted characters
- Return a text preview
- Reject non-PDF files
- Fast API response
- Interactive Swagger API documentation
- Error handling for invalid files
- Python-based backend

## 🛠️ Technologies Used

- Python
- FastAPI
- Uvicorn
- pypdf
- python-multipart
- Git
- GitHub

## 📁 Project Structure

01_PDF_Text_Extractor_API/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── venv/

The venv folder is excluded from GitHub using .gitignore.

## ⚙️ Installation

Clone the main repository:

    git clone https://github.com/athulsathyan136-alt/Hybrid-RAG-System.git

Open the project:

    cd Hybrid-RAG-System/01_PDF_Text_Extractor_API

Create a virtual environment:

    python -m venv venv

Install the required packages:

    pip install -r requirements.txt

If PowerShell allows virtual environment activation:

    .\venv\Scripts\Activate.ps1

If PowerShell blocks activation, you can run the project directly using:

    .\venv\Scripts\python.exe -m uvicorn main:app --reload

## ▶️ Run the API

Start the FastAPI server:

    uvicorn main:app --reload

Or without activating the virtual environment:

    .\venv\Scripts\python.exe -m uvicorn main:app --reload

The API will be available at:

    http://127.0.0.1:8000

## 📚 Swagger Documentation

FastAPI automatically creates interactive API documentation.

Open the following URL in your browser:

    http://127.0.0.1:8000/docs

You will see the available API endpoints and can test them directly from the browser.

## 🔗 API Endpoints

### GET /

Checks whether the API is running.

Example response:

    {
        "message": "PDF Text Extractor API is running"
    }

### POST /extract-text

Uploads a PDF file and extracts the text from it.

Example response:

    {
        "filename": "sample.pdf",
        "pages": 3,
        "characters": 2450,
        "preview": "This is the extracted text from the PDF..."
    }

## 🧪 How to Test

1. Start the API.

       uvicorn main:app --reload

2. Open the Swagger documentation.

       http://127.0.0.1:8000/docs

3. Find the POST /extract-text endpoint.

4. Click "Try it out".

5. Click "Choose File".

6. Select a PDF file from your computer.

7. Click "Execute".

8. The API will extract the PDF text and return the result.

## ❌ Error Handling

The API only accepts PDF files.

If a non-PDF file is uploaded, the API returns:

    {
        "detail": "Only PDF files are allowed"
    }

If the PDF cannot be processed, the API returns an HTTP 500 error with an appropriate error message.

## 🔄 How the System Works

User uploads PDF
        ↓
FastAPI receives the file
        ↓
File type validation
        ↓
pypdf reads the PDF
        ↓
Text is extracted
        ↓
Page and character counts are calculated
        ↓
Text preview is generated
        ↓
JSON response is returned

## 💻 Example

Input:

    resume.pdf

Output:

    {
        "filename": "resume.pdf",
        "pages": 2,
        "characters": 1837,
        "preview": "This is the extracted text from the PDF..."
    }

## 🔐 Security Considerations

This project is currently designed for learning and portfolio purposes.

For production deployment, the following improvements should be added:

- File size limits
- Authentication
- Authorization
- Malware scanning
- Rate limiting
- Input validation
- Secure file handling
- Logging
- Monitoring
- HTTPS

## 🚀 Future Improvements

The project can be extended with:

- OCR for scanned PDFs
- AWS S3 storage
- AWS Lambda processing
- AWS SQS asynchronous processing
- Docker containerization
- AWS ECR
- AWS ECS Fargate
- Authentication
- API rate limiting
- CloudWatch monitoring
- AI-powered PDF summarization
- PDF question answering
- Embedding generation
- Vector database
- Hybrid search
- RAG pipeline
- LLM integration

## 🎯 Learning Objectives

This project demonstrates practical experience with:

- Python
- FastAPI
- REST APIs
- File uploads
- PDF processing
- Error handling
- API documentation
- Virtual environments
- Python dependency management
- Git
- GitHub

## 📌 Project Information

Project: PDF Text Extractor API

Day: 1 / 30

Category: AI/ML Engineering

Programming Language: Python

Framework: FastAPI

PDF Library: pypdf

API Server: Uvicorn

Difficulty: Beginner to Intermediate

## 🏗️ Hybrid RAG Roadmap

This project is the first component of the larger Hybrid RAG System.

PDF Text Extraction
        ↓
Text Chunking
        ↓
Text Embeddings
        ↓
Vector Database
        ↓
Keyword Search
        ↓
Semantic Search
        ↓
Hybrid Search
        ↓
RAG Pipeline
        ↓
LLM
        ↓
Cloud Deployment

## 👨‍💻 Author

Athul Sathyan

GitHub:
https://github.com/athulsathyan136-alt

## 📜 License

This project is created for educational and portfolio purposes.

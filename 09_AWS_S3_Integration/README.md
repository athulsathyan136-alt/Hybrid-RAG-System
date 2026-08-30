# ☁️ AWS S3 Storage Integration

A Python-based file storage system that demonstrates how to integrate **Amazon S3-style object storage** into an AI/ML application. This project provides a simple command-line interface (CLI) for uploading, listing, downloading, and deleting files.

> **Project 9 of the Hybrid RAG System — AI/ML + Cloud Portfolio**

---

## 🚀 Features

* 📤 Upload files to storage
* 📋 List stored files
* 📥 Download files
* 🗑️ Delete files
* 💻 Simple interactive CLI
* 🔐 Designed to support secure AWS credential management
* ☁️ Can be extended from local storage to Amazon S3
* 🧩 Suitable as a storage component for a RAG/AI pipeline

---

## 🏗️ Project Structure

```text
09_AWS_S3_Integration/
│
├── s3_storage.py
├── test.txt
├── storage/
│   └── test.txt
│
└── README.md
```

---

## 🛠️ Technologies Used

| Technology   | Purpose                        |
| ------------ | ------------------------------ |
| Python       | Application logic              |
| AWS S3       | Object storage concept         |
| Boto3        | AWS SDK for Python             |
| File System  | Local S3-style storage/testing |
| Git & GitHub | Version control                |

---

## ⚙️ How It Works

The application provides an interactive menu:

```text
================================
     LOCAL S3 STORAGE
================================

Choose an option:
1. Upload file
2. List files
3. Download file
4. Delete file
5. Exit
```

### Upload

Select:

```text
1
```

Then provide the file path:

```text
test.txt
```

The application stores the file in the configured storage location.

Example:

```text
✅ File uploaded successfully!
Stored at: storage\test.txt
```

### List Files

Select:

```text
2
```

The application displays the files currently stored.

### Download

Select:

```text
3
```

Enter the filename to retrieve the stored file.

### Delete

Select:

```text
4
```

Enter the filename you want to remove.

### Exit

Select:

```text
5
```

to close the application.

---

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/athulsathyan136-alt/Hybrid-RAG-System.git
```

### 2. Navigate to Project 9

```bash
cd Hybrid-RAG-System/09_AWS_S3_Integration
```

### 3. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

### 4. Activate the environment

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the Python executable directly:

```powershell
.\venv\Scripts\python.exe s3_storage.py
```

---

## ▶️ Run the Application

```powershell
.\venv\Scripts\python.exe s3_storage.py
```

Or, after activating the virtual environment:

```powershell
python s3_storage.py
```

---

## ☁️ AWS S3 Integration

The project is structured as a foundation for integrating **Amazon S3** into the Hybrid RAG pipeline.

A production implementation can use:

```python
import boto3

s3 = boto3.client("s3")
```

Files can then be uploaded to an S3 bucket:

```python
s3.upload_file(
    "document.pdf",
    "your-bucket-name",
    "documents/document.pdf"
)
```

This allows documents to be stored centrally and accessed by other components of the AI pipeline.

---

## 🔐 Security

AWS credentials should **never be hardcoded** in the source code.

Avoid:

```python
AWS_ACCESS_KEY = "your-secret-key"
AWS_SECRET_KEY = "your-secret-key"
```

Instead, use:

* AWS IAM
* Environment variables
* AWS CLI credential configuration
* IAM roles when running on AWS services

Example:

```text
.env
```

should not be committed to GitHub.

Add sensitive files to `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
```

---

## 🔄 Role in the Hybrid RAG System

This project represents the **cloud storage layer** of the larger Hybrid RAG architecture.

```text
                 Hybrid RAG System
                       │
                       ▼
                📄 Documents
                       │
                       ▼
              ☁️ S3 Storage Layer
                       │
                       ▼
                Text Extraction
                       │
                       ▼
                  Chunking
                       │
                       ▼
                 Embeddings
                       │
                       ▼
                Vector Database
                       │
                       ▼
                 RAG Retrieval
                       │
                       ▼
                  LLM Response
```

The S3 layer can be used to store:

* PDF documents
* Text files
* User uploads
* Processed documents
* Embedding-related artifacts
* RAG knowledge-base documents

---

## 🧪 Testing

The application was tested using a sample file:

```text
test.txt
```

Successful upload output:

```text
✅ File uploaded successfully!
Stored at: storage\test.txt
```

The following operations are supported and tested:

* [x] Upload file
* [x] List files
* [x] Download file
* [x] Delete file
* [x] Exit application

---

## 📈 Future Improvements

Planned improvements include:

* [ ] Connect directly to Amazon S3
* [ ] Add AWS IAM authentication
* [ ] Add environment-based configuration
* [ ] Add file metadata
* [ ] Add file size validation
* [ ] Add MIME type validation
* [ ] Add logging
* [ ] Add error handling
* [ ] Add FastAPI endpoints
* [ ] Integrate with the RAG pipeline
* [ ] Dockerize the application
* [ ] Add CI/CD with GitHub Actions
* [ ] Deploy storage service to AWS

---

## 🎯 Learning Objectives

This project demonstrates practical understanding of:

* Python file handling
* Object storage concepts
* AWS S3 architecture
* Cloud storage integration
* Boto3 fundamentals
* CLI application development
* Secure credential management
* Git/GitHub project management
* Cloud architecture for AI applications

---

## 👨‍💻 Author

**Athul Sathyan**



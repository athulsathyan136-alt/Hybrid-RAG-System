# 🧠 Embedding Generator

A simple Python project that converts text into numerical **embeddings** using a pretrained Hugging Face Sentence Transformers model.

This project is **Day 3** of my 30-Day AI/ML + Cloud Portfolio project series and is an important component of my **Hybrid RAG System**.

---

## 🚀 Project Overview

An embedding is a numerical representation of text.

Instead of treating text only as words, an embedding model converts the meaning of the text into a vector of numbers.

For example:

```text
"Artificial intelligence is changing the world"
```

is converted into a vector similar to:

```text
[0.0214, -0.0342, 0.0678, ...]
```

The vector can then be used for:

* Semantic search
* Similarity comparison
* Recommendation systems
* Retrieval-Augmented Generation (RAG)
* Document search
* Question answering
* AI applications

---

## 🎯 Objective

The main objectives of this project are:

* Generate text embeddings
* Understand vector representations
* Use Hugging Face Sentence Transformers
* Calculate semantic similarity
* Prepare embeddings for vector databases
* Understand an important component of RAG systems

---

## 🛠️ Technologies Used

* Python
* Sentence Transformers
* Hugging Face
* NumPy
* `all-MiniLM-L6-v2`

---

## 📁 Project Structure

```text
03_Embedding_Generator/
│
├── embedding_generator.py
├── requirements.txt
└── README.md
```

---

## 🤖 Embedding Model

This project uses:

```text
all-MiniLM-L6-v2
```

from the Sentence Transformers library.

The model converts text into a **384-dimensional vector**.

Example:

```text
Input Text
    ↓
Sentence Transformer
    ↓
384-Dimensional Embedding
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/athulsathyan136-alt/Hybrid-RAG-System.git
```

### 2. Enter the project

```bash
cd Hybrid-RAG-System/03_Embedding_Generator
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 📦 Requirements

The `requirements.txt` file contains:

```text
sentence-transformers
numpy
```

---

## ▶️ How to Run

Run:

```bash
python embedding_generator.py
```

The program will ask for text:

```text
==================================================
       EMBEDDING GENERATOR
==================================================

Enter text:
```

Enter an example:

```text
Artificial intelligence is changing the world
```

---

## 📊 Example Output

```text
Original Text:
Artificial intelligence is changing the world

Embedding Dimension:
384

First 10 Embedding Values:
[...]

Embedding generated successfully!
```

The exact embedding values may be different depending on the environment and model version.

---

## 🧪 Semantic Similarity Test

The project also compares two sentences:

```text
Sentence 1:
I love artificial intelligence.

Sentence 2:
AI is my favorite technology.
```

The program generates embeddings for both sentences and calculates their cosine similarity.

Example:

```text
==================================================
       SEMANTIC SIMILARITY TEST
==================================================

Sentence 1:
I love artificial intelligence.

Sentence 2:
AI is my favorite technology.

Similarity Score:
0.7...
```

A higher similarity score generally indicates that the two sentences are more semantically similar.

---

## 🔢 How Similarity Works

The project uses **cosine similarity**.

The formula is:

```text
similarity = A · B / (||A|| × ||B||)
```

Where:

* `A` = embedding of the first sentence
* `B` = embedding of the second sentence
* `·` = dot product
* `||A||` = magnitude of vector A
* `||B||` = magnitude of vector B

Cosine similarity is commonly used to compare embeddings.

---

## 🧠 What I Learned

Through this project, I learned:

* What text embeddings are
* How text is converted into vectors
* How Sentence Transformers work
* How to use Hugging Face models
* How to generate embeddings with Python
* What vector dimensions mean
* How semantic similarity works
* How cosine similarity compares vectors
* Why embeddings are important for RAG systems

---

## 🔗 Role in RAG

Embeddings are a core component of a Retrieval-Augmented Generation system.

The basic pipeline is:

```text
Documents
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Embedding Generation
    ↓
Vector Database
    ↓
Similarity Search
    ↓
Relevant Context
    ↓
LLM
    ↓
Final Answer
```

This project implements the **Embedding Generation** stage.

---

## 🔮 Future Improvements

Possible improvements include:

* Add batch embedding generation
* Read text from files
* Generate embeddings for PDF documents
* Save embeddings to disk
* Add FAISS vector search
* Build a FastAPI API
* Add a vector database
* Connect embeddings to the complete RAG pipeline
* Add GPU support
* Add automated tests

---

## 📚 Project Series

This project is part of my **30-Day AI/ML + Cloud Portfolio Builder**.

### Day 1

**PDF Text Extractor API**

Technologies:

* Python
* FastAPI
* PyPDF2
* Docker

### Day 2

**Smart Text Chunker**

Technologies:

* Python
* Regular Expressions
* Text Processing

### Day 3

**Embedding Generator**

Technologies:

* Python
* Sentence Transformers
* Hugging Face
* NumPy

### Day 4

**Vector Database + Similarity Search**

Planned technologies:

* Python
* FAISS
* Embeddings
* Vector Search

---

## 📈 RAG Progress

```text
[✓] PDF Text Extraction
[✓] Text Chunking
[✓] Embedding Generation
[ ] Vector Database
[ ] Similarity Search
[ ] Retrieval Pipeline
[ ] LLM Integration
[ ] RAG API
[ ] Docker Deployment
[ ] AWS Deployment
[ ] CI/CD
```

---

## 👨‍💻 Author

**Amal Sathyan**


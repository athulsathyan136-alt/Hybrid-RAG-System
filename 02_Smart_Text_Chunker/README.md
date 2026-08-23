# ✂️ Smart Text Chunker

A beginner-friendly Python project that divides large text documents into smaller overlapping chunks.

This project is Day 2 of the 30 Days, 30 AI/ML + Cloud Projects portfolio challenge.

The main purpose of this project is to understand how large documents are prepared before they are used in AI systems such as RAG (Retrieval-Augmented Generation), semantic search, vector databases, and document question-answering systems.

## 🚀 Features

- Split large text into smaller chunks
- Configurable chunk size
- Configurable chunk overlap
- Preserve context between chunks
- Display chunk numbers
- Display character count
- Simple Python implementation
- No external Python libraries required
- Easy to understand
- Easy to extend for RAG applications

## 🧠 What Is Text Chunking?

Text chunking means dividing a large document into smaller pieces called chunks.

For example:

Large Document
       ↓
   Text Chunker
       ↓
   ┌─────────┐
   │ Chunk 1 │
   └─────────┘
       ↓
   ┌─────────┐
   │ Chunk 2 │
   └─────────┘
       ↓
   ┌─────────┐
   │ Chunk 3 │
   └─────────┘
       ↓
   ┌─────────┐
   │ Chunk 4 │
   └─────────┘

Large documents are divided because AI systems often work better when information is processed in smaller meaningful pieces.

## 🔄 What Is Chunk Overlap?

Chunk overlap means that some text from one chunk is repeated in the next chunk.

Example:

Chunk 1:

Python is a popular programming language used for AI applications.

Chunk 2:

AI applications. Developers use Python to build machine learning systems.

The phrase "AI applications." appears in both chunks.

This repeated text is called overlap.

Overlap helps preserve context when information is divided between chunks.

## 🤔 Why Do We Need Overlap?

Imagine a sentence is divided between two chunks:

Chunk 1:

Python is widely used in artificial

Chunk 2:

intelligence and machine learning.

The meaning is separated.

With overlap:

Chunk 1:

Python is widely used in artificial intelligence

Chunk 2:

artificial intelligence and machine learning.

The important context appears in both chunks.

This can improve retrieval in RAG systems.

## 🛠️ Technologies Used

- Python
- Python Functions
- Python Lists
- Python Loops
- Python String Slicing
- Git
- GitHub

No external Python packages are required.

## 💻 Requirements

You need:

- Python 3.x
- VS Code
- Git

Check Python:

python --version

Example:

Python 3.12.0

## 📁 Project Structure

Hybrid-RAG-System/
│
├── 01_PDF_Text_Extractor_API/
│   ├── main.py
│   ├── requirements.txt
│   ├── README.md
│   └── .gitignore
│
└── 02_Smart_Text_Chunker/
    ├── text_chunker.py
    ├── README.md
    └── .gitignore

## 📄 Main Python File

The main program is:

text_chunker.py

The program contains a function called:

chunk_text()

This function receives text and divides it into smaller chunks.

## 🧩 Complete Python Code

```python
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start = end - overlap

    return chunks


text = """
Python is a popular programming language used in web development,
automation, data science, artificial intelligence, machine learning,
and many other areas. Python has a simple syntax that makes it easy
for beginners to learn. Developers use Python to build applications,
APIs, scripts, machine learning models, and automation tools.
FastAPI is a modern Python framework for building APIs. It is fast,
easy to use, and provides automatic API documentation.
"""


chunks = chunk_text(
    text,
    chunk_size=100,
    overlap=20
)


for number, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {number} ---")
    print(f"Characters: {len(chunk)}")
    print(chunk)

from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from PyPDF2 import PdfReader
from pydantic import BaseModel
import json

from search import search
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="RAG Document Upload API",
    description="Upload PDF documents and ask questions using RAG.",
    version="1.0.0"
)


# ==========================================
# DIRECTORIES
# ==========================================

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("output")

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


# ==========================================
# LOAD LANGUAGE MODEL
# ==========================================

MODEL_NAME = "google/flan-t5-small"

print("Loading language model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

print("Language model loaded!")


# ==========================================
# HOME ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "RAG Document Upload API is running"
    }


# ==========================================
# CREATE TEXT CHUNKS
# ==========================================

def create_chunks(text, chunk_size=1200, overlap=200):

    # Clean the text
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces
    lines = []

    for line in text.split("\n"):
        line = line.strip()

        if line:
            lines.append(line)

    # Rebuild clean text
    clean_text = " ".join(lines)

    chunks = []

    start = 0
    text_length = len(clean_text)

    while start < text_length:

        end = start + chunk_size

        # Get chunk
        chunk = clean_text[start:end]

        # Try to end at a sentence
        if end < text_length:

            last_period = chunk.rfind(". ")
            last_question = chunk.rfind("? ")
            last_exclamation = chunk.rfind("! ")

            best_break = max(
                last_period,
                last_question,
                last_exclamation
            )

            if best_break > chunk_size * 0.5:
                end = start + best_break + 1
                chunk = clean_text[start:end]

        chunk = chunk.strip()

        if chunk:
            chunks.append(chunk)

        # Move forward with overlap
        start = end - overlap

        if start < 0:
            start = 0

    return chunks

# ==========================================
# PDF UPLOAD ENDPOINT
# ==========================================

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Check file type

    if file.content_type != "application/pdf":

        return {
            "error": "Only PDF files are allowed"
        }

    # Save PDF

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:

        buffer.write(await file.read())

    # Read PDF

    reader = PdfReader(file_path)

    # Extract text

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    # Save extracted text

    output_file = OUTPUT_DIR / f"{file.filename}.txt"

    with open(output_file, "w", encoding="utf-8") as file_out:

        file_out.write(text)

    # Create chunks

    chunks = create_chunks(text)

    # Save chunks

    chunks_file = OUTPUT_DIR / f"{file.filename}.chunks.json"

    with open(chunks_file, "w", encoding="utf-8") as chunks_out:

        json.dump(
            chunks,
            chunks_out,
            ensure_ascii=False,
            indent=2
        )

    # Return information

    return {

        "message": "PDF uploaded and processed successfully",

        "filename": file.filename,

        "pages": len(reader.pages),

        "characters": len(text),

        "chunks": len(chunks),

        "text_file": str(output_file),

        "chunks_file": str(chunks_file)
    }


# ==========================================
# QUESTION REQUEST MODEL
# ==========================================

class QuestionRequest(BaseModel):

    question: str


# ==========================================
# ASK QUESTION ENDPOINT
# ==========================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    # Search relevant chunks

    results = search(
        request.question,
        top_k=3
    )

    # Check if results exist

    if not results:

        return {

            "question": request.question,

            "answer": "I could not find relevant information in the PDF."
        }

    # Build context

    context_parts = []

    for result in results:

        chunk = result["chunk"]

        # Limit each chunk

        chunk = chunk[:500]

        context_parts.append(chunk)

    context = "\n\n".join(context_parts)

    # Create prompt

    prompt = (
        "Answer the question using only the information "
        "provided in the context. "
        "Give a short and clear answer.\n\n"

        "Context:\n"

        f"{context}\n\n"

        "Question:\n"

        f"{request.question}\n\n"

        "Answer:"
    )

    # Convert prompt to tokens

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    # Generate answer

    outputs = model.generate(

        **inputs,

        max_new_tokens=100,

        num_beams=4,

        early_stopping=True
    )

    # Convert generated tokens to text

    answer = tokenizer.decode(

        outputs[0],

        skip_special_tokens=True
    )

    # Return answer

    return {

        "question": request.question,

        "answer": answer
    }
from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
from pydantic import BaseModel
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

import faiss
import json


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="RAG Multi-Document API",
    description="Upload multiple PDF documents and search across them.",
    version="1.0.0"
)


# ==========================================
# DIRECTORIES
# ==========================================

UPLOAD_DIR = Path("uploads")
DATA_DIR = Path("data")

UPLOAD_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)


# ==========================================
# FILE PATHS
# ==========================================

DOCUMENTS_FILE = DATA_DIR / "documents.json"
INDEX_FILE = DATA_DIR / "faiss.index"


# ==========================================
# EMBEDDING MODEL
# ==========================================

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading embedding model...")

embedding_model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded!")


# ==========================================
# GLOBAL DATA
# ==========================================

all_chunks = []

vector_index = None


# ==========================================
# LOAD SAVED DATA
# ==========================================

def load_vector_data():

    global all_chunks
    global vector_index

    if DOCUMENTS_FILE.exists():

        with open(
            DOCUMENTS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            all_chunks = json.load(file)

    if INDEX_FILE.exists():

        vector_index = faiss.read_index(
            str(INDEX_FILE)
        )

    print(f"Loaded {len(all_chunks)} chunks")


load_vector_data()


# ==========================================
# HOME API
# ==========================================

@app.get("/")
def home():

    documents = set()

    for item in all_chunks:

        documents.add(
            item["document"]
        )

    return {

        "message": "RAG Multi-Document API is running",

        "status": "ready",

        "total_documents": len(documents),

        "total_chunks": len(all_chunks)

    }


# ==========================================
# TEXT CHUNKING
# ==========================================

def create_chunks(
    text,
    chunk_size=1000,
    overlap=200
):

    text = text.replace(
        "\r\n",
        "\n"
    )

    text = text.replace(
        "\r",
        "\n"
    )

    clean_lines = []

    for line in text.split("\n"):

        line = line.strip()

        if line:

            clean_lines.append(line)

    clean_text = " ".join(
        clean_lines
    )

    chunks = []

    start = 0

    while start < len(clean_text):

        end = min(

            start + chunk_size,

            len(clean_text)

        )

        chunk = clean_text[
            start:end
        ].strip()

        if chunk:

            chunks.append(chunk)

        if end >= len(clean_text):

            break

        start = end - overlap

    return chunks


# ==========================================
# BUILD FAISS INDEX
# ==========================================

def build_vector_index():

    global vector_index

    if not all_chunks:

        return 0

    texts = []

    for item in all_chunks:

        texts.append(
            item["content"]
        )

    print(
        f"Generating embeddings for "
        f"{len(texts)} chunks..."
    )

    embeddings = embedding_model.encode(

        texts,

        convert_to_numpy=True,

        show_progress_bar=False

    )

    embeddings = embeddings.astype(
        "float32"
    )

    dimension = embeddings.shape[1]

    vector_index = faiss.IndexFlatL2(
        dimension
    )

    vector_index.add(
        embeddings
    )

    print(
        f"FAISS index created with "
        f"{len(texts)} vectors"
    )

    return len(texts)


# ==========================================
# SAVE DATA
# ==========================================

def save_vector_data():

    with open(

        DOCUMENTS_FILE,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            all_chunks,

            file,

            ensure_ascii=False,

            indent=2

        )

    if vector_index is not None:

        faiss.write_index(

            vector_index,

            str(INDEX_FILE)

        )

    print(
        "Data saved successfully"
    )


# ==========================================
# UPLOAD MULTIPLE PDF DOCUMENTS
# ==========================================

@app.post(
    "/upload",

    openapi_extra={

        "requestBody": {

            "required": True,

            "content": {

                "multipart/form-data": {

                    "schema": {

                        "type": "object",

                        "properties": {

                            "files": {

                                "type": "array",

                                "items": {

                                    "type": "string",

                                    "format": "binary"

                                },

                                "description":
                                "Upload one or more PDF files"

                            }

                        },

                        "required": [

                            "files"

                        ]

                    }

                }

            }

        }

    }

)

async def upload_documents(

    files: list[UploadFile] = File(...)

):

    global all_chunks

    uploaded_documents = []


    for uploaded_file in files:


        # ----------------------------------

        # CHECK FILE NAME

        # ----------------------------------

        if not uploaded_file.filename:

            continue


        # ----------------------------------

        # CHECK PDF FORMAT

        # ----------------------------------

        if not uploaded_file.filename.lower().endswith(
            ".pdf"
        ):

            raise HTTPException(

                status_code=400,

                detail=(
                    f"{uploaded_file.filename} "
                    "is not a PDF file"
                )

            )


        # ----------------------------------

        # SAVE FILE

        # ----------------------------------

        file_path = (

            UPLOAD_DIR /

            uploaded_file.filename

        )


        content = await uploaded_file.read()


        with open(

            file_path,

            "wb"

        ) as buffer:

            buffer.write(
                content
            )


        # ----------------------------------

        # READ PDF

        # ----------------------------------

        try:


            reader = PdfReader(
                file_path
            )


            text = ""


            for page in reader.pages:


                page_text = page.extract_text()


                if page_text:

                    text += (

                        page_text +

                        "\n"

                    )


        except Exception as error:


            raise HTTPException(

                status_code=400,

                detail=(

                    f"Could not process "

                    f"{uploaded_file.filename}: "

                    f"{str(error)}"

                )

            )


        # ----------------------------------

        # CHECK TEXT

        # ----------------------------------

        if not text.strip():


            raise HTTPException(

                status_code=400,

                detail=(

                    f"No readable text found in "

                    f"{uploaded_file.filename}"

                )

            )


        # ----------------------------------

        # CREATE CHUNKS

        # ----------------------------------

        document_chunks = create_chunks(
            text
        )


        # ----------------------------------

        # STORE CHUNKS

        # ----------------------------------

        for chunk in document_chunks:


            all_chunks.append({

                "document":
                uploaded_file.filename,

                "content":
                chunk

            })


        # ----------------------------------

        # DOCUMENT RESULT

        # ----------------------------------

        uploaded_documents.append({

            "filename":
            uploaded_file.filename,

            "pages":
            len(reader.pages),

            "characters":
            len(text),

            "chunks":
            len(document_chunks

            )

        })


    # ======================================

    # CHECK UPLOAD

    # ======================================

    if not uploaded_documents:


        raise HTTPException(

            status_code=400,

            detail=(
                "Please upload at least one "
                "PDF file."
            )

        )


    # ======================================

    # BUILD VECTOR DATABASE

    # ======================================

    indexed_chunks = build_vector_index()


    # ======================================

    # SAVE DATA

    # ======================================

    save_vector_data()


    return {


        "message":
        "Documents uploaded successfully",


        "documents":
        uploaded_documents,


        "uploaded_documents":
        len(uploaded_documents),


        "total_chunks":
        len(all_chunks),


        "indexed_chunks":
        indexed_chunks

    }


# ==========================================
# QUESTION REQUEST MODEL
# ==========================================

class QuestionRequest(
    BaseModel
):

    question: str

    top_k: int = 5


# ==========================================
# QUERY DOCUMENTS
# ==========================================

@app.post("/query")

def query_documents(
    request: QuestionRequest
):


    if vector_index is None:


        raise HTTPException(

            status_code=400,

            detail=(
                "No documents indexed. "
                "Please upload PDF files first."
            )

        )


    if not all_chunks:


        raise HTTPException(

            status_code=400,

            detail=(
                "No document chunks available."
            )

        )


    top_k = min(

        request.top_k,

        len(all_chunks)

    )


    # --------------------------------------

    # QUESTION EMBEDDING

    # --------------------------------------

    question_embedding = embedding_model.encode(

        [request.question],

        convert_to_numpy=True

    )


    question_embedding = question_embedding.astype(
        "float32"
    )


    # --------------------------------------

    # SEARCH FAISS

    # --------------------------------------

    distances, indices = vector_index.search(

        question_embedding,

        top_k

    )


    results = []


    for distance, index in zip(

        distances[0],

        indices[0]

    ):


        if index == -1:

            continue


        chunk = all_chunks[index]


        results.append({


            "document":
            chunk["document"],


            "content":
            chunk["content"],


            "distance":
            float(distance)


        })


    return {


        "question":
        request.question,


        "results":
        results,


        "total_results":
        len(results)

    }


# ==========================================
# LIST DOCUMENTS
# ==========================================

@app.get("/documents")

def list_documents():


    documents = {}


    for item in all_chunks:


        filename = item["document"]


        if filename not in documents:


            documents[filename] = 0


        documents[filename] += 1


    result = []


    for filename, chunks in documents.items():


        result.append({


            "filename":
            filename,


            "chunks":
            chunks


        })


    return {


        "documents":
        result,


        "total_documents":
        len(result),


        "total_chunks":
        len(all_chunks)

    }


# ==========================================
# DELETE ALL DOCUMENTS
# ==========================================

@app.delete("/documents")

def delete_all_documents():


    global all_chunks

    global vector_index


    all_chunks = []

    vector_index = None


    # DELETE JSON

    if DOCUMENTS_FILE.exists():

        DOCUMENTS_FILE.unlink()


    # DELETE FAISS INDEX

    if INDEX_FILE.exists():

        INDEX_FILE.unlink()


    # DELETE UPLOADED FILES

    for file in UPLOAD_DIR.glob("*"):


        if file.is_file():

            file.unlink()


    return {


        "message":
        "All documents deleted successfully"

    }
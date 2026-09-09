from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from io import BytesIO
import chromadb
import uuid


# ==================================================
# FASTAPI APP
# ==================================================

app = FastAPI(
    title="RAG PDF Chatbot with ChromaDB",
    description="Upload PDF documents and ask questions using RAG",
    version="2.0.0"
)


# ==================================================
# CHROMADB SETUP
# ==================================================

print("=" * 50)
print("Connecting to ChromaDB...")
print("=" * 50)

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="pdf_documents"
)

print("ChromaDB connected!")
print("Existing chunks:", collection.count())


# ==================================================
# EMBEDDING MODEL
# ==================================================

print("=" * 50)
print("Loading embedding model...")
print("=" * 50)

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded!")


# ==================================================
# LLM MODEL
# ==================================================

print("=" * 50)
print("Loading FLAN-T5 model...")
print("=" * 50)

LLM_MODEL = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(
    LLM_MODEL
)

llm_model = AutoModelForSeq2SeqLM.from_pretrained(
    LLM_MODEL
)

print("FLAN-T5 model loaded!")


# ==================================================
# REQUEST MODEL
# ==================================================

class QuestionRequest(BaseModel):

    question: str

    top_k: int = 3


# ==================================================
# TEXT CHUNKING
# ==================================================

def split_text(
    text,
    chunk_size=500,
    overlap=100
):

    chunks = []

    start = 0

    step = chunk_size - overlap

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():

            chunks.append(
                chunk.strip()
            )

        start += step

    return chunks


# ==================================================
# GENERATE ANSWER
# ==================================================

def generate_answer(
    question,
    context
):

    prompt = f"""
Answer the question using only the information provided in the context.

If the answer is not available in the context, say:
"I could not find the answer in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    outputs = llm_model.generate(
        **inputs,
        max_new_tokens=150,
        num_beams=4,
        early_stopping=True
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return answer.strip()


# ==================================================
# HOME ENDPOINT
# ==================================================

@app.get("/")
def home():

    return {

        "message": "RAG PDF Chatbot with ChromaDB is running",

        "version": "2.0.0",

        "database_chunks": collection.count(),

        "embedding_model":
            "sentence-transformers/all-MiniLM-L6-v2",

        "llm_model":
            LLM_MODEL

    }


# ==================================================
# UPLOAD PDF ENDPOINT
# ==================================================

@app.post("/upload")
async def upload_pdf(
    files: list[UploadFile] = File(
        ...,
        description="Select one or more PDF files"
    )
):

    uploaded_documents = []

    total_chunks = 0

    for file in files:

        # ------------------------------------------
        # CHECK FILE NAME
        # ------------------------------------------

        if not file.filename:

            continue


        # ------------------------------------------
        # CHECK PDF
        # ------------------------------------------

        if not file.filename.lower().endswith(".pdf"):

            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} is not a PDF file"
            )


        # ------------------------------------------
        # READ FILE
        # ------------------------------------------

        file_content = await file.read()


        # ------------------------------------------
        # OPEN PDF
        # ------------------------------------------

        try:

            pdf_reader = PdfReader(
                BytesIO(file_content)
            )

        except Exception:

            raise HTTPException(
                status_code=400,
                detail=f"Could not read PDF: {file.filename}"
            )


        # ------------------------------------------
        # EXTRACT TEXT
        # ------------------------------------------

        text = ""

        for page in pdf_reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"


        # ------------------------------------------
        # CHECK TEXT
        # ------------------------------------------

        if not text.strip():

            raise HTTPException(
                status_code=400,
                detail=f"No readable text found in {file.filename}"
            )


        # ------------------------------------------
        # SPLIT TEXT
        # ------------------------------------------

        chunks = split_text(
            text,
            chunk_size=500,
            overlap=100
        )


        documents = []

        embeddings = []

        metadatas = []

        ids = []


        # ------------------------------------------
        # CREATE EMBEDDINGS
        # ------------------------------------------

        for index, chunk in enumerate(chunks):

            embedding = embedding_model.encode(
                chunk
            ).tolist()


            documents.append(
                chunk
            )


            embeddings.append(
                embedding
            )


            metadatas.append({

                "filename": file.filename,

                "chunk_number": index + 1

            })


            ids.append(
                str(uuid.uuid4())
            )


        # ------------------------------------------
        # STORE IN CHROMADB
        # ------------------------------------------

        collection.add(

            documents=documents,

            embeddings=embeddings,

            metadatas=metadatas,

            ids=ids

        )


        # ------------------------------------------
        # UPLOAD INFORMATION
        # ------------------------------------------

        uploaded_documents.append({

            "filename": file.filename,

            "pages": len(
                pdf_reader.pages
            ),

            "characters": len(text),

            "chunks": len(chunks)

        })


        total_chunks += len(chunks)


    # ------------------------------------------
    # RESPONSE
    # ------------------------------------------

    return {

        "message":
            "PDF documents uploaded successfully",

        "documents":
            uploaded_documents,

        "total_uploaded":
            len(uploaded_documents),

        "total_chunks":
            total_chunks,

        "database_chunks":
            collection.count()

    }


# ==================================================
# ASK QUESTION
# ==================================================

@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    # ------------------------------------------
    # VALIDATE QUESTION
    # ------------------------------------------

    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )


    # ------------------------------------------
    # VALIDATE DATABASE
    # ------------------------------------------

    database_count = collection.count()

    if database_count == 0:

        raise HTTPException(
            status_code=400,
            detail=
            "No PDF documents uploaded. Upload a PDF first."
        )


    # ------------------------------------------
    # LIMIT TOP K
    # ------------------------------------------

    top_k = max(
        1,
        min(
            request.top_k,
            database_count
        )
    )


    # ------------------------------------------
    # CREATE QUESTION EMBEDDING
    # ------------------------------------------

    question_embedding = embedding_model.encode(
        request.question
    ).tolist()


    # ------------------------------------------
    # SEARCH CHROMADB
    # ------------------------------------------

    results = collection.query(

        query_embeddings=[
            question_embedding
        ],

        n_results=top_k

    )


    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    distances = results["distances"][0]


    # ------------------------------------------
    # BUILD CONTEXT
    # ------------------------------------------

    context_parts = []

    for index, document in enumerate(documents):

        context_parts.append(

            f"""
SOURCE {index + 1}
FILE: {metadatas[index]["filename"]}
CHUNK: {metadatas[index]["chunk_number"]}

{document}
"""

        )


    context = "\n".join(
        context_parts
    )


    # ------------------------------------------
    # GENERATE AI ANSWER
    # ------------------------------------------

    try:

        answer = generate_answer(
            request.question,
            context
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Answer generation failed: {str(error)}"
        )


    # ------------------------------------------
    # PREPARE SOURCES
    # ------------------------------------------

    sources = []

    for index in range(
        len(documents)
    ):

        sources.append({

            "filename":
                metadatas[index]["filename"],

            "chunk_number":
                metadatas[index]["chunk_number"],

            "distance":
                distances[index],

            "content":
                documents[index]

        })


    # ------------------------------------------
    # FINAL RESPONSE
    # ------------------------------------------

    return {

        "question":
            request.question,

        "answer":
            answer,

        "sources":
            sources,

        "total_results":
            len(sources)

    }


# ==================================================
# DATABASE INFORMATION
# ==================================================

@app.get("/database")
def database_info():

    return {

        "total_chunks":
            collection.count(),

        "collection":
            "pdf_documents"

    }


# ==================================================
# CLEAR DATABASE
# ==================================================

@app.delete("/clear")
def clear_database():

    global collection


    try:

        chroma_client.delete_collection(
            name="pdf_documents"
        )

    except Exception:

        pass


    collection = chroma_client.get_or_create_collection(
        name="pdf_documents"
    )


    return {

        "message":
            "Database cleared successfully",

        "total_chunks":
            collection.count()

    }


# ==================================================
# CUSTOM OPENAPI
# ==================================================

def custom_openapi():

    if app.openapi_schema:

        return app.openapi_schema


    openapi_schema = get_openapi(

        title=app.title,

        version=app.version,

        description=app.description,

        routes=app.routes

    )


    try:

        upload_schema = (
            openapi_schema[
                "components"
            ][
                "schemas"
            ][
                "Body_upload_pdf_upload_post"
            ]
        )


        upload_schema[
            "properties"
        ][
            "files"
        ] = {

            "type": "array",

            "items": {

                "type": "string",

                "format": "binary"

            },

            "title": "Files",

            "description":
                "Select one or more PDF files"

        }


    except KeyError:

        pass


    app.openapi_schema = openapi_schema


    return app.openapi_schema


app.openapi = custom_openapi
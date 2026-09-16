from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="RAG Answer Generation API",
    description="Semantic retrieval followed by AI answer generation",
    version="1.0.0"
)


# ============================================================
# EMBEDDING MODEL
# ============================================================

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# ============================================================
# TEXT GENERATION MODEL
# ============================================================

generator = pipeline(
    "text-generation",
    model="distilgpt2"
)


# ============================================================
# KNOWLEDGE BASE
# ============================================================

documents = [
    "Python is a popular programming language used for web development, automation, data science, and artificial intelligence.",

    "FastAPI is a modern Python framework used for building high-performance REST APIs.",

    "Machine learning allows computers to learn patterns from data without being explicitly programmed.",

    "Natural language processing enables computers to understand and process human language.",

    "Docker packages applications and their dependencies into portable containers.",

    "AWS provides cloud computing services including EC2, S3, Lambda, and ECR.",

    "RAG stands for Retrieval-Augmented Generation and combines document retrieval with language model generation.",

    "Vector databases store numerical embeddings and allow semantic similarity search.",

    "MLOps combines machine learning development with deployment, monitoring, automation, and operations."
]


# ============================================================
# DOCUMENT EMBEDDINGS
# ============================================================

document_embeddings = embedding_model.encode(
    documents,
    convert_to_tensor=True
)


# ============================================================
# REQUEST MODEL
# ============================================================

class QuestionRequest(BaseModel):
    question: str
    top_k: int = 3


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "project": "RAG Answer Generation API",
        "status": "running",
        "description": "Retrieve relevant documents and generate an AI answer."
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "generation_model": "distilgpt2"
    }


# ============================================================
# DOCUMENTS
# ============================================================

@app.get("/documents")
def get_documents():

    return {
        "total_documents": len(documents),
        "documents": documents
    }


# ============================================================
# ASK QUESTION
# ============================================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        return {
            "error": "Question cannot be empty."
        }

    if request.top_k < 1:
        return {
            "error": "top_k must be at least 1."
        }

    # --------------------------------------------------------
    # STEP 1 — QUESTION EMBEDDING
    # --------------------------------------------------------

    question_embedding = embedding_model.encode(
        question,
        convert_to_tensor=True
    )

    # --------------------------------------------------------
    # STEP 2 — SEMANTIC SEARCH
    # --------------------------------------------------------

    scores = util.cos_sim(
        question_embedding,
        document_embeddings
    )[0]

    top_k = min(
        request.top_k,
        len(documents)
    )

    top_results = scores.topk(k=top_k)

    selected_documents = []

    for score, index in zip(
        top_results.values,
        top_results.indices
    ):

        selected_documents.append(
            {
                "document": documents[int(index)],
                "score": float(score)
            }
        )

    # --------------------------------------------------------
    # STEP 3 — BUILD CONTEXT
    # --------------------------------------------------------

    context = "\n".join(
        item["document"]
        for item in selected_documents
    )

    # --------------------------------------------------------
    # STEP 4 — GENERATION PROMPT
    # --------------------------------------------------------

    prompt = (
        "Answer the question using the context below.\n\n"
        "Context:\n"
        + context
        + "\n\nQuestion:\n"
        + question
        + "\n\nAnswer:"
    )

    # --------------------------------------------------------
    # STEP 5 — GENERATE ANSWER
    # --------------------------------------------------------

    generated = generator(
        prompt,
        max_new_tokens=80,
        do_sample=False,
        pad_token_id=generator.tokenizer.eos_token_id
    )

    generated_text = generated[0]["generated_text"]

    # Remove the original prompt from the generated output
    if generated_text.startswith(prompt):
        answer = generated_text[len(prompt):].strip()
    else:
        answer = generated_text.strip()

    # --------------------------------------------------------
    # STEP 6 — RETURN RAG RESULT
    # --------------------------------------------------------

    return {
        "question": question,
        "retrieval_method": "Semantic Similarity",
        "generation_model": "distilgpt2",
        "retrieved_documents": len(selected_documents),
        "answer": answer,
        "sources": selected_documents
    }
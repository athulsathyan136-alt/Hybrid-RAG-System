from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="RAG Citation & Source Attribution API",
    description="RAG API with source citations and document attribution",
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
    {
        "id": 1,
        "title": "Python",
        "content": "Python is a popular programming language used for web development, automation, data science, and artificial intelligence."
    },
    {
        "id": 2,
        "title": "FastAPI",
        "content": "FastAPI is a modern Python framework used for building high-performance REST APIs."
    },
    {
        "id": 3,
        "title": "Machine Learning",
        "content": "Machine learning allows computers to learn patterns from data without being explicitly programmed."
    },
    {
        "id": 4,
        "title": "Natural Language Processing",
        "content": "Natural language processing enables computers to understand and process human language."
    },
    {
        "id": 5,
        "title": "Docker",
        "content": "Docker packages applications and their dependencies into portable containers."
    },
    {
        "id": 6,
        "title": "AWS",
        "content": "AWS provides cloud computing services including EC2, S3, Lambda, and ECR."
    },
    {
        "id": 7,
        "title": "RAG",
        "content": "RAG stands for Retrieval-Augmented Generation and combines document retrieval with language model generation."
    },
    {
        "id": 8,
        "title": "Vector Databases",
        "content": "Vector databases store numerical embeddings and allow semantic similarity search."
    },
    {
        "id": 9,
        "title": "MLOps",
        "content": "MLOps combines machine learning development with deployment, monitoring, automation, and operations."
    }
]


# ============================================================
# DOCUMENT EMBEDDINGS
# ============================================================

document_texts = [
    document["content"]
    for document in documents
]

document_embeddings = embedding_model.encode(
    document_texts,
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
        "project": "RAG Citation & Source Attribution API",
        "status": "running",
        "description": "Retrieve documents, generate an answer, and return source citations."
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
    # STEP 1 — CREATE QUESTION EMBEDDING
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

        document = documents[int(index)]

        selected_documents.append(
            {
                "source_id": document["id"],
                "title": document["title"],
                "content": document["content"],
                "similarity_score": round(float(score), 4)
            }
        )

    # --------------------------------------------------------
    # STEP 3 — CREATE CITATION CONTEXT
    # --------------------------------------------------------

    context_parts = []

    for item in selected_documents:

        context_parts.append(
            f"[Source {item['source_id']}] "
            f"{item['title']}: "
            f"{item['content']}"
        )

    context = "\n".join(context_parts)

    # --------------------------------------------------------
    # STEP 4 — GENERATION PROMPT
    # --------------------------------------------------------

    prompt = (
        "Answer the question using the provided sources. "
        "Do not invent information. "
        "Mention the relevant source numbers in the answer.\n\n"
        "Sources:\n"
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
        max_new_tokens=100,
        do_sample=False,
        pad_token_id=generator.tokenizer.eos_token_id
    )

    generated_text = generated[0]["generated_text"]

    if generated_text.startswith(prompt):
        answer = generated_text[len(prompt):].strip()
    else:
        answer = generated_text.strip()

    # --------------------------------------------------------
    # STEP 6 — CREATE CITATIONS
    # --------------------------------------------------------

    citations = []

    for item in selected_documents:

        citations.append(
            {
                "citation": f"[{item['source_id']}]",
                "source_id": item["source_id"],
                "title": item["title"],
                "similarity_score": item["similarity_score"]
            }
        )

    # --------------------------------------------------------
    # STEP 7 — RETURN RESULT
    # --------------------------------------------------------

    return {
        "question": question,
        "answer": answer,
        "retrieval_method": "Semantic Similarity",
        "generation_model": "distilgpt2",
        "retrieved_documents": len(selected_documents),
        "citations": citations,
        "sources": selected_documents
    }
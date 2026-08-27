from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# ==================================================
# 1. LOAD EMBEDDING MODEL
# ==================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded!")


# ==================================================
# 2. DOCUMENT KNOWLEDGE BASE
# ==================================================

documents = [
    "Python is a popular programming language used for software development.",

    "Python is widely used in artificial intelligence and machine learning.",

    "Machine learning allows computers to learn patterns from data.",

    "Deep learning uses neural networks to solve complex problems.",

    "FastAPI is a Python framework used for building high-performance APIs.",

    "Docker packages applications into lightweight containers.",

    "AWS provides cloud computing services such as EC2, S3, Lambda, and ECS.",

    "Amazon S3 is an object storage service used to store files and data.",

    "Amazon EC2 provides virtual servers in the cloud.",

    "GitHub is a platform used to store and manage source code.",

    "Git is a version control system used to track changes in code.",

    "RAG combines information retrieval with large language models.",

    "Vector databases store numerical representations of text.",

    "FAISS is a library used for efficient similarity search.",

    "MLOps combines machine learning with software engineering and operations."
]


# ==================================================
# 3. CREATE DOCUMENT EMBEDDINGS
# ==================================================

print("\nCreating document embeddings...")

document_embeddings = embedding_model.encode(
    documents
)

document_embeddings = np.array(
    document_embeddings
).astype("float32")

print("Document embeddings created!")


# ==================================================
# 4. CREATE FAISS INDEX
# ==================================================

dimension = document_embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(document_embeddings)

print(
    f"FAISS index contains {index.ntotal} documents."
)


# ==================================================
# 5. LOAD FLAN-T5 MODEL
# ==================================================

print("\nLoading language model...")

model_name = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(
    model_name
)

language_model = AutoModelForSeq2SeqLM.from_pretrained(
    model_name
)

print("Language model loaded!")


# ==================================================
# 6. RETRIEVE DOCUMENTS
# ==================================================

def retrieve_documents(query, top_k=3):

    query_embedding = embedding_model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, index_number in zip(
        distances[0],
        indices[0]
    ):

        results.append({
            "text": documents[index_number],
            "distance": float(distance)
        })

    return results


# ==================================================
# 7. GENERATE ANSWER
# ==================================================

def generate_answer(query, retrieved_documents):

    context = "\n".join(
        document["text"]
        for document in retrieved_documents
    )

    prompt = f"""
Answer the question using only the information
provided in the context.

Context:
{context}

Question:
{query}

Answer:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = language_model.generate(
        **inputs,
        max_new_tokens=100
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return answer


# ==================================================
# 8. RAG PIPELINE
# ==================================================

def rag(query):

    print("\nSearching knowledge base...")

    retrieved_documents = retrieve_documents(
        query,
        top_k=3
    )

    print("\n===== RETRIEVED CONTEXT =====")

    for number, document in enumerate(
        retrieved_documents,
        start=1
    ):

        print(f"\nContext {number}")

        print(
            f"Distance: "
            f"{document['distance']:.4f}"
        )

        print(
            f"Text: "
            f"{document['text']}"
        )

    print("\nGenerating answer...")

    answer = generate_answer(
        query,
        retrieved_documents
    )

    print("\n===== AI ANSWER =====")

    print(answer)


# ==================================================
# 9. USER INTERFACE
# ==================================================

print("\n========================================")
print("          DAY 6 RAG PIPELINE")
print("========================================")

print("\nType 'exit' to stop.")

while True:

    query = input("\nAsk a question: ")

    if query.lower() == "exit":

        print("\nGoodbye!")

        break

    if not query.strip():

        print("Please enter a question.")

        continue

    rag(query)
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


# --------------------------------------------------
# 1. Load embedding model
# --------------------------------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully!")


# --------------------------------------------------
# 2. Documents
# --------------------------------------------------

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


# --------------------------------------------------
# 3. Generate document embeddings
# --------------------------------------------------

print("\nGenerating document embeddings...")

document_embeddings = model.encode(documents)

document_embeddings = np.array(
    document_embeddings
).astype("float32")

print("Embeddings generated successfully!")


# --------------------------------------------------
# 4. Create FAISS index
# --------------------------------------------------

dimension = document_embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(document_embeddings)

print(f"Stored {index.ntotal} documents in FAISS.")


# --------------------------------------------------
# 5. Semantic search function
# --------------------------------------------------

def semantic_search(query, top_k=5):

    # Convert query into embedding
    query_embedding = model.encode([query])

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    # Search FAISS
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
            "document": documents[index_number],
            "distance": float(distance)
        })

    return results


# --------------------------------------------------
# 6. User interface
# --------------------------------------------------

print("\n====================================")
print("       SEMANTIC SEARCH ENGINE")
print("====================================")

print("\nType 'exit' to stop the program.")


while True:

    query = input("\nEnter your search query: ")

    if query.lower() == "exit":
        print("\nGoodbye!")
        break

    if not query.strip():
        print("Please enter a search query.")
        continue

    results = semantic_search(query, top_k=5)

    print("\n========== SEARCH RESULTS ==========")

    for position, result in enumerate(
        results,
        start=1
    ):

        print(f"\nResult {position}")

        print(
            f"Distance: "
            f"{result['distance']:.4f}"
        )

        print(
            f"Text: "
            f"{result['document']}"
        )

    print("\n====================================")
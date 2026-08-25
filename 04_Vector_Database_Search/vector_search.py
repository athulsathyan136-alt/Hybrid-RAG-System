from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


# --------------------------------------------------
# 1. Load the embedding model
# --------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------------------------
# 2. Example document chunks
# --------------------------------------------------

chunks = [
    "Python is a popular programming language.",
    "Python is widely used for artificial intelligence and machine learning.",
    "FastAPI is a Python framework for building APIs.",
    "Docker is a platform used to build and run applications in containers.",
    "AWS provides cloud computing services such as EC2, S3, Lambda, and ECS.",
    "Machine learning allows computers to learn patterns from data.",
    "RAG combines document retrieval with large language models.",
    "GitHub is used to store and manage source code.",
]


# --------------------------------------------------
# 3. Generate embeddings
# --------------------------------------------------

embeddings = model.encode(chunks)


# Convert embeddings to NumPy float32
embeddings = np.array(embeddings).astype("float32")


print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)


# --------------------------------------------------
# 4. Create FAISS index
# --------------------------------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)


# --------------------------------------------------
# 5. Add embeddings to FAISS
# --------------------------------------------------

index.add(embeddings)


print("Vectors stored in FAISS:", index.ntotal)


# --------------------------------------------------
# 6. Ask the user for a search query
# --------------------------------------------------

query = input("\nEnter your search query: ")


# --------------------------------------------------
# 7. Convert query into an embedding
# --------------------------------------------------

query_embedding = model.encode([query])

query_embedding = np.array(query_embedding).astype("float32")


# --------------------------------------------------
# 8. Search FAISS
# --------------------------------------------------

k = 3

distances, indices = index.search(query_embedding, k)


# --------------------------------------------------
# 9. Display results
# --------------------------------------------------

print("\n===== SEARCH RESULTS =====")

for rank, (distance, index_number) in enumerate(
    zip(distances[0], indices[0]),
    start=1
):
    print(f"\nResult {rank}")
    print(f"Distance: {distance:.4f}")
    print(f"Text: {chunks[index_number]}")
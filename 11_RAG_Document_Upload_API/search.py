import faiss
import numpy as np
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer


INDEX_FILE = Path("output/faiss.index")
CHUNKS_FILE = Path("output/pythoncrashcourse.pdf.chunks.json")


print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded!")


print("Loading FAISS index...")

index = faiss.read_index(str(INDEX_FILE))

print(f"FAISS index contains {index.ntotal} vectors")


with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
    chunks = json.load(file)

print(f"Loaded {len(chunks)} chunks")


def search(query, top_k=5):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    # Normalize query
    faiss.normalize_L2(query_embedding)

    # Search more results first
    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, index_id in zip(scores[0], indices[0]):

        if index_id == -1:
            continue

        results.append({
            "chunk": chunks[index_id],
            "score": float(score)
        })

    # Make sure highest similarity comes first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results


if __name__ == "__main__":

    question = input("\nAsk a question about the PDF: ")

    results = search(question)

    print("\n========== SEARCH RESULTS ==========\n")

    for i, result in enumerate(results, start=1):

        print(f"--- Result {i} ---")
        print(f"Similarity: {result['score']:.4f}")
        print(result["chunk"][:1000])
        print()
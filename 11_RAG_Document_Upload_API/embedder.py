from sentence_transformers import SentenceTransformer
import numpy as np
import json
from pathlib import Path


MODEL_NAME = "all-MiniLM-L6-v2"

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded!")


def create_embeddings(chunks):

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True
    )

    return embeddings


def load_chunks(chunks_file):

    with open(chunks_file, "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":

    chunks_file = Path(
        "output/pythoncrashcourse.pdf.chunks.json"
    )

    chunks = load_chunks(chunks_file)

    print(f"Loaded {len(chunks)} chunks")

    embeddings = create_embeddings(chunks)

    print("Embeddings created!")

    print("Embedding shape:", embeddings.shape)

    np.save(
        "output/embeddings.npy",
        embeddings
    )

    print("Embeddings saved!")
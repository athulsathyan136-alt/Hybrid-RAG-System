import faiss
import numpy as np
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer


# ==========================================
# FILE PATHS
# ==========================================

CHUNKS_FILE = Path("output/pythoncrashcourse.pdf.chunks.json")
EMBEDDINGS_FILE = Path("output/embeddings.npy")
INDEX_FILE = Path("output/faiss.index")


# ==========================================
# LOAD CHUNKS
# ==========================================

print("Loading chunks...")

with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
    chunks = json.load(file)

print(f"Loaded {len(chunks)} chunks")


# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded!")


# ==========================================
# CREATE EMBEDDINGS
# ==========================================

print("Generating embeddings...")

embeddings = model.encode(
    chunks,
    convert_to_numpy=True,
    show_progress_bar=True
)

embeddings = embeddings.astype("float32")


print(f"Embedding shape: {embeddings.shape}")


# ==========================================
# NORMALIZE EMBEDDINGS
# ==========================================

faiss.normalize_L2(embeddings)


# ==========================================
# SAVE EMBEDDINGS
# ==========================================

np.save(
    EMBEDDINGS_FILE,
    embeddings
)

print("Embeddings saved!")


# ==========================================
# CREATE FAISS INDEX
# ==========================================

print("Building FAISS index...")

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)


print(f"FAISS index contains {index.ntotal} vectors")


# ==========================================
# VERIFY INDEX
# ==========================================

if index.ntotal != len(chunks):

    raise ValueError(
        f"Mismatch! FAISS has {index.ntotal} vectors "
        f"but there are {len(chunks)} chunks."
    )


# ==========================================
# SAVE FAISS INDEX
# ==========================================

faiss.write_index(
    index,
    str(INDEX_FILE)
)

print("FAISS index saved!")

print("\n================================")
print("VECTOR STORE READY")
print("================================")
from sentence_transformers import SentenceTransformer
import numpy as np


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text):
    """
    Convert text into a numerical embedding vector.
    """
    embedding = model.encode(text)
    return embedding


def main():
    print("=" * 50)
    print("       EMBEDDING GENERATOR")
    print("=" * 50)

    # Get text from user
    text = input("\nEnter text: ")

    if not text.strip():
        print("Please enter some text.")
        return

    # Generate embedding
    embedding = generate_embedding(text)

    print("\nOriginal Text:")
    print(text)

    print("\nEmbedding Dimension:")
    print(len(embedding))

    print("\nFirst 10 Embedding Values:")
    print(np.round(embedding[:10], 6))

    print("\nEmbedding generated successfully!")

    # ---------------------------------
    # Semantic Similarity Test
    # ---------------------------------

    text1 = "I love artificial intelligence."
    text2 = "AI is my favorite technology."

    embedding1 = generate_embedding(text1)
    embedding2 = generate_embedding(text2)

    # Calculate cosine similarity
    similarity = np.dot(embedding1, embedding2) / (
        np.linalg.norm(embedding1) *
        np.linalg.norm(embedding2)
    )

    print("\n" + "=" * 50)
    print("       SEMANTIC SIMILARITY TEST")
    print("=" * 50)

    print("\nSentence 1:")
    print(text1)

    print("\nSentence 2:")
    print(text2)

    print("\nSimilarity Score:")
    print(round(float(similarity), 4))


if __name__ == "__main__":
    main()
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start = end - overlap

    return chunks


text = """
Python is a popular programming language used in web development,
automation, data science, artificial intelligence, machine learning,
and many other areas. Python has a simple syntax that makes it easy
for beginners to learn. Developers use Python to build applications,
APIs, scripts, machine learning models, and automation tools.
FastAPI is a modern Python framework for building APIs. It is fast,
easy to use, and provides automatic API documentation.
"""


chunks = chunk_text(
    text,
    chunk_size=100,
    overlap=20
)


for number, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {number} ---")
    print(f"Characters: {len(chunk)}")
    print(chunk)
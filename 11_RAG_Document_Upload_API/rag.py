from search import search


def generate_answer(question):

    results = search(question, top_k=3)

    if not results:
        return "I could not find relevant information in the PDF."

    best_chunk = results[0]["chunk"]

    return best_chunk


if __name__ == "__main__":

    question = input("\nAsk a question about the PDF: ")

    answer = generate_answer(question)

    print("\n========== ANSWER ==========\n")
    print(answer)
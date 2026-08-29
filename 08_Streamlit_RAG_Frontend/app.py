import streamlit as st
import requests


# Page configuration
st.set_page_config(
    page_title="RAG AI Assistant",
    page_icon="🤖",
    layout="centered"
)


# Title
st.title("🤖 RAG AI Assistant")
st.write("Ask questions and get answers from your RAG system.")


# FastAPI URL
API_URL = "http://127.0.0.1:8000/chat"


# User question
question = st.text_input(
    "Ask your question:",
    placeholder="Example: What is Docker?"
)


# Ask button
if st.button("Ask AI"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "question": question
                    },
                    timeout=120
                )

                if response.status_code == 200:

                    data = response.json()

                    st.subheader("🤖 Answer")

                    st.write(data.get("answer", "No answer returned."))

                    # Sources
                    sources = data.get("sources", [])

                    if sources:

                        st.subheader("📚 Sources")

                        for i, source in enumerate(sources, start=1):

                            if isinstance(source, dict):
                                text = source.get("text", "")
                            else:
                                text = str(source)

                            st.write(f"**Source {i}:**")
                            st.write(text)

                else:

                    st.error(
                        f"API Error: {response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Could not connect to the RAG API. "
                    "Make sure Day 7 FastAPI is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "⏱️ The request took too long. "
                    "Please try again."
                )

            except Exception as e:

                st.error(
                    f"Unexpected error: {e}"
                )
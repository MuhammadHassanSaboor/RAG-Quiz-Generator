import streamlit as st
import os
from rag_pipeline import build_vector_db, get_answer

import gc
gc.collect()


st.title("📄 RAG-Powered Document QA App")
st.markdown("Upload PDFs, PPTs, DOCX, or TXT files and ask questions from them.")

uploaded_files = st.file_uploader(
    "Upload documents", 
    type=["pdf", "pptx", "docx", "txt"], 
    accept_multiple_files=True
)

if uploaded_files:
    doc_paths = []
    os.makedirs("docs", exist_ok=True)

    for file in uploaded_files:
        filepath = os.path.join("docs", file.name)
        with open(filepath, "wb") as f:
            f.write(file.getbuffer())
        doc_paths.append(filepath)

    st.info("Processing documents...")
    build_vector_db(doc_paths) 
    st.success("Documents processed and stored!")

query = st.text_input("Ask a question from your documents")

if query:
    with st.spinner("Thinking..."):
        response = get_answer(query)
    st.markdown(f"**Answer:** {response}")

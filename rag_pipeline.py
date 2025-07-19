import os
import gc
import shutil
from typing import List

from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
    TextLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.docstore.document import Document
import chromadb

PERSIST_DIRECTORY = "embeddings"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 400
TOP_K = 5

embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def load_docs(file_paths: List[str]) -> List[Document]:
    docs = []
    for path in file_paths:
        print(f"📂 Loading: {path}")
        try:
            if path.endswith(".pdf"):
                loader = PyPDFLoader(path)
            elif path.endswith(".pptx"):
                loader = UnstructuredPowerPointLoader(path)
            elif path.endswith(".docx"):
                loader = UnstructuredWordDocumentLoader(path)
            elif path.endswith((".txt", ".text")):
                loader = TextLoader(path, encoding="utf-8")
            else:
                print(f"❗ Unsupported file format: {path}")
                continue
            docs.extend(loader.load())
        except Exception as e:
            print(f"❌ Error loading {path}: {e}")
    print(f"✅ Total documents loaded: {len(docs)}")
    return docs


def split_docs(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(docs)
    print(f"🔪 Total chunks created: {len(chunks)}")
    return chunks


def reset_chroma_db_without_deleting():
    try:
        client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
        collections = client.list_collections()
        for collection in collections:
            client.delete_collection(name=collection.name)
        print("✅ All Chroma collections deleted.")
    except Exception as e:
        print(f"❌ Error clearing collections: {e}")

    os.makedirs(PERSIST_DIRECTORY, exist_ok=True)



def store_embeddings(splits: List[Document]) -> Chroma:
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=PERSIST_DIRECTORY,
    )
    # vectordb.persist()
    # vectordb.dispose()
    print("📦 Embeddings stored and vector DB persisted.")
    return vectordb


def get_relevant_chunks(query: str, k: int = TOP_K) -> List[Document]:
    vectordb = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embedding)
    return vectordb.similarity_search(query, k=k)


def get_answer(query: str) -> str:
    chunks = get_relevant_chunks(query)
    if not chunks:
        return "❌ No relevant information found in the documents."

    context = "\n\n".join(doc.page_content for doc in chunks)

    prompt = f"""You are a helpful assistant. Use the context below to answer the question.

Context:
{context}

Question: {query}

Answer:"""

    llm = Ollama(model="llama3", temperature=0.3)
    return llm.invoke(prompt)


def build_vector_db(file_paths: List[str]):
    reset_chroma_db_without_deleting()
    docs = load_docs(file_paths)
    splits = split_docs(docs)
    store_embeddings(splits)

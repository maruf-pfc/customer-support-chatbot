from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS

from app.config import DATA_DIR, VECTORSTORE_DIR, EMBEDDING_MODEL_NAME
import os


def ingestDocuments():
    documents = []

    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(str(DATA_DIR / file))
            documents.extend(loader.load())

    if not documents:
        raise ValueError("No PDF documents found in data/docs")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    embeddings = SentenceTransformerEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)

    VECTORSTORE_DIR.mkdir(exist_ok=True)
    vectorstore.save_local(str(VECTORSTORE_DIR))

    print(f"Ingested {len(chunks)} chunks into FAISS")


if __name__ == "__main__":
    ingestDocuments()

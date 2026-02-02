from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS

from app.config import DATA_DIR, VECTORSTORE_DIR, EMBEDDING_MODEL_NAME


def ingest_documents():
    if not DATA_DIR.exists():
        raise RuntimeError(f"DATA_DIR does not exist: {DATA_DIR}")

    pdf_files = list(DATA_DIR.glob("*.pdf"))
    if not pdf_files:
        raise RuntimeError("No PDF files found in data/docs")

    documents = []
    for pdf in pdf_files:
        loader = PyPDFLoader(str(pdf))
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = pdf.name
        documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Reduced from 700
        chunk_overlap=50, # Reduced from 140
    )
    chunks = splitter.split_documents(documents)

    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    vectorstore = FAISS.from_documents(chunks, embeddings)

    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(VECTORSTORE_DIR))

    print(f"Ingested {len(chunks)} chunks into FAISS")


if __name__ == "__main__":
    ingest_documents()
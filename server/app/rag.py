from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.llms import Ollama

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.config import VECTORSTORE_DIR, EMBEDDING_MODEL_NAME


def load_rag_chain():
    if not VECTORSTORE_DIR.exists():
        raise RuntimeError(
            "Vectorstore not found. Run ingest.py first."
        )

    # 1. Load embeddings
    embeddings = SentenceTransformerEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )

    # 2. Load FAISS index
    vectorstore = FAISS.load_local(
        folder_path=str(VECTORSTORE_DIR),
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    # 3. Load Ollama
    llm = Ollama(
        # model="qwen3:8b",
        # model="qwen2.5:3b",
        model="llama3.2:1b",
        temperature=0,
    )

    # 4. Prompt
    prompt = PromptTemplate.from_template(
        """You are a helpful assistant.
Answer the question ONLY using the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:"""
    )

    # 5. Runnable RAG chain
    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
    )

    return rag_chain

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings          
from langchain_ollama import OllamaLLM                           

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

from app.config import VECTORSTORE_DIR, EMBEDDING_MODEL_NAME


def format_docs(docs) -> str:
    """
    Safely formats retrieved documents or strings into readable context.
    Handles both Document objects and plain strings (compatibility layer).
    """
    if not docs:
        return "No relevant information found in the documents."

    lines = []
    for i, item in enumerate(docs, 1):
        if isinstance(item, str):
            content = item.strip()
            source = "unknown document"
        elif isinstance(item, Document):
            content = item.page_content.strip()
            source = item.metadata.get("source", "unknown document")
        else:
            content = str(item).strip()
            source = "unknown format"

        lines.append(f"[{i}] {content}  (Source: {source})")

    return "\n\n".join(lines)


def load_rag_chain():
    """
    Loads the complete RAG chain with proper retrieval and formatting.
    """
    if not VECTORSTORE_DIR.exists():
        raise RuntimeError("Vectorstore not found. Please run ingest.py first.")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    vectorstore = FAISS.load_local(
        folder_path=str(VECTORSTORE_DIR),
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )

    llm = OllamaLLM(
        model="qwen2.5:0.5b",
        temperature=0.1,
        num_ctx=2048,  # Reduced context window for lower RAM usage
        num_predict=256, # Reduced max tokens for speed
        timeout=60.0,
    )

    prompt = PromptTemplate.from_template(
        """You are a concise and accurate customer support assistant.
Answer using **only** the provided context.
If the information is not in the context, reply only: "Sorry, I don't have that information."

Always keep answers short, clear and polite.

Context:
{context}

Question: {question}

Answer:"""
    )

    rag_chain = (
        {
            "question": RunnablePassthrough(),
            "retrieved": retriever,
        }
        | RunnableParallel(
            question=RunnablePassthrough(),
            context=RunnableLambda(format_docs),
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
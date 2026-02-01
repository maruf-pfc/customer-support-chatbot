from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from app.config import VECTORSTORE_DIR, EMBEDDING_MODEL_NAME


def load_rag_chain():
    # 1. Load embeddings model
    embeddings = SentenceTransformerEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )

    # 2. Load FAISS vector store from disk
    vectorstore = FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    # 3. Create retriever
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    # 4. Load Ollama LLM
    llm = Ollama(
        model="qwen3:8b",
        temperature=0
    )

    # 5. Prompt template
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a helpful assistant.
Answer the question ONLY using the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""
    )

    # 6. Create RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    return qa_chain

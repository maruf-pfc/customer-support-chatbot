from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.rag import load_rag_chain


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Loading RAG chain...")
        app.state.rag_chain = load_rag_chain()
        print("RAG chain loaded successfully")
    except Exception as e:
        print(f"Failed to load RAG: {e}")
        raise RuntimeError("Cannot start server — vector store missing or broken")
    yield
    print("Shutting down...")


app = FastAPI(title="AI Support Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str


@app.get("/health")
async def health():
    return {"status": "ok", "rag_loaded": hasattr(app.state, "rag_chain")}


import asyncio

@app.post("/ask")
async def ask(req: AskRequest):
    if not hasattr(app.state, "rag_chain"):
        raise HTTPException(503, "RAG engine not ready.")

    print(f"Received question: {req.question}")

    try:
        print("Starting chain invocation...")
        answer = await app.state.rag_chain.ainvoke(req.question)
        print(f"Chain returned: {answer[:200]}...")  # truncate for log
        return {"answer": answer.strip()}
    except (TimeoutError, asyncio.TimeoutError):
        print("❌ RAG execution timed out (Ollama unresponsive)")
        raise HTTPException(504, "AI model timed out. Please try again later.")
    except Exception as e:
        import traceback
        print("\n" + "═" * 80)
        print("RAG EXECUTION FAILED:")
        traceback.print_exc()
        print("═" * 80 + "\n")
        raise HTTPException(500, f"Backend processing error: {str(e)}")
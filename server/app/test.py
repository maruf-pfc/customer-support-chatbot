# server/test_rag.py
import asyncio
from app.rag import load_rag_chain

async def test():
    chain = load_rag_chain()
    print("Chain loaded OK")
    
    q = "jipc batch 2 er enrollment er last date kobe?"
    print(f"\nQuestion: {q}")
    
    try:
        ans = await chain.ainvoke(q)
        print(f"Answer:\n{ans}\n")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
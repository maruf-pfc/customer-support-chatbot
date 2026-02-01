from app.rag import load_rag_chain

qa = load_rag_chain()

result = qa("What is the refund policy?")
print(result["result"])

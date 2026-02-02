from app.rag import load_rag_chain

rag = load_rag_chain()

question = "jipc batch 2 er enrollment er last date kobe?"
answer = rag.invoke(question)

print("Q:", question)
print("A:", answer)

# AI Support Assistant 🚀

A premium, document-aware customer support chatbot powered by RAG (Retrieval-Augmented Generation), FastAPI, and Next.js.

![AI Support Assistant](https://placehold.co/1200x600/png?text=AI+Support+Assistant+Preview)

## ✨ Features

- **Document-Aware**: Answers questions based on your specific PDF documents (policies, manuals, course outlines).
- **Modern UI/UX**: Glassmorphism design, smooth animations, and responsive layout.
- **RAG Architecture**: Uses FAISS vector store and Ollama (Qwen2.5) for accurate retrieval and generation.
- **Real-time Streaming**: Instant feedback with "Thinking" states and smooth message delivery.

## 🛠️ Tech Stack

- **Frontend**: Next.js 15, TypeScript, TailwindCSS v4, Framer Motion, Lucide React
- **Backend**: FastAPI, LangChain, FAISS, PyPDF
- **AI Model**: Ollama (qwen2.5:3b), HuggingFace Embeddings (all-MiniLM-L6-v2)

## 🚀 Getting Started

### Prerequisites

1. **Node.js** (v18+) and **pnpm**
2. **Python** (v3.10+)
3. **Ollama**: [Download and install Ollama](https://ollama.com/)
   - Pull the model: `ollama pull qwen2.5:3b`

### Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd customer-support-chatbot
   ```

2. **Setup Server**
   ```bash
   cd server
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Setup Client**
   ```bash
   cd ../client
   pnpm install
   ```

### 🏃‍♂️ Running the App

You can run both client and server with a single command from the root directory:

```bash
# From the root directory
pnpm dev
```

- Client: [http://localhost:3000](http://localhost:3000)
- Server API: [http://localhost:8000/docs](http://localhost:8000/docs)

### 📚 Knowledge Base Ingestion

To add your own documents:
1. Place PDF files in `server/data/docs/`
2. Run the ingestion script:
   ```bash
   cd server
   # Ensure env is activated
   python app/ingest.py
   ```

## 🐛 Troubleshooting

**Server fails to start?**
- Ensure virtual environment is activated.
- Check if Ollama is running: `ollama list`

**"RAG chain failed"?**
- Did you run `ingest.py`? The vector store must be built first.
- Ensure the `vectorstore` directory exists in `server/`.

**Client connection error?**
- Verify server is running on port 8000.
- Check network console for CORS issues (CORS is allowed for "*" by default).

## 📄 License

MIT License

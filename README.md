# AI Support Assistant 🚀

A fully local, privacy-first customer support chatbot powered by Retrieval-Augmented Generation (RAG). Answers questions accurately using your own PDF documents — no cloud APIs, no data leaks.

![Chatbot Preview](https://placehold.co/1200x630?text=AI+Support+Assistant+Chat+Interface&font=roboto)

## ✨ Features

- **Document-Grounded Answers**: Uses your PDFs (policies, manuals, FAQs) as knowledge base
- **Zero Cost & Private**: Runs 100% locally with Ollama
- **Fast Retrieval**: FAISS vector database for semantic search
- **Modern Chat UI**: Animated, responsive, dark-mode ready with shadcn/ui
- **Real-time Feedback**: Smooth "Thinking..." animation during generation
- **Cross-Platform**: Works on Linux, Windows, macOS

## 🛠️ Tech Stack

### Backend

- Python 3.10+
- FastAPI
- LangChain (modern Runnable API)
- FAISS (vector database)
- SentenceTransformers (`all-MiniLM-L6-v2`)
- Ollama (`qwen2.5:3b` recommended)

### Frontend

- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui components
- Framer Motion (animations)
- Lucide React icons

### AI Model

- **Recommended**: `qwen2.5:3b` (fast & accurate on low-end hardware)
- Alternatives: `phi3:mini`, `gemma2:2b`, `llama3.2:3b`

## 📋 Prerequisites

1. **Node.js** (v18 or higher) + **npm**
2. **Python** (3.10–3.12 recommended)
3. **Ollama** installed: [https://ollama.com/download](https://ollama.com/download)

   After installing Ollama, pull the model:

   ```bash
   ollama pull qwen2.5:3b
   ```

## 🚀 Quick Start (One-Command Setup)

### Option 1: Use the launcher script (Recommended)

From the project root, run:

```bash
# Linux / macOS / Git Bash / WSL
./run.sh

# Windows PowerShell
.\run.ps1
```

Follow the menu to start backend, frontend, or both.

### Option 2: Manual setup

```bash
# 1. Clone and enter project
git clone <your-repo-url>
cd customer-support-chatbot

# 2. Backend setup
cd server
python -m venv env
source env/bin/activate          # Windows: env\Scripts\activate
pip install -r requirements.txt

# 3. Frontend setup
cd ../frontend
npm install
# or pnpm install / yarn install

# 4. Ingest your documents (first time only)
cd ../server
python -m app.ingest             # Places PDFs in server/data/docs/

# 5. Start services (two terminals)
# Terminal 1 - Backend
cd server
source env/bin/activate
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Open browser: [http://localhost:3000](http://localhost:3000)

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📚 Adding Your Knowledge Base

1. Place your PDF files in `server/data/docs/`
2. Run ingestion:
   ```bash
   cd server
   source env/bin/activate
   python -m app.ingest
   ```
3. Restart the backend server

The chatbot will now answer based on your documents!

## ⚙️ Performance Tips (Low-End Hardware)

Your Ryzen 3 3200G can run this smoothly with these tweaks:

- Use `qwen2.5:3b` or smaller (`phi3:mini`, `gemma2:2b`)
- Limit Ollama threads:
  ```bash
  export OLLAMA_NUM_THREADS=3
  ```
- Reduce context size in `app/rag.py` if needed

On Apple M4 devices: expect **2–5 second responses** (vs minutes on older PCs)

## 🐛 Troubleshooting

| Issue                         | Solution                                              |
| ----------------------------- | ----------------------------------------------------- |
| Server fails to start         | Activate virtualenv, run `python -m app.ingest` first |
| "Could not connect to server" | Ensure backend is running on port 8000                |
| Slow responses                | Switch to smaller model, limit threads                |
| Ollama errors                 | Run `ollama serve &` and check `ollama list`          |
| Vectorstore missing           | Run ingestion script again                            |
| Import errors                 | Reinstall requirements in clean env                   |

## 🤝 Contributing

Contributions welcome! Feel free to:

- Improve UI/UX
- Add markdown rendering
- Support more document types
- Optimize performance

## 📄 License

MIT License — feel free to use commercially or modify.

---

Built with ❤️ by Md. Maruf Sarker
Dhaka, Bangladesh · February 2026

**Enjoy your customer support assistant** 🚀

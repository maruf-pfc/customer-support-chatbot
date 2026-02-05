#!/usr/bin/env bash
# run.sh
# Single-command launcher for the AI Customer Support Chatbot project
# Works best on Linux / macOS / Git Bash / WSL

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_DIR="$PROJECT_ROOT/server"
FRONTEND_DIR="$PROJECT_ROOT/frontend"   # ← change if your frontend folder has different name

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}AI Customer Support Chatbot Launcher${NC}"
echo "Project root: $PROJECT_ROOT"
echo ""

check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}Error:${NC} $1 is required but not installed."
        exit 1
    fi
}

# ── Basic dependency checks ────────────────────────────────────────
check_command python3
check_command node   # or npm
check_command npm

# ── Helper functions ───────────────────────────────────────────────
start_backend() {
    echo -e "${YELLOW}Starting FastAPI backend...${NC}"
    cd "$SERVER_DIR" || { echo -e "${RED}Cannot cd to server directory${NC}"; exit 1; }

    # Activate virtualenv if it exists
    if [ -d "env" ] && [ -f "env/bin/activate" ]; then
        # shellcheck disable=SC1091
        source env/bin/activate
    elif [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
        # shellcheck disable=SC1091
        source .venv/bin/activate
    fi

    # Make sure Ollama is running (optional but helpful)
    if ! curl -s http://localhost:11434 > /dev/null; then
        echo -e "${YELLOW}Ollama not detected. Trying to start it in background...${NC}"
        ollama serve >/dev/null 2>&1 &
        sleep 3
    fi

    # Start uvicorn
    exec uvicorn main:app --reload --port 8000
}

start_frontend() {
    echo -e "${YELLOW}Starting Next.js frontend...${NC}"
    cd "$FRONTEND_DIR" || { echo -e "${RED}Cannot cd to frontend directory${NC}"; exit 1; }

    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "Installing frontend dependencies..."
        npm install
    fi

    exec npm run dev
}

# ── Main logic ─────────────────────────────────────────────────────
echo "Choose what you want to start:"
echo "  1) Backend only      (FastAPI + Ollama check)"
echo "  2) Frontend only     (Next.js dev server)"
echo "  3) Both (recommended – opens two terminals)"
echo ""
read -rp "Enter number (1–3): " choice

case $choice in
    1)
        start_backend
        ;;
    2)
        start_frontend
        ;;
    3)
        echo -e "${GREEN}Launching both services...${NC}"
        echo "(You will need two terminal windows)"

        if command -v tmux >/dev/null 2>&1; then
            tmux new-session -d -s chatbot 'cd "'"$SERVER_DIR"'" && bash -c "source env/bin/activate 2>/dev/null || true; uvicorn main:app --reload --port 8000"'
            tmux split-window -h -t chatbot 'cd "'"$FRONTEND_DIR"'" && npm run dev'
            tmux attach -t chatbot
        elif command -v gnome-terminal >/dev/null 2>&1; then
            gnome-terminal -- bash -c "cd '$SERVER_DIR' && source env/bin/activate 2>/dev/null || true && uvicorn main:app --reload --port 8000; exec bash" &
            gnome-terminal -- bash -c "cd '$FRONTEND_DIR' && npm run dev; exec bash" &
        else
            echo -e "${YELLOW}Please open two terminals manually:${NC}"
            echo "Terminal 1: cd server && source env/bin/activate && uvicorn main:app --reload --port 8000"
            echo "Terminal 2: cd frontend && npm run dev"
        fi
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac
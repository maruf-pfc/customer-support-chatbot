from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "docs"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
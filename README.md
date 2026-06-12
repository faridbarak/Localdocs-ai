<<<<<<< HEAD
=======
<<<<<<< HEAD
# Localdocs-ai
Privacy-focused local documentation generator using AI
=======
>>>>>>> 8e2668faed65efad03dd3c83b10c3c36cf74846a
# LocalDocs AI 🤖

**Privacy-focused local documentation generator using AI**

## Features
<<<<<<< HEAD

- ✅ 100% Local - No API keys, no cloud
- ✅ Privacy-First - Code stays on your machine
- ✅ Multi-Language - Python, JavaScript, TypeScript
- ✅ CLI + API - Terminal or HTTP interface
- ✅ Open Source - MIT License
=======
- ✅ 100% Local - No API keys
- ✅ Privacy-First - Code stays on your machine
- ✅ FastAPI Backend
- ✅ Swagger UI Documentation
>>>>>>> 8e2668faed65efad03dd3c83b10c3c36cf74846a

## Quick Start

```bash
<<<<<<< HEAD
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run API
PYTHONPATH=src uvicorn localdocs.main:app --reload --host 0.0.0.0 --port 8000

# 4. Open docs
# http://localhost:8000/docs
=======
# Install dependencies
pip install fastapi uvicorn

# Run server
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Open docs
# http://localhost:8000/docs
>>>>>>> b6f1f8a (Initial commit: Push localdocs-ai project)
>>>>>>> 8e2668faed65efad03dd3c83b10c3c36cf74846a

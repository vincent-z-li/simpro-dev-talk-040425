# Retrieval Augmented Generation(RAG) with LangChain & Tracing and Monitoring with LangSmith 

## Major tech stack
FastAPI, OpenAI, langChain, langSmith, pydantic, FAISS

## Prerequisites

- Python (3.7 or newer) installed and better can create virtual environments
- OpenAI Account & API key
- LangChain Account & LangSmith API keys

## Getting Started

1. Create a virutalenv and source the environment

```bash
python3 -m venv myenv
source venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a .env file based on .env.dist, and fill in the keys

```bash
cp .env.dist .env
```

4. Generate vectore store (FAISS)

```bash
cd ./scripts
python3 -m ingest_docs
```
After success, `./data/vector_store` folder should appear with .pkl and .faiss files

5. Start the server

```bash
uvicorn api.main:app --reload
```

## Endpoints

1. Swagger API doc  `http://localhost:8000/docs`
2. Swagger API redoc_url `http://localhost:8000/redo`

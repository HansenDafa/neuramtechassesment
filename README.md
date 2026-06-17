# CV Summarizer + Tavily News API

This project provides a small FastAPI backend with two features:

- Upload a PDF CV/resume and extract structured information using OpenRouter (LLM).
- Search news via Tavily and return structured results.

Quick overview

- POST /cv/summarize — upload a PDF file, returns extracted name, location, and work experience summary.
- GET /news?query=... — returns a list of news articles matching the query.

Setup

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
# edit .env and set OPENROUTER_API_KEY and TAVILY_API_KEY
```

Run locally

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Example requests

- CV summarization (multipart/form-data):

```bash
curl -X POST "http://localhost:8000/cv/summarize" -F "file=@/path/to/resume.pdf"
```

- News search:

```bash
curl "http://localhost:8000/news?query=AI"
```

Notes

- The project expects `OPENROUTER_API_KEY` and `TAVILY_API_KEY` to be set in the environment.
- The Tavily API URL can be adjusted in `.env` if your account requires a different endpoint.
- This implementation focuses on clarity and defensive error handling; adapt model names and tokens as needed.

Docker

Build and run with Docker:

```bash
docker build -t cv-summarizer .
docker run -p 8000:8000 --env-file .env cv-summarizer
```

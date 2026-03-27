# RegWatch Agentic AI Backend

FastAPI backend for the RegWatch regulatory intelligence platform.

## Features

- Modular AI agents for:
  - regulation fetch
  - document parse
  - relevance and impact scoring
  - compliance gap analysis
  - policy diff
  - action planning
  - audit logging
- Google Gemini integration (`gemini-2.5-flash`)
- In-memory storage for demo use
- REST APIs designed for the existing Next.js frontend

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set env vars:

```bash
set GEMINI_API_KEY=your_key_here
```

## Run

```bash
uvicorn main:app --reload --port 8000
```

## API Endpoints

- `GET /api/regulations`
- `GET /api/regulation/{id}`
- `POST /api/analyze`
- `GET /api/compliance`
- `GET /api/audit-logs`

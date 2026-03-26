# FOCUS MASTER AI

FOCUS MASTER AI is a modular, local-first orchestration system that routes natural-language tasks into specialized engines and integration adapters.

## Features

- Task classification and dispatching
- Multi-engine workflow orchestration
- Parallel task execution (comma-separated commands)
- Integrations:
  - OpenAI (`OPENAI_API_KEY`)
  - Make webhook (`MAKE_WEBHOOK_URL`)
  - GitHub API stubs (`GITHUB_TOKEN`, `GITHUB_REPO`)
  - Replit endpoint trigger (`REPLIT_RUNNER_URL`)
- Lightweight task history and research cache in `memory/`

## Project Structure

```text
FOCUS_MASTER_AI/
├── core/
├── engines/
├── integrations/
├── pipelines/
├── memory/
├── docs/
├── .env.example
├── main.py
└── requirements.txt
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your real credentials.

## Run

Interactive mode:

```bash
python main.py
```

Single command mode:

```bash
python main.py "build full automation AI system and deploy architecture"
```

Parallel command mode:

```bash
python main.py "research market trends,write launch email,automate follow-up"
```

HTTP API mode:

```bash
python api_server.py
```

Then call:

```bash
curl -X POST http://127.0.0.1:8000/run -H "Content-Type: application/json" -d "{\"task\":\"build full automation AI system and deploy architecture\"}"
```

## Security Notes

- Never hardcode credentials in source files.
- Keep `.env` local and excluded from git.
- If credentials are ever posted in chat or logs, rotate them immediately.

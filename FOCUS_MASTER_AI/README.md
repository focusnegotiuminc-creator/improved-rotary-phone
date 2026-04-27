# FOCUS MASTER AI

FOCUS MASTER AI is a modular, local-first orchestration system that routes natural-language tasks into specialized engines and integration adapters.

## Features

- Task classification and dispatching
- Multi-engine workflow orchestration
- Parallel task execution (comma-separated commands)
- Private operator runtime with persistent run history
- Local-first routing through Ollama when available, with optional OpenAI, Anthropic, and Gemini fallbacks
- Internal API endpoints for runtime health, run execution, and run review
- Integrations:
  - Ollama (`OLLAMA_BASE_URL`, `DEFAULT_OLLAMA_MODEL`)
  - OpenAI (`OPENAI_API_KEY`)
  - Anthropic (`ANTHROPIC_API_KEY`)
  - Gemini (`GEMINI_API_KEY` or `GOOGLE_API_KEY`)
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
3. Copy `.env.example` to `.env` and add your real credentials or local runtime settings.

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

Private runtime status:

```bash
curl http://127.0.0.1:8000/v1/private/runtime
```

Launch a private operator run:

```bash
curl -X POST http://127.0.0.1:8000/v1/private/runs \
  -H "Content-Type: application/json" \
  -d "{\"business\":\"focus-negotium\",\"workflow\":\"Website Design and Deployment\",\"mission\":\"Prepare a private execution plan for a live service-page refresh.\",\"deliverables\":[\"execution brief\",\"deployment checklist\"],\"constraints\":[\"keep internal tooling private\"],\"context\":[\"internal workspace\",\"live site\"],\"integrations\":[\"github\",\"stripe\"],\"execute_automation\":false}"
```

Review a run:

```bash
curl http://127.0.0.1:8000/v1/private/runs
curl http://127.0.0.1:8000/v1/private/runs/<run_id>
```

Private console:

```text
http://127.0.0.1:8000/private-console
```

## VS Code workspace

The workspace is intended to run well in VS Code with Codex CLI as the execution companion:

- use `.vscode/tasks.json` for API, tests, archive builds, and Flux QA
- use `.vscode/launch.json` for the private console API
- keep secrets local in `.env` / `.secrets` and only share sanitized templates

## Security Notes

- Never hardcode credentials in source files.
- Keep `.env` local and excluded from git.
- If credentials are ever posted in chat or logs, rotate them immediately.

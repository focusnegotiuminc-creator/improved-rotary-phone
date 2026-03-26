# FOCUS_MASTER_AI

Modular automation workspace for BUILD, AUTOMATE, CREATE, DEPLOY, and MARKET tasks.

## Project Structure

- `core/`: routing, orchestration, and API templates.
- `modules/`: domain modules (sacred geometry, construction, marketing, publishing).
- `workflows/`: Make/Zapier scenario configs.
- `data/`: research and verification logs.
- `outputs/`: generated books, diagrams, and automation artifacts.
- `config/`: integration mappings and environment template.

## Replit Auto Runner

```bash
python main.py
```

## Daily Command Example

```text
Run FOCUS MASTER AI: Build sacred geometry housing system, generate book, create diagrams, store in GitHub, deploy via Replit, and create marketing funnel with Mailchimp automation.
```

## Make.com Configuration Summary

### Scenario 1 — TASK EXECUTOR
1. Trigger: Webhook (Custom)
2. OpenAI (ChatGPT)
3. Router
   - Path A: GitHub save file
   - Path B: Mailchimp email
   - Path C: Google Drive store output
   - Path D: HTTP API call

### Scenario 2 — AUTOMATION LOOP
1. Trigger: Scheduler (every 1 hour)
2. GitHub watch repo changes
3. OpenAI analyze task
4. HTTP send to Replit endpoint
5. Slack/Email notify

## Credential Handling

Create `.env` manually from `config/.env.template`. Never commit real credentials.

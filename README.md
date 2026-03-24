# THE EYE OF FOCUS

A portable, structured personal AI workspace designed to run your **11-Stage AI Engine** with **Sacred Geometry as the foundational mode**.

## What this repo now includes

- `engine/stages.json`: canonical 11-stage engine definition.
- `engine/prompt-loader.js`: reusable loader/validator for engine stages.
- `app/`: lightweight daily-use web app (`index.html`, `styles.css`, `main.js`).
- `docs/deployment-troubleshooting.md`: why old formats can still appear after publishing and how to fix them.

## Quick start

Because this app is dependency-light, you can run it anywhere.

### Option A: open directly
Open `app/index.html` in a browser.

### Option B: local static server
```bash
cd app
python3 -m http.server 8000
```
Then visit `http://localhost:8000`.

## Core behavior

1. Loads and validates all 11 engine stages.
2. Keeps Sacred Geometry context fixed as the base directive.
3. Lets you generate a structured session brief with:
   - identity + mission
   - engine stages
   - task instructions
   - execution checklist
4. Exports the generated brief as Markdown for reuse in ChatGPT or GitHub workflows.

## Recommended workflow

1. Start each day by loading **THE EYE OF FOCUS**.
2. Set mission, outcomes, constraints, and deliverables.
3. Generate the brief.
4. Paste it into your active coding/chat environment.
5. Execute and track completion stage-by-stage.


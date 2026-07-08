# Focus Beat Maker V3

Codex-ready rewrite of the Focus Records AI Beat Engine.

## What V3 adds

- Production-oriented deterministic audio engine
- Layered kick, snare, hats, percussion, 808 glide, leads, pads, FX, risers
- Section-aware arrangements: hooks, 16-bar verses, bridges, beat-switch logic
- Stems: drums, bass, music, FX
- Mix/master chain: sidechain-style bass ducking, stereo width, compression, reverb, soft clipping, limiting
- FastAPI platform endpoints
- CLI commands
- Local rewrite agent that audits code and writes QA findings
- Safe vocal workflow only: verified Focus-owned or permissioned vocals

## Run locally

```bash
cd focus_records_ai_beat_engine_v3
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m engine.focus_cli list-concepts
python -m engine.focus_cli render C01 --bars 8
python -m engine.focus_cli rewrite-once
uvicorn engine.app:app --reload
```

## API

- `GET /` health
- `GET /concepts` concept list
- `POST /render/{concept_id}?bars=8` render one concept
- `POST /render-all?preview_bars=8` render all concepts
- `POST /rewrite/run` run rewrite audit agent

## Voice rule

Use only verified Focus-owned vocals or permissioned vocal datasets.

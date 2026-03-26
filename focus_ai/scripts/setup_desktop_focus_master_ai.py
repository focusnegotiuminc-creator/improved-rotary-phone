#!/usr/bin/env python3
"""Create a runnable local Focus Master AI app on Desktop from this repository's content."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DESKTOP_APP_DIR = Path.home() / "Desktop" / "focus-master-ai"
SOURCE_FILES = [
    Path("README.md"),
    Path("focus_ai/docs/brand_voice.md"),
    Path("focus_ai/docs/offers.md"),
    Path("focus_ai/docs/ip_and_compliance.md"),
    Path("focus_ai/docs/launch_checklist.md"),
    Path("focus_ai/engine/sacred_ai_workflow.md"),
]

APP_PY = r'''#!/usr/bin/env python3
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

APP_ROOT = Path(__file__).resolve().parent
KNOWLEDGE_DIR = APP_ROOT / "knowledge"
INDEX_FILE = APP_ROOT / "index.html"


def load_documents() -> dict[str, str]:
    docs: dict[str, str] = {}
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        docs[path.name] = path.read_text(encoding="utf-8", errors="ignore")
    return docs


def build_response(question: str, docs: dict[str, str]) -> dict[str, str]:
    tokens = {token.strip(".,!?;:()[]{}'").lower() for token in question.split() if token.strip()}
    best_name = ""
    best_score = -1
    for name, content in docs.items():
        score = sum(1 for token in tokens if token and token in content.lower())
        if score > best_score:
            best_name, best_score = name, score

    if best_name:
        snippet = docs[best_name][:700].replace("\n", " ").strip()
        return {
            "answer": f"Based on {best_name}: {snippet}",
            "source": best_name,
        }

    return {
        "answer": "I couldn't find a direct match in the local Focus Master knowledge files. Try a more specific question.",
        "source": "none",
    }


class Handler(BaseHTTPRequestHandler):
    docs = load_documents()

    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            content = INDEX_FILE.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return
        if path == "/api/health":
            self._send_json({"status": "ok", "documents": len(self.docs)})
            return
        self._send_json({"error": "not found"}, status=404)

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/api/chat":
            self._send_json({"error": "not found"}, status=404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw or b"{}")
        except json.JSONDecodeError:
            self._send_json({"error": "invalid JSON"}, status=400)
            return

        question = str(payload.get("message", "")).strip()
        if not question:
            self._send_json({"error": "message is required"}, status=400)
            return

        response = build_response(question, self.docs)
        self._send_json(response)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8787), Handler)
    print("Focus Master AI running at http://127.0.0.1:8787")
    server.serve_forever()
'''

INDEX_HTML = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Focus Master AI</title>
    <style>
      body { font-family: Arial, sans-serif; max-width: 860px; margin: 2rem auto; padding: 0 1rem; }
      #log { border: 1px solid #ddd; border-radius: 8px; padding: 1rem; min-height: 260px; white-space: pre-wrap; }
      textarea { width: 100%; height: 90px; margin-top: 1rem; }
      button { margin-top: .5rem; padding: .6rem 1rem; }
      .muted { color: #666; font-size: .9rem; }
    </style>
  </head>
  <body>
    <h1>Focus Master AI</h1>
    <p class="muted">Local assistant powered by your Focus--Master repository knowledge files.</p>
    <div id="log">Assistant ready. Ask a question about brand voice, offers, launch, or workflow.</div>
    <textarea id="message" placeholder="Ask something..."></textarea>
    <br />
    <button id="send">Send</button>

    <script>
      const log = document.getElementById("log");
      const message = document.getElementById("message");
      document.getElementById("send").addEventListener("click", async () => {
        const text = message.value.trim();
        if (!text) return;
        log.textContent += "\n\nYou: " + text;
        message.value = "";
        try {
          const res = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: text}),
          });
          const data = await res.json();
          log.textContent += "\nAI: " + (data.answer || data.error || 'No response');
          if (data.source) log.textContent += "\n(source: " + data.source + ")";
        } catch (err) {
          log.textContent += "\nAI error: " + err;
        }
      });
    </script>
  </body>
</html>
'''

DESKTOP_README = """# Focus Master AI (Desktop App)\n\nThis folder was generated from the Focus--Master repository.\n\n## Run\n```bash\npython3 app.py\n```\n\nThen open: http://127.0.0.1:8787\n\n## Contents\n- `app.py`: local HTTP AI service and chat endpoint\n- `index.html`: browser UI\n- `knowledge/`: copied project knowledge files used for responses\n"""


def copy_knowledge(source_root: Path, target_dir: Path) -> list[Path]:
    knowledge_dir = target_dir / "knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    copied: list[Path] = []
    for rel_path in SOURCE_FILES:
        source = source_root / rel_path
        destination = knowledge_dir / rel_path.name
        shutil.copy2(source, destination)
        copied.append(destination)
    return copied


def scaffold_app(target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "app.py").write_text(APP_PY, encoding="utf-8")
    (target_dir / "index.html").write_text(INDEX_HTML, encoding="utf-8")
    (target_dir / "README.md").write_text(DESKTOP_README, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a Desktop Focus Master AI folder and app.")
    parser.add_argument(
        "--desktop-dir",
        default=str(DEFAULT_DESKTOP_APP_DIR),
        help="Destination folder for the desktop app (default: ~/Desktop/focus-master-ai).",
    )
    parser.add_argument(
        "--source-root",
        default=str(ROOT),
        help="Repository root to read source knowledge files from.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    desktop_dir = Path(args.desktop_dir).expanduser().resolve()
    source_root = Path(args.source_root).resolve()

    scaffold_app(desktop_dir)
    copied = copy_knowledge(source_root, desktop_dir)

    print(f"Created Focus Master AI at: {desktop_dir}")
    print("Knowledge files copied:")
    for file_path in copied:
        print(f"- {file_path}")
    print("Run: python3 app.py")


if __name__ == "__main__":
    main()

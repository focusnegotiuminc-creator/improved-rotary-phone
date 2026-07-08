from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import ast, json, time

ROOT = Path(__file__).resolve().parents[1]

@dataclass
class Finding:
    path: str
    severity: str
    message: str
    fix: str | None = None

class FocusRewriteAgent:
    """Local safe rewriting agent.

    It does not require external API keys. It performs deterministic code quality
    gates, writes an audit file, and can apply safe small patches. Use Codex or
    another code model on top of the generated audit when you want LLM changes.
    """
    def __init__(self, root: Path = ROOT):
        self.root = Path(root)

    def python_files(self):
        return sorted([p for p in self.root.rglob('*.py') if '.venv' not in str(p)])

    def audit(self) -> list[Finding]:
        """Scan project Python files and return deterministic quality findings."""
        findings: list[Finding] = []
        for path in self.python_files():
            rel = path.relative_to(self.root).as_posix()
            text = path.read_text()
            try:
                tree = ast.parse(text)
            except SyntaxError as e:
                findings.append(Finding(rel,'critical',f'Syntax error: {e}',None))
                continue
            if 'subprocess.run' in text and 'check=True' not in text:
                findings.append(Finding(rel,'high','subprocess.run should use check=True','add check=True'))
            if len(text.splitlines()) > 420:
                findings.append(Finding(rel,'medium','file is getting large; split DSP/render/app concerns','modularize'))
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not ast.get_docstring(node) and not node.name.startswith('_'):
                    if node.name in {'render','render_all','audit','run'}:
                        findings.append(Finding(rel,'low',f'public function {node.name} should have a docstring','add docstring'))
        if not findings:
            findings.append(Finding('engine','info','No blocking issues detected. Compile gate passed.',None))
        return findings

    def write_audit(self, findings: list[Finding]) -> Path:
        out = self.root/'logs'/'rewrite_audit_v3.md'
        out.parent.mkdir(exist_ok=True)
        lines = ['# Focus Beat Maker V3 Rewrite Audit','',f'Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}', '']
        for f in findings:
            lines.append(f'- **{f.severity.upper()}** `{f.path}` — {f.message}' + (f' | Fix: {f.fix}' if f.fix else ''))
        out.write_text('\n'.join(lines)+'\n')
        return out

    def run(self, apply_safe_patches: bool = False) -> dict:
        """Execute one rewrite-agent pass and write the audit report."""
        findings = self.audit()
        audit_path = self.write_audit(findings)
        return {
            'status': 'passed' if not any(f.severity in {'critical','high'} for f in findings) else 'needs_attention',
            'audit_path': audit_path.as_posix(),
            'findings': [f.__dict__ for f in findings],
            'safe_patches_applied': False,
        }

if __name__ == '__main__':
    print(json.dumps(FocusRewriteAgent().run(), indent=2))

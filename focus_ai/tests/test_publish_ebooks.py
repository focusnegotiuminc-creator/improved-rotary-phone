from pathlib import Path
import subprocess


def test_publish_outputs_index_and_books():
    result = subprocess.run(
        ["python3", "focus_ai/scripts/publish_ebooks.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Published" in result.stdout
    out = Path("focus_ai/published/ebooks")
    assert (out / "index.html").exists()
    assert any(out.glob("*.html"))

import subprocess
import py_compile
from pathlib import Path
import sys


def test_setup_desktop_focus_master_ai_creates_expected_files(tmp_path: Path):
    output_dir = tmp_path / "focus-master-ai"
    result = subprocess.run(
        [
            sys.executable,
            "focus_ai/scripts/setup_desktop_focus_master_ai.py",
            "--desktop-dir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    assert "Created Focus Master AI" in result.stdout
    assert (output_dir / "app.py").exists()
    assert (output_dir / "index.html").exists()
    assert (output_dir / "README.md").exists()
    assert (output_dir / "knowledge" / "brand_voice.md").exists()



def test_generated_app_is_valid_python(tmp_path: Path):
    output_dir = tmp_path / "focus-master-ai"
    subprocess.run(
        [sys.executable, "focus_ai/scripts/setup_desktop_focus_master_ai.py", "--desktop-dir", str(output_dir)],
        check=True,
    )
    py_compile.compile(str(output_dir / "app.py"), doraise=True)

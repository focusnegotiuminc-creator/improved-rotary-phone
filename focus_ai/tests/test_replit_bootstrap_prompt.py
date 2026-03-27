import subprocess
import sys


def test_bootstrap_prompt_includes_required_exports():
    result = subprocess.run(
        [sys.executable, "focus_ai/scripts/build_replit_bootstrap_prompt.py", "--default-repo", "acme/focus"],
        capture_output=True,
        text=True,
        check=True,
    )

    output = result.stdout
    assert "export GITHUB_TOKEN='REPLACE_WITH_NEW_GITHUB_TOKEN'" in output
    assert "INFINITYFREE_FTP_HOST" in output
    assert "github_ops.py merge-prs --repo \"acme/focus\"" in output
    assert "github_ops.py go-live --deploy" in output

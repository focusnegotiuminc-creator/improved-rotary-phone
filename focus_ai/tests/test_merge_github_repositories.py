import subprocess


def test_merge_script_dry_run_with_explicit_repos():
    result = subprocess.run(
        [
            "python3",
            "focus_ai/scripts/merge_github_repositories.py",
            "--owner",
            "acme",
            "--repos",
            "alpha",
            "beta",
            "--dry-run",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Dry run" in result.stdout
    assert "acme/alpha" in result.stdout
    assert "acme/beta" in result.stdout


def test_merge_script_help_mentions_auto_branch_mode():
    result = subprocess.run(
        ["python3", "focus_ai/scripts/merge_github_repositories.py", "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "default branch" in result.stdout and "auto" in result.stdout

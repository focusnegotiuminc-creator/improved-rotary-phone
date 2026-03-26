import shutil
from pathlib import Path
import subprocess


def test_build_public_site_outputs_bundle():
    subprocess.run(
        ["python3", "focus_ai/scripts/publish_ebooks.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    result = subprocess.run(
        ["python3", "focus_ai/scripts/build_public_site.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Built public site" in result.stdout

    out = Path("focus_ai/published/public_site")
    assert (out / "index.html").exists()
    assert (out / "landing.html").exists()
    assert (out / "funnel_landing.html").exists()
    assert (out / "delivery.html").exists()
    assert (out / "book_offer.html").exists()
    assert (out / "upsell.html").exists()
    assert (out / "high_ticket.html").exists()
    assert (out / "email_automation.html").exists()
    assert (out / "ebooks" / "index.html").exists()
    shutil.rmtree(out)

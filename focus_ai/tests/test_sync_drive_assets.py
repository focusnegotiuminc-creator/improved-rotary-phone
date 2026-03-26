import importlib.util
import io
import zipfile
from pathlib import Path

MODULE_PATH = Path("focus_ai/scripts/sync_drive_assets.py")
spec = importlib.util.spec_from_file_location("sync_drive_assets", MODULE_PATH)
sync_drive_assets = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(sync_drive_assets)


def test_extract_drive_file_id_from_standard_url():
    url = "https://drive.google.com/file/d/abc123XYZ/view?usp=drive_link"
    assert sync_drive_assets.extract_drive_file_id(url) == "abc123XYZ"


def test_unpack_zip_extracts_files(tmp_path: Path):
    payload = io.BytesIO()
    with zipfile.ZipFile(payload, mode="w") as archive:
        archive.writestr("folder/asset.txt", "hello")

    count = sync_drive_assets.unpack_zip(payload.getvalue(), tmp_path)

    assert count == 1
    assert (tmp_path / "folder" / "asset.txt").read_text(encoding="utf-8") == "hello"

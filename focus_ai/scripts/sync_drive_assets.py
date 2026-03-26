#!/usr/bin/env python3
"""Download Google Drive zip assets, extract them, and run the local workflow checks."""

from __future__ import annotations

import argparse
import io
import re
import shutil
import zipfile
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
IMPORTS_DIR = ROOT / "imports"

DEFAULT_URLS = [
    "https://drive.google.com/file/d/13YSO4chuNl80LVoBb0dvDPf6Ssp1Y1zR/view?usp=drive_link",
    "https://drive.google.com/file/d/1JAF3x54Q4PA1NL68NrDnDNog49MTT9Jg/view?usp=drive_link",
]


def extract_drive_file_id(url: str) -> str:
    parsed = urlparse(url)
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", parsed.path)
    if match:
        return match.group(1)

    query_file_id = parse_qs(parsed.query).get("id")
    if query_file_id:
        return query_file_id[0]

    raise ValueError(f"Could not parse a Google Drive file id from URL: {url}")


def download_drive_bytes(url: str) -> bytes:
    file_id = extract_drive_file_id(url)
    direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    req = Request(direct_url, headers={"User-Agent": "Focus-AI-Sync/1.0"})
    with urlopen(req, timeout=60) as response:
        content = response.read()

    if b"Google Drive - Virus scan warning" in content or b"confirm=" in content:
        text = content.decode("utf-8", errors="ignore")
        match = re.search(r"confirm=([0-9A-Za-z_]+)", text)
        if not match:
            raise RuntimeError("Google Drive confirmation token not found for large file download")
        confirm = match.group(1)
        confirmed = f"{direct_url}&confirm={confirm}"
        req2 = Request(confirmed, headers={"User-Agent": "Focus-AI-Sync/1.0"})
        with urlopen(req2, timeout=60) as response:
            content = response.read()

    return content


def unpack_zip(content: bytes, destination: Path) -> int:
    extracted = 0
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            extracted += 1
            archive.extract(info, destination)
    return extracted


def run_sync(urls: list[str], clean: bool = False) -> int:
    IMPORTS_DIR.mkdir(parents=True, exist_ok=True)

    if clean and IMPORTS_DIR.exists():
        shutil.rmtree(IMPORTS_DIR)
        IMPORTS_DIR.mkdir(parents=True, exist_ok=True)

    total_files = 0
    for index, url in enumerate(urls, start=1):
        subdir = IMPORTS_DIR / f"drive_asset_{index}"
        subdir.mkdir(parents=True, exist_ok=True)

        print(f"Downloading: {url}")
        try:
            content = download_drive_bytes(url)
            count = unpack_zip(content, subdir)
        except zipfile.BadZipFile as error:
            print(f"Failed: downloaded content is not a zip archive ({error})")
            return 1
        except Exception as error:  # noqa: BLE001
            print(f"Failed to sync '{url}': {error}")
            return 1

        total_files += count
        print(f"Extracted {count} files into {subdir}")

    print(f"Sync complete. Extracted {total_files} files from {len(urls)} archive(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync zip assets from Google Drive links")
    parser.add_argument("urls", nargs="*", help="Google Drive links to zip files")
    parser.add_argument("--clean", action="store_true", help="Delete existing imports before extracting")
    args = parser.parse_args()

    urls = args.urls or DEFAULT_URLS
    return run_sync(urls, clean=args.clean)


if __name__ == "__main__":
    raise SystemExit(main())

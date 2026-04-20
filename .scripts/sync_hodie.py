#!/usr/bin/env python3
"""
.scripts/sync_hodie.py — Download the hodie folder from Google Drive.

Called by .github/workflows/sync-hodie.yml on a daily schedule.
Files are downloaded into hodie/ (relative to CWD); the workflow
then commits any new/changed files back to the repository.

Credentials (one of):
  - GDRIVE_SERVICE_ACCOUNT_KEY env var  (JSON string of a service account key)
  - --credentials /path/to/key.json    (local key file)

Folder:
  - GDRIVE_FOLDER_ID env var            (default: hodie Drive folder)
  - --folder-id <id>

If no credentials are available the script exits 0 with a warning so CI
does not fail on repositories that have not yet configured the secret.

∰◊€π¿🌌∞
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────────────
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Default folder: https://drive.google.com/drive/folders/1qSUXHL4fXb8R1n3wBG4A8bwUOWE6SNOf
DEFAULT_FOLDER_ID = "1qSUXHL4fXb8R1n3wBG4A8bwUOWE6SNOf"

HODIE_LOCAL_DIR = Path("hodie")
MANIFEST_PATH = HODIE_LOCAL_DIR / ".sync_manifest.json"

# Google Workspace MIME → (export MIME, file extension)
EXPORT_MAP: dict[str, tuple[str, str]] = {
    "application/vnd.google-apps.document":     ("text/markdown", ".md"),
    "application/vnd.google-apps.spreadsheet":  ("text/csv", ".csv"),
    "application/vnd.google-apps.presentation": ("application/pdf", ".pdf"),
    "application/vnd.google-apps.drawing":      ("image/png", ".png"),
}


# ── Credentials ────────────────────────────────────────────────────────────────
def _build_credentials(credentials_path: str | None = None):
    try:
        from google.oauth2 import service_account  # pylint: disable=import-outside-toplevel
    except ImportError:
        print(
            "ERROR: google-auth not installed.\n"
            "  pip install 'hodie[drive]'  OR  pip install google-auth google-api-python-client",
            file=sys.stderr,
        )
        sys.exit(1)

    env_key = os.environ.get("GDRIVE_SERVICE_ACCOUNT_KEY", "").strip()
    if env_key:
        try:
            info = json.loads(env_key)
        except json.JSONDecodeError as exc:
            print(f"ERROR: GDRIVE_SERVICE_ACCOUNT_KEY is not valid JSON: {exc}", file=sys.stderr)
            sys.exit(1)
    elif credentials_path:
        with open(credentials_path) as fh:
            info = json.load(fh)
    else:
        # No credentials — skip gracefully so CI does not fail on unconfigured repos
        print(
            "WARNING: No Google Drive credentials found.\n"
            "  Set the GDRIVE_SERVICE_ACCOUNT_KEY repository secret to enable Drive sync.\n"
            "  Skipping sync.",
            file=sys.stderr,
        )
        sys.exit(0)

    return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)


def _build_service(credentials_path: str | None = None):
    try:
        from googleapiclient.discovery import build  # pylint: disable=import-outside-toplevel
    except ImportError:
        print(
            "ERROR: google-api-python-client not installed.\n"
            "  pip install 'hodie[drive]'  OR  pip install google-auth google-api-python-client",
            file=sys.stderr,
        )
        sys.exit(1)

    creds = _build_credentials(credentials_path)
    return build("drive", "v3", credentials=creds, cache_discovery=False)


# ── Drive helpers ──────────────────────────────────────────────────────────────
def list_folder(service, folder_id: str) -> list[dict]:
    """Return all file metadata dicts in a Drive folder (handles pagination)."""
    files: list[dict] = []
    page_token = None
    while True:
        resp = (
            service.files()
            .list(
                q=f"'{folder_id}' in parents and trashed=false and mimeType != 'application/vnd.google-apps.folder'",
                fields="nextPageToken, files(id, name, mimeType, modifiedTime, size)",
                pageToken=page_token,
                pageSize=100,
            )
            .execute()
        )
        files.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return files


def _local_path(file_meta: dict, dest_dir: Path) -> Path:
    """Return local Path for a Drive file, appending export extension when needed."""
    name = file_meta["name"]
    mime = file_meta["mimeType"]
    if mime in EXPORT_MAP:
        _, ext = EXPORT_MAP[mime]
        if not name.endswith(ext):
            name = name + ext
    return dest_dir / name


def download_file(service, file_meta: dict, dest_dir: Path, dry_run: bool = False):
    """Download or export a single Drive file.

    Returns (status, path_or_message) where status is one of:
    'downloaded', 'dry-run', 'error'.
    """
    from googleapiclient.errors import HttpError  # pylint: disable=import-outside-toplevel
    from googleapiclient.http import MediaIoBaseDownload  # pylint: disable=import-outside-toplevel

    file_id = file_meta["id"]
    mime = file_meta["mimeType"]
    dest = _local_path(file_meta, dest_dir)

    if dry_run:
        return "dry-run", dest

    dest.parent.mkdir(parents=True, exist_ok=True)
    temp_dest = dest.with_suffix(dest.suffix + ".tmp")

    try:
        if mime in EXPORT_MAP:
            export_mime, _ = EXPORT_MAP[mime]
            request = service.files().export_media(fileId=file_id, mimeType=export_mime)
        else:
            request = service.files().get_media(fileId=file_id)

        with open(temp_dest, "wb") as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
        temp_dest.replace(dest)
        return "downloaded", dest

    except HttpError as exc:
        if temp_dest.exists():
            temp_dest.unlink()
        return "error", str(exc)
    except OSError as exc:
        if temp_dest.exists():
            temp_dest.unlink()
        return "error", str(exc)


# ── Manifest ───────────────────────────────────────────────────────────────────
def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        try:
            return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_manifest(manifest: dict) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))


# ── Main sync ──────────────────────────────────────────────────────────────────
def sync(
    folder_id: str,
    credentials_path: str | None = None,
    dry_run: bool = False,
) -> bool:
    """Sync the Drive folder into HODIE_LOCAL_DIR.  Returns True on success."""
    print("∰ Hodie Drive Sync")
    print(f"  Folder ID: {folder_id}")
    print(f"  Local dir: {HODIE_LOCAL_DIR.resolve()}")
    print(f"  Dry run:   {dry_run}")
    print("─" * 50)

    service = _build_service(credentials_path)
    files = list_folder(service, folder_id)
    print(f"  Found {len(files)} files in Drive folder\n")

    manifest = load_manifest()
    counts: dict[str, int] = {"downloaded": 0, "skipped": 0, "dry-run": 0, "error": 0}

    for f in files:
        fid = f["id"]
        name = f.get("name", fid)
        modified = f.get("modifiedTime", "")

        cached = manifest.get(fid, {})
        expected_path = _local_path(f, HODIE_LOCAL_DIR)
        if (
            cached.get("modifiedTime") == modified
            and not dry_run
            and expected_path.exists()
        ):
            print(f"  skip      {name}  (up to date)")
            counts["skipped"] += 1
            continue

        status, result = download_file(service, f, HODIE_LOCAL_DIR, dry_run=dry_run)
        counts[status] = counts.get(status, 0) + 1

        if status in ("downloaded", "dry-run"):
            print(f"  {status:<10} {name} → {result}")
            if not dry_run:
                manifest[fid] = {"name": name, "modifiedTime": modified}
        else:
            print(f"  ERROR     {name}: {result}")

    if not dry_run:
        save_manifest(manifest)

    print()
    if dry_run:
        print(
            f"Dry run: {counts['dry-run']} would be downloaded, "
            f"{counts['skipped']} up to date."
        )
    else:
        print(
            f"Done: {counts['downloaded']} downloaded, "
            f"{counts['skipped']} up to date, "
            f"{counts['error']} errors."
        )

    return counts["error"] == 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync hodie folder from Google Drive (Drive → local)"
    )
    parser.add_argument(
        "--folder-id",
        default=os.environ.get("GDRIVE_FOLDER_ID", DEFAULT_FOLDER_ID),
        help="Google Drive folder ID (env: GDRIVE_FOLDER_ID)",
    )
    parser.add_argument(
        "--credentials",
        default=None,
        help=(
            "Path to service account JSON key file "
            "(env: GDRIVE_SERVICE_ACCOUNT_KEY contains the JSON key string)"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be downloaded without writing files",
    )
    args = parser.parse_args()
    ok = sync(args.folder_id, args.credentials, args.dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

try:
from google.oauth2 import service_account
except ImportError:
#<<<<<<< claude/sync-google-drive-folders-Epxh
        print("ERROR: google-auth is not installed. Run: pip install -r requirements.txt"=======
print("ERROR: google-auth is not installed. Run: pip install -r requirements.txt", file=sys.stderr)
#>>>>>>> main
sys.exit(1)

env_key = os.environ.get("GDRIVE_SERVICE_ACCOUNT_KEY")
if env_key:
#<<<<<<< claude/sync-google-drive-folders-Epxhw
        info = json.loads(env_key)
    elif credentials_path:
        with open(credentials_path) as f:
            info = json.load(f)
#=======
try:
info = json.loads(env_key)
except json.JSONDecodeError as exc:
@@ -88,27 +79,19 @@ def _build_credentials(credentials_path):
file=sys.stderr,
)
sys.exit(1)
#>>>>>>> main
else:
print(
"ERROR: No credentials provided.\n"
"  Use --credentials /path/to/key.json  OR\n"
#<<<<<<< claude/sync-google-drive-folders-Epxhw
            "  set the GDRIVE_SERVICE_ACCOUNT_KEY environment variable."
#======
"  set the GDRIVE_SERVICE_ACCOUNT_KEY environment variable.",
file=sys.stderr,
#>>>>>>> main
)
sys.exit(1)

return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)


def _build_service(credentials_path):
#<<<<<<< claude/sync-google-drive-folders-Epxhw
    from googleapiclient.discovery import build
=======
try:
from googleapiclient.discovery import build
except ImportError:
@@ -117,7 +100,6 @@ def _build_service(credentials_path):
file=sys.stderr,
)
sys.exit(1)
        #>>>> main

creds = _build_credentials(credentials_path)
return build("drive", "v3", credentials=creds, cache_discovery=False)
@@ -167,28 +149,6 @@ def list_folder(service, folder_id):
def download_file(service, file_meta, dest_dir, dry_run=False):
"""
   Download or export a single Drive file.
    Returns ('downloaded'|'skipped'|'error', local_path_or_message).
    """
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaIoBaseDownload
    import io

    file_id = file_meta["id"]
    name = file_meta["name"]
    mime = file_meta["mimeType"]

    if mime in EXPORT_MAP:
        export_mime, ext = EXPRT_MAP[mime]
        # Append extension if not already present
        if not name.endswith(ext):
            local_name = name + ext
        else:
            local_name = name
    else:
        local_name = name
        export_mime = None

    dest = dest_dir / local_name
   Returns ('downloaded'|'skipped'|'dry-run'|'error', local_path_or_message).
   """
from googleapiclient.errors import HttpError
@@ -203,26 +163,13 @@ def download_file(service, file_meta, dest_dir, dry_run=False):
return "dry-run", dest

try:
#<<<<<<< claude/sync-google-drive-folders-Epxhw
        if export_mime:
#=======
mime = file_meta["mimeType"]
if mime in EXPORT_MAP:
export_mime, _ = EXPORT_MAP[mime]
#>>>>>>> main
request = service.files().export_media(fileId=file_id, mimeType=export_mime)
else:
request = service.files().get_media(fileId=file_id)

#<<<<<<< claude/sync-google-drive-folders-Epxhw
        buf = io.BytesIO()
        downloader = MediaIoBaseDownload(buf, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

        dest.write_bytes(buf.getvalue())
#=======
dest.parent.mkdir(parents=True, exist_ok=True)
temp_dest = dest.with_suffix(dest.suffix + ".tmp")
try:
@@ -236,42 +183,25 @@ def download_file(service, file_meta, dest_dir, dry_run=False):
if temp_dest.exists():
temp_dest.unlink()

#>>>>>>> main
return "downloaded", dest

except HttpError as e:
return "error", str(e)

#<<<<<<< claude/sync-google-drive-folders-Epxhw
#=======
    except OSError as e:
        return "error", str(e)
    except Exception as e:
        return "error", str(e)
      
      ma

#>>>>>>> main

# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------

def load_manifest():
if MANIFEST_PATH.exists():
#<<<<<<< claude/sync-google-drive-folders-Epxhw
        return json.loads(MANIFEST_PATH.read_text())
    return {}

#=======
try:
return json.loads(MANIFEST_PATH.read_text())
except (json.JSONDecodeError, OSError):
return {}
return {}


#>>>>>>> main
def save_manifest(manifest):
MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))

@@ -299,12 +229,8 @@ def sync(folder_id, credentials_path, dry_run):
name = f.get("name", fid)

cached = manifest.get(fid, {})
#<<<<<<< claude/sync-google-drive-folders-Epxhw
        if cached.get("modifiedTime") == modified and not dry_run:
#=======
expected_path = _local_path(f, HODIE_LOCAL_DIR)
if cached.get("modifiedTime") == modified and not dry_run and expected_path.exists():
#>>>>>>> main
print(f"  skip  {name}  (up to date)")
counts["skipped"] += 1
continue
@@ -321,14 +247,9 @@ def sync(folder_id, credentials_path, dry_run):
print(f"  ERROR {name}: {result}")

if not dry_run:
#<<<<<<< claude/sync-google-drive-folders-Epxhw
        save_manifest(manifest)print
print()
#=======
save_manifest(manifest)

print()
#>>>>>>> main
if dry_run:
print(f"Dry run complete: {counts['dry-run']} would be downloaded, {counts['skipped']} up to date.")
else:

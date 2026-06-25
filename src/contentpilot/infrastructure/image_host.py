"""Google Drive image host adapter.

Uploads an image to Drive, makes it public, and returns a Google-CDN URL
(`lh3.googleusercontent.com/d/<id>=w1200`) that hotlinks reliably into Blogger
posts. Drive auth uses the Hermes Google token (the only one with Drive scope);
this is the one infra detail that reaches outside the project workspace.
"""
from __future__ import annotations

from pathlib import Path

from ..application.ports import ImageHostPort

HERMES_TOKEN = Path.home() / ".hermes" / "google_token.json"
DRIVE_SCOPE = ["https://www.googleapis.com/auth/drive"]
_MIME = {".webp": "image/webp", ".png": "image/png",
         ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


class DriveImageHost(ImageHostPort):
    def __init__(self, token_path: Path = HERMES_TOKEN):
        self._token_path = token_path

    def _drive(self):
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        creds = Credentials.from_authorized_user_file(str(self._token_path), DRIVE_SCOPE)
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            self._token_path.write_text(creds.to_json())
        return build("drive", "v3", credentials=creds)

    def upload_public(self, local_path: str) -> str:
        from googleapiclient.http import MediaFileUpload

        drive = self._drive()
        p = Path(local_path)
        media = MediaFileUpload(
            str(p), mimetype=_MIME.get(p.suffix.lower(), "image/webp"), resumable=False
        )
        f = drive.files().create(body={"name": p.name}, media_body=media, fields="id").execute()
        fid = f["id"]
        drive.permissions().create(
            fileId=fid, body={"type": "anyone", "role": "reader"}
        ).execute()
        return f"https://lh3.googleusercontent.com/d/{fid}=w1200"

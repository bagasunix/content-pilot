"""Blogger publisher adapter.

The OAuth-readiness check and the real Blogger API v3 upload live here. The
upload creates an UNPUBLISHED draft post (isDraft=True) — going live stays a
separate, human-gated action. The use case stays unaware of HTTP/OAuth/HTML.
"""
from __future__ import annotations

from ..application.ports import PublisherPort
from .html import markdown_to_html
from .paths import Workspace

SCOPES = ["https://www.googleapis.com/auth/blogger"]


class BloggerPublisher(PublisherPort):
    def __init__(self, ws: Workspace):
        self._ws = ws

    def token_available(self) -> bool:
        return self._ws.token.exists()

    def _service(self):
        # Imported lazily so the package (and its fast unit tests) don't require
        # google-api libs unless a real upload is actually attempted.
        import yaml
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        creds = Credentials.from_authorized_user_file(str(self._ws.token), SCOPES)
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            self._ws.token.write_text(creds.to_json())
        cfg = yaml.safe_load(self._ws.config.read_text())
        return build("blogger", "v3", credentials=creds), str(cfg["blog_id"])

    def upload_draft(self, title: str, content: str, labels: list | None = None) -> dict:
        service, blog_id = self._service()
        body = {
            "kind": "blogger#post",
            "title": title,
            "content": markdown_to_html(content),
            "labels": labels or [],
        }
        result = service.posts().insert(
            blogId=blog_id, body=body, isDraft=True
        ).execute()
        return {"id": result["id"], "url": result.get("url", ""), "title": result["title"]}

    def update_post(self, post_id: str, content: str) -> None:
        service, blog_id = self._service()
        service.posts().patch(
            blogId=blog_id, postId=post_id,
            body={"content": markdown_to_html(content)},
        ).execute()

"""Simulate a GitHub push webhook locally, with correct HMAC signature."""
import hashlib
import hmac
import json

import httpx

SECRET = "dev-webhook-secret-change-me"  # must match .env GITHUB_WEBHOOK_SECRET
URL = "http://localhost:8000/webhooks/github"

payload = {
    "repository": {
        "name": "SAGE",
        "owner": {"login": "lakshit2234"},
    }
}
body = json.dumps(payload).encode()
signature = "sha256=" + hmac.new(SECRET.encode(), body, hashlib.sha256).hexdigest()

resp = httpx.post(
    URL,
    content=body,
    headers={
        "Content-Type": "application/json",
        "X-Hub-Signature-256": signature,
        "X-GitHub-Event": "push",
    },
)
print(resp.status_code, resp.json())
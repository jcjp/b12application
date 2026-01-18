import json
import hmac
import hashlib
import os
from datetime import datetime, timezone

import requests

ENDPOINT = "https://b12.io/apply/submission"
SIGNING_SECRET = b"hello-there-from-b12"

def iso8601_timestamp():
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )

def main():
    action_run_id = os.environ["GITHUB_RUN_ID"]
    repository = os.environ["GITHUB_REPOSITORY"]
    server_url = os.environ["GITHUB_SERVER_URL"]

    payload = {
        "action_run_link": f"{server_url}/{repository}/actions/runs/{action_run_id}",
        "email": "personal.chamver@gmail.com",
        "name": "John Chamver Puno",
        "repository_link": f"{server_url}/{repository}",
        "resume_link": "https://drive.google.com/drive/folders/1uWs28XPTgRsuE0uye877MguDgZhDVM9c",
        "timestamp": iso8601_timestamp(),
    }

    body = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    digest = hmac.new(
        SIGNING_SECRET,
        body,
        hashlib.sha256,
    ).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": f"sha256={digest}",
    }

    response = requests.post(
        ENDPOINT,
        data=body,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()
    receipt = result.get("receipt")

    if receipt:
        print("Submission receipt:", receipt)
    else:
        raise RuntimeError("No receipt returned")

if __name__ == "__main__":
    main()

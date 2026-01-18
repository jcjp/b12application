# B12 Application Submission (CI-Based)

This repository contains a Python script and GitHub Actions workflow
that **submits an application to B12 via a signed HTTP POST request**,
executed from continuous integration.

The submission is **triggered manually**, runs in GitHub Actions, and
posts a **cryptographically signed, canonical JSON payload** to the B12
application endpoint. The CI run itself serves as verifiable proof of
execution.

------------------------------------------------------------------------

## Overview

The application submission works as follows:

1.  A GitHub Actions workflow is manually triggered.
2.  The workflow runs a Python script.
3.  The script:
    -   Constructs a required JSON payload
    -   Canonicalizes it (sorted keys, compact formatting, UTF-8)
    -   Signs it using HMAC-SHA256
    -   Sends it via POST to the B12 endpoint
4.  On success, the CI logs print a **receipt**, which confirms
    submission.

------------------------------------------------------------------------

## Files

    .
    ├── submit_application.py
    ├── .github/
    │   └── workflows/
    │       └── submit.yml
    └── README.md

------------------------------------------------------------------------

## Requirements

-   Python **3.9+**
-   GitHub Actions (or another CI system with equivalent environment
    variables)
-   Internet access from CI

Python dependencies: - `requests`

------------------------------------------------------------------------

## Payload Details

The script submits a JSON payload with the following required fields:

``` json
{
  "timestamp": "ISO 8601 timestamp (UTC)",
  "name": "Your name",
  "email": "you@example.com",
  "resume_link": "https://pdf-or-html-or-linkedin.example.com",
  "repository_link": "https://github.com/your/repo",
  "action_run_link": "https://github.com/your/repo/actions/runs/<run_id>"
}
```

------------------------------------------------------------------------

## Request Signing

Each request includes a signature header:

    X-Signature-256: sha256=<hex-digest>

The signature is computed using **HMAC-SHA256** over the raw UTF-8
encoded JSON body.

------------------------------------------------------------------------

## Running the Submission

Trigger the workflow manually from the **Actions** tab in GitHub.\
On success, the logs will print a submission receipt.

------------------------------------------------------------------------

## License

Provided solely for submitting an application to B12.

# Public demo safety and hosting requirements

The current application is a local MVP. Do not expose it directly to the internet unchanged. A recruiter-accessible demo should be a separate, stateless showcase deployment.

## Required public-demo defaults

- Synthetic examples only; prominently prohibit customer, employer, personal, confidential, or production data.
- Disable file uploads.
- Disable SQLite memory and all persistence (`save_to_memory = false`).
- Do not publish private/local knowledge folders or historical research archives.
- Expose only the VMware Case Agent workflow and a small allowlisted set of synthetic prompts.
- Do not expose `/memory` or unrestricted `/knowledge/search` endpoints.
- Enforce request-size limits, rate limiting, timeouts, safe error messages, and basic abuse monitoring.
- Add an explicit acknowledgement before analysis: “I will use synthetic data only.”
- Keep infrastructure execution unavailable; never accept credentials or connect to vCenter/ESXi/VCF systems.
- Display that output is educational/advisory, may be incomplete, and must be verified against current official Broadcom documentation.
- Provide a contact/feedback route that does not reveal a private email address unnecessarily.

## Recommended public architecture

Use a public repository containing a dedicated demo entry point. Host the stateless Streamlit experience on a reputable app platform, or host the API and UI separately with an environment-configured API URL. Keep the full local application and local knowledge/memory outside the public deployment.

```text
LinkedIn Project / Featured post
              |
              v
Public synthetic-only demo
  |-- allowlisted prompts
  |-- no uploads
  |-- no persistence
  |-- no private knowledge
  `-- no infrastructure execution
```

## Visible privacy notice

> This public portfolio demo is for synthetic VMware scenarios only. Do not enter customer, employer, personal, confidential, production, credential, case, hostname, IP-address, or private-link data. Inputs are not intended for operational support. The tool is advisory and does not connect to or change infrastructure. Verify all guidance against current official documentation and your organization’s change process.

## Suggested tester consent

> I understand this is a portfolio demonstration. I will use only synthetic information and will not submit customer, employer, personal, confidential, or production data.

## Pre-publication security gate

1. Create a clean public repository from an allowlisted export; do not publish the current folder blindly.
2. Run privacy and unit tests.
3. Scan the working tree and repository history for secrets and sensitive identifiers.
4. Review every Markdown, JSON, fixture, log, database, image, and generated artifact manually.
5. Confirm uploads, memory, private knowledge search, debug mode, stack traces, and infrastructure integrations are absent.
6. Test rate limits, oversized inputs, malformed requests, and refresh/restart behavior.
7. Verify the demo and source links from a signed-out browser.
8. Record the deployed commit and rollback procedure.

## Go/no-go rule

Publish only when every required default and security-gate item passes. If the synthetic-only deployment is not ready, publish the LinkedIn project with the public demonstration document and repository README, label the live demo “coming soon,” and do not expose the local service.


# Chat Exporter

Automated nightly export of ChatGPT & Claude conversations to JSON/Markdown/PDF,
scheduled via k3s CronJob at 03:00 (America/New_York).

## Quickstart
```bash
git clone <repo>
cd chat-exporter
make venv
make test-run  # local headless test
```

## Output Directory
Exports are written to `${OUTPUT_DIR:-/tmp/exports}/<date>/`. The `outputs` rule
shows where today's export will be saved.

See `k8s/` for deployment manifests and `.gitlab-ci.yml` for CI pipeline.

_Generated 2025-05-21_

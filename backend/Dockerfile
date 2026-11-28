# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base
WORKDIR /srv/backend

FROM base AS migrate
COPY app/ app/
COPY migrations/ migrations/
CMD ["python", "-m", "app.links.migrate"]

FROM base AS api
COPY pyproject.toml .
RUN python - <<'PY'
import subprocess
import sys
import tomllib

with open("pyproject.toml", "rb") as project:
    dependencies = tomllib.load(project)["project"]["dependencies"]
subprocess.run([sys.executable, "-m", "pip", "install", "--no-cache-dir", *dependencies], check=True)
PY
COPY --from=migrate /srv/backend/ .
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]

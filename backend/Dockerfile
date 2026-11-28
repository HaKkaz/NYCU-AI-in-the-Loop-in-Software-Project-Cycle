FROM python:3.12-slim AS migrate
WORKDIR /srv/backend
COPY app/ app/
COPY migrations/ migrations/
CMD ["python", "-m", "app.links.migrate"]

FROM migrate AS api
COPY pyproject.toml .
RUN python -m pip install --no-cache-dir .
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]

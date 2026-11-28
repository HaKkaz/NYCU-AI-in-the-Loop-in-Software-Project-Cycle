FROM python:3.12-slim AS migrate
WORKDIR /srv/backend
COPY app/ app/
COPY migrations/ migrations/
CMD ["python", "-m", "app.links.migrate"]

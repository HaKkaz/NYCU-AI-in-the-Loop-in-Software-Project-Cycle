# NYCU-AI-in-the-Loop-in-Software-Project-Cycle

## SQLite migrations

From the repository root, run `docker compose run --build --rm migrate`. The default SQLite file is `backend/data/app.db`. Both local and container runs use that file with these defaults.

For local development, use Python 3.11 or later and run the following from the repository root.

```sh
cd backend
python -m app.links.migrate
python -m app.links.migrate --check
python -m pip install -e ".[test]"
python -m pytest
```

Set `DATABASE_URL` to select a different database. For example, `sqlite:///./data/demo.db` places another file in the shared data directory. For an absolute path in Compose, both services need a mount that covers that path.

## FastAPI startup

Run `docker compose up --build api` from the repository root. Compose runs `migrate` first. When it succeeds, FastAPI starts and serves its OpenAPI page at `http://localhost:8000/docs`. The API checks the same SQLite file on each startup, including after a container restart.

To run FastAPI outside Compose, install the backend dependencies as above, then run the following from `backend/`. Use the same `DATABASE_URL` for both commands.

```sh
python -m app.links.migrate
python -m fastapi dev app/main.py
```

On each startup FastAPI opens the database read-only to check its version. A missing database, pending migration, or newer schema stops startup before the API accepts requests.

When implementing link operations, use `app.links.db.connect()` and record the link change and its event in the same transaction. Order history by `at, id` so events with matching timestamps have a stable order.

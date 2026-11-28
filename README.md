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

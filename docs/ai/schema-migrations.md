# SQLite migration work log

## PR 1 · Schema and migration runner

- Tool and model: OpenAI Codex, GPT-6.
- Request: Use the supplied product specification to define the database in two reviewable PRs. Follow the requested layout with standard-library `sqlite3`, tables `link` and `link_event`, a shared connection helper, and migrations ordered by `PRAGMA user_version`.
- Retained: SQL constraints, the partial unique index for an active decision–PR pair, transactional migration execution, the one-shot Compose service and the tests for F4, F8, F9 and §8.
- Revised during implementation: Adopted the requested singular table names, four-digit migration filenames and `app/links/` package. Table definitions live in SQL.
- Collaboration: The teammate requesting these database PRs supplied the specification and layout. Codex prepared the code and ran the local checks. Human review requested revisions. Approval is pending.
- Review revision: Removed the action-dependent check on `link_event.comment`. SQLite stores optional comments verbatim. The F6/F7 transition handlers will enforce required comments when those handlers are implemented.

## PR 2 · Event history and FastAPI startup

- Tool and model: OpenAI Codex, GPT-6.
- Request: Add the second SQL migration and a one-shot Compose migration service. Run `migrate()` at FastAPI startup so the schema is ready before accepting requests.
- Retained: Creation-event uniqueness, a backfill derived from saved creator/time, the status-change timestamp trigger, the shared database mount and FastAPI startup tests.
- PR review: The reviewer requested one owner for schema upgrades and an API image whose dependency layer can be reused when source code changes. Compose runs the migration service. FastAPI opens the database read-only and checks the version. The API image installs dependencies from `pyproject.toml` before copying the source.
- Collaboration: Codex implemented the two review comments on PR #16 and updated the startup tests.

# SQLite migration work log

## PR 1 · Schema and migration runner

- Tool and model: OpenAI Codex, GPT-6.
- Request: Use the supplied product specification to define the database in two reviewable PRs. Follow the requested layout with standard-library `sqlite3`, tables `link` and `link_event`, a shared connection helper, and migrations ordered by `PRAGMA user_version`.
- Retained: SQL constraints, the partial unique index for an active decision–PR pair, transactional migration execution, the one-shot Compose service and the tests for F4, F8, F9 and §8.
- Revised during implementation: Adopted the requested singular table names, four-digit migration filenames and `app/links/` package. Table definitions live in SQL.
- Collaboration: The teammate requesting these database PRs supplied the specification and layout. Codex prepared the code and ran the local checks. Human review requested revisions. Approval is pending.
- Review revision: Removed the action-dependent check on `link_event.comment`. SQLite stores optional comments verbatim. The F6/F7 transition handlers will enforce required comments when those handlers are implemented.

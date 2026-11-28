# Decisions Log

## 2026-09-21 — Initial code steward
**What:** 林品安 (HaKkaz) is the code steward for the first rotation and reviews and approves every pull request into `main` during that period.
**Why:** 林品安 created the repository and configured branch protection and the PR template, so they had the most context on how the repository is set up.
**Led by:** 林品安 (HaKkaz)

## 2026-11-29 — Backend uses FastAPI
**What:** The backend API is implemented in Python with FastAPI.
**Why:** FastAPI validates requests and generates an OpenAPI reference at `/docs` directly from our Pydantic models, which gives the team one up-to-date contract for every endpoint.
**Alternative rejected:** Flask, which has no built-in request validation or generated API documentation.
**Led by:** 林品安 (HaKkaz)
**Code steward:** 林品安 (HaKkaz)

## 2026-11-29 — Database uses SQLite
**What:** Decision–PR links and their event history are persisted in SQLite; data fetched from GitHub is not stored.
**Why:** The persisted data is limited to a few hundred rows per repository, and SQLite runs in-process from a single file, so development machines and demo machines need no separate database server.
**Alternative rejected:** PostgreSQL, which adds a service to install and operate with no benefit at this data volume.
**Led by:** 林品安 (HaKkaz)
**Code steward:** 林品安 (HaKkaz)

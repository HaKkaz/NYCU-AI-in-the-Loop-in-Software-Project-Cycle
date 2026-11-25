# Decisions Log

## 2026-11-25 - Track B recovery plan

**Status:** accepted for the Week 12 recovery plan
**What:** Keep the project-history dashboard scope, but make the first end-to-end slice a Python CLI that merges `git log` events with dated entries from this file. The web dashboard and any AI summarization are deferred until the deterministic timeline works.
**Why:** The repository has no runnable prototype. A deterministic CLI is the smallest slice that proves the main collaboration task and can be tested without an API key.
**Alternative rejected:** Starting with a web UI or AI-generated summaries. Either option would add setup and evaluation work before the underlying history merge is proven.
**Led by:** `HaKkaz`
**Owner and date:** `HaKkaz`, 2026-11-28
**Consequence:** The team honestly remains Track B until a new contributor can run the documented command and see both commit and decision events.

## 2026-11-25 - Human-readable AI evidence in every PR

**Status:** accepted
**What:** Adopt the Week 12 PR template. Every PR states whether AI was used, what it generated, what the author changed, how the result was checked, and the main risk. A non-author review must name evidence that was checked; an empty approval or `LGTM` is not substantive evidence.
**Why:** Earlier PRs contain empty, emoji-only, or `LGTM` approvals, and most do not make AI involvement verifiable.
**Alternative rejected:** Relying on chat history or the author remembering how the change was produced.
**Led by:** `u7chi`

## 2026-11-25 - Steward and ownership for the recovery period

**Status:** accepted
**What:** `HaKkaz` is acting code steward for the Week 12 recovery update. The other owners are `iris2617` for README/setup, `milktea7654` for decisions and dates, and `u7chi` for AI evidence and PR process.
**Why:** Track B work needs explicit ownership and dates that an outside reviewer can verify.
**Alternative rejected:** Keeping `[Name]` placeholders or assigning work only in private chat.
**Led by:** Group 13

## 2026-09-21 - Initial project direction

**Status:** superseded in part by the 2026-11-25 recovery plan
**What:** Explore a dashboard that helps teammates reconstruct project history from Git activity and human-authored decisions.
**Why:** Important context is split between implementation history and decision records.

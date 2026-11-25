# Phase 3 Recovery Plan

## Objective

Move Group 13 from Track B to a verifiable walking skeleton without hiding the current gap.

## Smallest end-to-end slice

Build a Python CLI that accepts a repository path, reads `git log` and dated `DECISIONS.md` entries, combines them into chronological order, and prints each event with its source.

## Tasks

| Task | Owner | Target | Acceptance evidence |
|---|---|---|---|
| Define two event types and sample fixtures | `milktea7654` | 2026-11-27 | Fixture contains one commit and one decision |
| Implement parsing and timeline ordering | `HaKkaz` | 2026-11-28 | Automated test passes |
| Add CLI command and README instructions | `iris2617` | 2026-11-28 | Fresh clone can run one command |
| Review AI disclosure, tests, and risks | `u7chi` | 2026-11-28 | Substantive review comment and completed PR template |

## AI failure and unavailability

The walking skeleton is deterministic and must remain usable without AI. If AI summarization is added later:

- when the model is unavailable, the original commit and decision text remains visible and usable;
- malformed or unsupported output is rejected rather than displayed as fact;
- AI-generated summaries are labelled as AI drafts with links to their source events; and
- users can ignore or correct a summary without changing the underlying Git or decision record.

## Main risks

- `DECISIONS.md` entries may not have machine-readable dates; the CLI will report skipped entries with a reason.
- Git author dates and decision dates may use different time zones; the first slice will display the original timestamp and sort normalized values.
- A generated summary may invent causality; AI summarization stays out of the first slice.

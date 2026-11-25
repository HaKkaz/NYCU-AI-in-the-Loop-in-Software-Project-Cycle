# Project History Dashboard

Final project repository for Group 13 in CSIC30216, Fall 2026.

## Problem

Student software teams record implementation history in Git commits and pull requests, while the reasons for important choices live separately in `DECISIONS.md`. A teammate who did not make a change has to move between those sources to reconstruct what changed, why it changed, and what happened next.

The planned product is a small project-history dashboard that combines Git commit history and human-authored decision entries into one chronological timeline.

## Current status - Track B

As of 2026-11-25, the main task does **not** run end to end. It breaks before the first setup step because the repository does not yet contain a runnable prototype.

This is an explicit status statement, not a claim that a prototype exists. The current repository contains planning and process artifacts only:

- [`EVALUATION_PLAN.md`](EVALUATION_PLAN.md) - proposed evaluation method and thresholds;
- [`AI_USAGE_GUIDELINES.md`](AI_USAGE_GUIDELINES.md) - checkable rules for AI-assisted work;
- [`DECISIONS.md`](DECISIONS.md) - current decisions and ownership;
- [`PHASE3_PLAN.md`](PHASE3_PLAN.md) - the smallest recovery plan for Phase 3; and
- [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) - the Week 12 AI-augmented PR template.

## Planned main task

The first walking skeleton will be a Python CLI that:

1. accepts the path to a Git repository;
2. reads dated events from `git log` and `DECISIONS.md`;
3. sorts them into one timeline; and
4. prints the timeline with each event's source.

The first slice intentionally excludes a web UI and AI summarization. It is complete when another teammate can clone the repository, run one documented command, and see both commit and decision events.

## Phase 3 recovery

| Work | Owner | Target date |
|---|---|---|
| Implement the CLI walking skeleton and one automated test | `HaKkaz` | 2026-11-28 |
| Add exact setup and run instructions after the CLI lands | `iris2617` | 2026-11-28 |
| Keep decisions, owners, and dates current | `milktea7654` | 2026-11-27 |
| Enforce the PR template and AI evidence rules | `u7chi` | 2026-11-27 |

See [`PHASE3_PLAN.md`](PHASE3_PLAN.md) for acceptance criteria, risks, and fallback behavior.

## Team

- `HaKkaz`
- `iris2617`
- `u7chi`
- `milktea7654`

## AI assistance disclosure

OpenAI Codex helped audit the repository and draft the Week 12 documentation update. The team remains responsible for reviewing, correcting, and explaining every submitted artifact; the interaction is recorded in [`PROMPT_LOG.md`](PROMPT_LOG.md).

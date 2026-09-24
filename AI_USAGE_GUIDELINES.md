# Draft AI Usage Guidelines

## Section 1 — What AI tools we plan to use, and what we will use each for

- We will use OpenAI Codex to generate boilerplate code, initial test skeletons, and first drafts of docstrings or API documentation. A human team member must review, understand, and edit the output before it can be merged.
- We will use OpenAI Codex for syntax checks and one-off debugging questions. Its answers are suggestions and cannot be merged into `main` without human review.
- We will use OpenAI Codex to brainstorm and compare architecture options. The team will make the final decision and record significant choices in `DECISIONS.md`.
- We will not use AI as the final authority for authentication, authorization, credentials, or other security-critical logic. Such code must be written or fully verified by a human team member.

## Section 2 — How we will document AI interactions

- Every prompt that produces code, text, or a decision that ends up in the repository will be recorded in the prompt engineering log. The entry will include the prompt, the model used, and what the team kept or changed.
- One-off syntax lookups or debugging questions do not require a log entry when their output does not become repository code, text, or a project decision.
- The collaboration log will record which team member used AI, what task it supported, and which team member reviewed or edited the result.
- Every PR description will state whether AI was involved and point to the relevant log entry when one is required.
- If an AI suggestion changes the team's actual approach, the decision and its reasoning will also be recorded in `DECISIONS.md`.

## Section 3 — How we will handle disagreements about AI output quality

- If team members disagree about whether AI-generated work is good enough to merge, the code steward has final say.
- Before AI-generated code can be merged, it must pass the existing test suite and the PR review checklist, and a team member other than the person who generated it must be able to explain it.
- Disagreements about style or preference will be resolved using the team's existing style guide and linter configuration.
- A vote alone is not evidence. If the evidence does not resolve the disagreement, the code steward will make the final decision and record a one-sentence explanation in `DECISIONS.md`.

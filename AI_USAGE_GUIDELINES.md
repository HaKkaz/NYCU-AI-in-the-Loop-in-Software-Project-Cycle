# AI Usage Guidelines

Updated from the Week 3 draft using the repository evidence reviewed in Week 12.

## Current rules

### 1. Make AI assistance visible in the pull request

Every PR fills in the `AI assistance` section of `.github/PULL_REQUEST_TEMPLATE.md`. It either says `none`, or names the tool/model, the files or functions generated, the instruction given, and what the author changed afterwards. A reviewer must not approve while this section is empty.

### 2. Require human evidence, not an empty approval

Before merge, the author reads every changed line and records the tests or manual checks performed. A teammate other than the author leaves a substantive review comment that names at least one thing checked and any question, concern, or reason no concern remains. An empty approval, emoji, or `LGTM` alone does not count.

### 3. Keep consequential AI interactions traceable

When AI-generated code, documentation, or a project decision enters the repository, the same PR adds or links a prompt-log entry containing the request, the kind of output, what was accepted/changed/rejected, and the intent-output lesson. Significant engineering choices also receive a `DECISIONS.md` entry led by a named human.

## Boundaries

- AI output is a draft; a human owns the submitted result and must be able to explain it without asking AI.
- AI cannot approve or merge its own work or make the final decision about accepting a contribution.
- No secrets, credentials, private data, or other teams' private information may be placed in prompts or committed.
- Security-critical behavior requires human verification against tests and authoritative documentation.

## Week 12 evidence and rule changes

Repository evidence for the last two weeks: **0 PRs mostly AI-generated, 0 PRs another teammate could demonstrate explaining line by line, and 0 PRs that say what the AI did**. The counts are zero because no PRs were merged during that period; older PRs were inspected to identify process gaps.

| # | Old Week 3 wording | New checkable rule | Evidence |
|---|---|---|---|
| 1 | "A human team member must review, understand, and edit the output before it can be merged." | The PR must complete every AI-assistance field (or say `none`), and a reviewer blocks approval while it is empty. | PRs #1-#3 contain no AI disclosure; PR #4 mentions Codex but does not identify files or author changes. |
| 2 | "AI-generated code must pass the existing test suite and the PR review checklist, and another member must be able to explain it." | The PR records exact checks, and a non-author review comment names evidence checked plus a question, concern, or explicit conclusion. | Reviews on PRs #2 and #3 are empty, PR #1 is emoji-only, and PRs #4 and #6 only say `LGTM`. |
| 3 | "Every prompt that produces repository content will be recorded in the prompt engineering log." | The same PR adds or links a prompt-log entry with request, output, decision, and intent-output lesson; a significant choice also links `DECISIONS.md`. | The repository promised a prompt log but contained no prompt-log artifact before this update. |

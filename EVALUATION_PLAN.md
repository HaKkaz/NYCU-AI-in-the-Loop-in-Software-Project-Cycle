# Draft Evaluation Plan

## Problem Grounding

### 1. Who specifically has the collaboration problem?

The target population is university students working in small software development teams that use GitHub for collaborative projects and need to understand decisions and implementation changes made by other team members. This is particularly relevant when several people contribute to the same repository, project work spans multiple days or weeks, and important decisions are documented separately from implementation history.

The problem is most visible when a student needs to understand work performed by another teammate, joins a project later, or revisits an older part of the project. That student may be able to find the code change, but still need to reconstruct the reasoning and sequence of events that led to it.

### 2. What do they currently do instead of our tool?

Team members currently inspect project information in separate places, including:

- Git commit history
- pull request descriptions
- pull request comments
- `DECISIONS.md`
- team messages when additional context is missing

To understand a project change, a teammate may manually correlate the following sequence:

```text
Decision
↓
Date
↓
Nearby commits
↓
Pull request discussion
↓
Resulting implementation
```

This workflow has several weaknesses:

- Information is spread across different places.
- Relationships between decisions and implementation changes are not immediately visible.
- Reconstructing project history requires repeated navigation and manual comparison.
- A teammate may understand what changed without understanding why it changed.
- Older decisions become harder to rediscover as the repository grows.

This plan describes the current workflow as a problem to evaluate; it does not claim that interviews or user studies have already been conducted.

### 3. What would be observably different about collaboration if our tool worked?

If the dashboard works, team members should be able to:

- reconstruct important project history faster;
- identify what happened before and after a decision;
- understand implementation changes and decision rationale from one chronological interface;
- switch between fewer separate information sources;
- answer questions about previous project decisions with less effort; and
- require fewer clarification questions from the teammate who originally made the change.

These differences are observable through task completion time, answer accuracy, navigation effort, and the number of clarification requests during project-history tasks.

# Evaluation Plan

## Success Definition

We will know our tool works if team members can correctly reconstruct the sequence of important project decisions and related implementation changes faster using the dashboard than by manually navigating Git history and `DECISIONS.md`.

The primary comparison will be between:

- **Baseline:** GitHub commit history, `DECISIONS.md`, and normal repository navigation, with pull requests available if needed.
- **Dashboard:** a unified chronological timeline containing Git commit history and human-authored entries from `DECISIONS.md`.

The evaluation will measure at least the following:

### 1. Task completion time

Measure how long each participant takes to answer project-history questions, such as:

- What decision happened before this commit?
- Why was this project change made?
- What implementation changes happened after this decision?
- What was the sequence of events surrounding this change?

### 2. Answer accuracy

Faster performance will not count as success if participants reach the wrong conclusion. We will measure whether participants correctly identify the relevant decision, implementation change, ordering of events, and documented rationale.

### 3. Navigation effort

We will measure an approximate indicator of navigation effort, such as the number of separate pages or files visited, context switches, and searches or navigation actions required. The exact interaction-count metric may be refined later.

### 4. Clarification requirement

We will observe whether participants still need to ask another teammate for missing context while completing the tasks. A reduction in clarification requests would be useful evidence, but no success claim is made before evaluation.

This success definition evaluates human understanding of project history. It does not require autonomous AI behavior or treat AI output as a substitute for participant judgment.

## Human–AI Boundary

The current proposed MVP does not require AI. The dashboard primarily visualizes existing human-authored project information:

- Git commits, including commit SHA, author, timestamp, and commit message; and
- entries from `DECISIONS.md`, including the decision date, what was decided, why, and optionally rejected alternatives or the person who led the decision.

> The initial prototype does not require AI to make or approve project decisions. Whether AI-assisted summarization, automatic decision extraction, or automatic commit-to-decision linking will be added is TBD — to be determined by CP1.

If AI is introduced later, humans must remain responsible for validating important engineering decisions and any AI-generated interpretation of project history.

## Target Users

The target users are university students with experience working in small GitHub-based software development teams. Preferred participants will have:

- worked on group programming projects;
- used Git or GitHub;
- reviewed code written by teammates; and
- needed to understand project history that they did not personally create.

For the earliest internal dogfooding, our own team members can use the dashboard with this repository. The repository is the first real project and data source, not a user.

For later evaluation, we plan to recruit approximately **5–8 participants**, such as students from computer science or software engineering courses, classmates with GitHub group-project experience, or students participating in side projects or hackathons. These participants are a planned target population, not already-recruited users.

## Method

We will use structured observation, a brief post-task survey, and a short follow-up interview. The evaluation will use a baseline-versus-tool comparison with project-history tasks of comparable difficulty.

### Evaluation Data Source

The team's actual repository, `HaKkaz/NYCU-AI-in-the-Loop-in-Software-Project-Cycle`, will be the first real evaluation project once it contains enough commits and decision-log entries to support meaningful project-history tasks. The repository should naturally accumulate commits, pull requests, and decisions during normal course development.

We will not generate synthetic project history unless real data later proves insufficient. The future dashboard is intended to combine Git history and `DECISIONS.md` into one chronological project timeline. The exact product architecture is not decided in this plan. Future versions may connect decisions with related commits, but that connection is not a required Week 3 capability.

### Baseline Condition

Participants will use the repository normally. They may inspect GitHub commit history, `DECISIONS.md`, and pull requests if needed. Example project-history questions include:

1. What important decision occurred before a specified commit?
2. Why was a certain project-level change made?
3. Which implementation changes happened after a specific decision?
4. What is the chronological sequence of several project events?

For each task, we will record completion time, answer correctness, the number of information sources visited, and whether clarification from another person was required.

### Dashboard Condition

Participants will answer comparable questions while using the project-history dashboard. We will record the same metrics: completion time, answer correctness, navigation effort, and clarification requirement.

Tasks will be comparable in difficulty. We will avoid having participants answer the exact same question twice, because remembering the first answer could bias the comparison between conditions.

### Post-task Survey

After the tasks, participants will answer short questions such as:

- Was it easier to understand the project's history using the dashboard?
- Was it easier to understand why a change happened?
- Did the dashboard reduce the need to switch between Git history and the decision log?
- Was any information missing or confusing?
- Would this dashboard be useful in a real group software project?

We will prefer a small Likert scale with optional written comments.

### Brief Interview

The follow-up interview will ask:

- What information was easiest to find?
- What was still difficult to understand?
- Which part of the normal GitHub workflow caused the most friction?
- Did the chronological timeline make the relationship between decisions and implementation clearer?
- What additional information should appear in the dashboard?

### Evaluation Timing

The evaluation will be conducted after a usable dashboard prototype exists and after the repository has accumulated enough real commits and decision-log entries to support meaningful project-history tasks.

## Minimum Evidence Threshold

The first evaluation will use the following provisional Week 3 threshold. It should include at least **5 participants who complete both baseline and dashboard-assisted tasks**.

Minimum convincing evidence will require:

1. At least **4 out of 5 participants** correctly complete the project-history tasks using the dashboard.
2. The **median task completion time is at least 20% lower** with the dashboard than with the baseline workflow.
3. Accuracy does **not decrease** compared with the baseline.
4. At least **4 out of 5 participants** report that the dashboard makes project history easier to understand or reduces the effort required to find relevant context.
5. Navigation effort shows a consistent reduction compared with manually switching between Git history and `DECISIONS.md`.

These thresholds are provisional Week 3 evaluation criteria and may be refined during CP1. They are not achieved results, and no evaluation outcome is claimed yet.

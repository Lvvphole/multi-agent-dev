# Frozen Plan: PR #3 P1 Review Repair

Run: `2026-08-19-pr3-p1-review-fix-0002`

Status: `REVISION_2_FROZEN_BY_HUMAN_DIRECTIVE`

## Current state

The reviewed checker validates normalized local route bindings but normalizes an absolute filesystem target before rejecting it. The prior evidence run reports PASS without accepted Scout and frozen Plan predecessors.

## Desired state

- Every local Markdown route target is repository-relative before resolution.
- Required bindings are counted only when they are active in rendered Markdown, not hidden in HTML comments or fenced code.
- POSIX and Windows absolute targets are rejected deterministically.
- Existing redirect, swap, outside-repository, canonical-sequence, and invariant mutations remain rejected.
- Historical run `2026-08-19-pr1-p1-review-fix-0001` truthfully reports `BLOCKED` for missing predecessor-stage continuity.
- This replacement run preserves a digest-bound Scout-to-Test trajectory and does not claim independent Codex acceptance before it exists.
- Evidence integrity is executed by a persisted, qualified verifier whose exact command and file digest are recorded.

## Smallest vertical slice

1. Add an absolute-route predicate before path resolution.
2. Add POSIX and Windows absolute-target mutations.
3. Mark the incomplete historical run `BLOCKED` with its reason.
4. Produce the required Build and Test artifacts for this accepted and frozen Plan.
5. Filter non-rendered Markdown regions and add HTML-comment and fenced-code mutations.
6. Persist and qualify a deterministic evidence-manifest verifier, then record its exact invocation and identity.
7. Submit the exact evidence-bound head to Codex and continue only if the review has no major issue.

## Boundaries and exclusions

- No changes to `AGENTS.md`, architecture, runtime topology, dependencies, permissions, schemas, or business objectives.
- No merge, activation, or external side effect other than the authorized branch and PR updates.
- No retroactive claim that the historical run had predecessor inputs.

## Data and evidence contracts

- Route-target classification occurs on the raw fragment-free Markdown target.
- Every Plan, Build, and Test input is bound by SHA-256.
- The tested code commit is recorded separately from the later evidence-binding commit.
- Raw command output preserves timestamps, exit status, and unedited command output.

## Rollback

Revert the PR #3 repair commits. No runtime or persistent business state is changed.

## Human gates

- Scope acceptance is supplied by the maintainer's directive to fix every Codex issue until no major issue remains.
- Codex supplies independent review evidence.
- Only the maintainer may merge.

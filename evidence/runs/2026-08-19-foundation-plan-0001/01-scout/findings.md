# Scout Findings: Objective-to-Verified-Problem Foundation

Run ID: `2026-08-19-foundation-plan-0001`
Status: `ACCEPTED_FOR_PLANNING`
Base commit: `85e577c2e10283a9c0b4c5291eb594e6e504f148`

## Decision

The next implementation should be the smallest business-domain foundation that can reject a false progression:

```text
Stage 0 Objective Definition
  -> Stage 1 Problem Scouting
  -> Stage 2 Problem Validation
  -> VERIFIED_PROBLEM | REJECTED_TO_SCOUTING | BLOCKED
```

This is a contract-first slice. It must establish the common operating record, transition proposals, evidence admission, independent verification, and the canonical commit boundary before any durable agent orchestration is added.

The current change is planning and checker qualification only. It does not implement that runtime slice.

## Current-state evidence

- The approved operating specification makes Stage 0 mandatory, defines Stage 1 output as a candidate problem, and requires all five Stage 2 gates before solution design.
- The specification defines 17 common operating-record fields and forbids internal activity from proving business progression.
- The locked architecture requires one canonical state-transition service, revision vectors, compare-and-set, independent verification, and human authority.
- The repository currently contains one `Developer` SDK agent and one `DevelopmentProposal` contract. It contains no common operating-record contract, canonical state model, state-transition service, persistence configuration, lockfile, or canonical runtime test command.
- The physical owner and repository location of the state-transition service are not fixed by the checked-in architecture. Choosing one silently would change the locked architecture.

## Why this slice is first

1. It starts at the approved objective instead of an available model or product idea.
2. It can falsify the core safety hypothesis: a candidate cannot become a verified problem without every required gate and admitted external evidence.
3. It is the earliest reusable business boundary for every later stage.
4. It keeps the initial blast radius small: pure contracts and transition semantics precede persistence, queues, tools, or autonomous effects.
5. It exposes architecture decisions while they are still cheap to reverse.

## Central implementation hypothesis

> A bounded domain kernel plus a separately authorized canonical writer can represent Stage 0 through Stage 2 and reject missing, stale, self-verified, internally inferred, or incomplete evidence without granting an SDK agent authority.

The future implementation is disproven if any seeded invalid transition commits, if any actor other than the state-transition service can commit canonical state, or if the checker cannot detect its required negative controls.

## Constraints

- `AGENTS.md` is authoritative.
- The approved business specification and locked architecture may not be silently changed.
- `MODEL != AUTHORITY`, `STATE ACCESS != AUTHORITY`, and `TOOL RESULT != VERIFIED EFFECT` remain hard constraints.
- The software delivery pipeline cannot claim verified client value or retained revenue.
- Production implementation is forbidden in this planning run.
- Build promotion is blocked until every blocking decision in the input manifest is resolved and the plan is independently verified and accepted by Lvvphole.

## Risks and unknowns

- The locked architecture names the state-transition service semantically but does not select its physical package, owner, or persistence boundary.
- The repository has no canonical install or test environment for future runtime code.
- `S_C`, `S_D`, gap comparison, consequence thresholds, reachability, and solvability require domain-specific measurement contracts that are not yet approved.
- Checker qualification proves structural sensitivity only. It does not prove business validity, production correctness, or economic outcomes.

## Scout exit condition

The user explicitly requested a tested plan for the previously recommended next path. These findings are therefore accepted as Plan-stage input, but they do not authorize Build, architecture changes, external effects, or merge.

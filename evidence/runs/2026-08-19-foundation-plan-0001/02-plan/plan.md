# Candidate Plan: Objective-to-Verified-Problem Foundation

Run ID: `2026-08-19-foundation-plan-0001`
Base commit: `85e577c2e10283a9c0b4c5291eb594e6e504f148`
Plan status: `CANDIDATE`
Implementation gate: `BLOCKED`
Acceptance authority: `Lvvphole`

## Single next best path

Implement the smallest contract-first business slice that can prevent a false problem from becoming a solution mandate:

```text
Stage 0 Objective Definition
  -> Stage 1 Problem Scouting
  -> Stage 2 Problem Validation
  -> VERIFIED_PROBLEM | REJECTED_TO_SCOUTING | BLOCKED
```

Do this before durable agents, queues, autonomous tool selection, or external effects.

The first action after this plan is accepted is an architecture-decision change, not runtime code: Lvvphole must approve the physical owner, package boundary, persistence boundary, and interface of the sole state-transition service. The data contracts and executable transition slice follow only after that ADR is merged.

No production implementation is permitted in this planning run.

## Why this is the first slice

- It begins with the approved business objective and definition of done.
- It enforces the invariant that a problem must be real, unsatisfied, consequential, reachable, and solvable before solution design.
- It establishes the common record, evidence, authority, verification, and state boundaries reused by all later business stages.
- It has a decisive negative test: omit or disprove any required gate and canonical progression must not occur.
- It is small enough to review and reverse before persistence, concurrency, and autonomous behavior multiply the failure surface.

This is an evolutionary-architecture slice: protect named characteristics with separate fitness functions and change one bounded dimension at a time. The fitness functions are not combined into a score that can trade away a hard constraint.

## User and experience

The primary user is the repository maintainer and human accountable for merge, Lvvphole.

For each candidate change, the maintainer should receive one inspectable decision packet:

1. the business objective and bounded change;
2. requirement-to-source-to-check traceability;
3. exact PASS, FAIL, and BLOCKED results with raw evidence;
4. mutations used to qualify each critical checker;
5. residual uncertainty and unresolved human decisions; and
6. one software-delivery recommendation: `MERGE_READY`, `DO_NOT_MERGE`, or `BLOCKED`.

There is no opaque confidence score. Hard constraints cannot be offset by passing unrelated tests. A drill-down from every recommendation must reach the requirement, source, checker, input digest, raw result, and verifier identity.

## Current state

- The approved organizational objective, operating loop, common record semantics, locked architecture, authority rules, and implementation-stage routes are merged.
- The repository has a proposal-producing Developer SDK agent and a four-field DevelopmentProposal contract.
- The repository has no canonical operating-record schema, transition proposal schema, state-transition service, canonical persistence configuration, dependency lockfile, or runtime qualification command.
- The checked-in architecture names a sole state-transition service but does not choose its physical package or persistence boundary.
- The initial client domain and its measurement, evidence-admission, and risk policy are not approved.

## Desired state for this foundation

A deterministic, model-independent foundation can:

- represent all 17 common operating-record fields without changing their semantics;
- keep business stages, software-delivery stages, verification verdicts, and value-cycle states separate;
- require the complete Stage 0 objective contract;
- represent a Stage 1 candidate problem without prematurely representing it as a solution;
- require all five Stage 2 validation gates under an approved domain policy;
- accept externally attributable, fresh, state-relative evidence and reject proxy-only claims;
- keep transition proposals separate from canonical commits;
- permit only an authorized state-transition service to commit with revision-vector compare-and-set;
- require a verifier independent from the producer; and
- fail closed without invoking a model, queue, or external-effect capability.

## Objective and hard constraints

The foundation objective is to maximize admissible, explainable progression from a complete objective to a verified problem while preventing false progression.

The following are hard, non-compensating constraints:

- zero accepted seeded invalid transitions;
- zero canonical write paths outside the state-transition service;
- zero stale-revision commits in qualification fixtures;
- zero self-verified consequential transitions;
- 100% source binding for in-scope requirements;
- 100% requirement coverage by an objective fitness function or explicit manual gate; and
- `BLOCKED != PASS` in every result namespace.

Runtime latency, throughput, cost, and retry budgets are not guessed. They must be approved in `DEC-PTRR-005` before Build.

## Scope

### In scope for the future foundation implementation

- logical contracts for the common operating record, Stage 0 objective, Stage 1 candidate problem, Stage 2 validation, evidence, transition proposal, verification decision, revision vector, and commit receipt;
- pure deterministic validation and transition rules for stages 0 through 2;
- a separately authorized sole-writer boundary with compare-and-set and idempotency semantics;
- independent verifier identity and qualification checks;
- atomic fitness functions followed by one bounded end-to-end simulation;
- ICM stage artifacts and reproducible run evidence; and
- maintainer-facing decision evidence.

### Out of scope

- Stage 3 Gap Diagnosis or any later business stage;
- product, offer, distribution, demand, sales, revenue, implementation, value-realization, retention, or expansion behavior;
- durable agent topology or dynamic-principal creation;
- queues, scheduling, leasing, retry implementation, or autonomous loop control;
- model or prompt selection;
- external-effect capabilities;
- UI, analytics dashboards, and economic optimization; and
- any claim of realized client value or retained revenue.

## Logical contracts

Physical filenames and language bindings remain blocked by `DEC-PTRR-001` and `DEC-PTRR-002`. The ADR must map these logical contracts into the locked repository without weakening them.

| Logical contract | Minimum responsibility |
| --- | --- |
| `CommonOperatingRecord` | Preserve the 17 approved semantic fields and their evidence references. |
| `ObjectiveDefinition` | Goal, current state, desired state, definition of done, objective function, constraints, owner, and approval state. |
| `CandidateProblem` | Entity, context, observed condition, consequence hypothesis, ability-to-act hypothesis, and evidence references; no solution qualification. |
| `ProblemValidation` | Separate Real, Unsatisfied, Consequential, Reachable, and Solvable decisions under a versioned domain policy. |
| `EvidenceRecord` | Source, provenance, epistemic label, observed time, applicable revision, scope, integrity identity, and admission state. |
| `TransitionProposal` | Producer, from-state, proposed to-state or return route, predicate results, evidence identities, expected revision vector, idempotency key, and creation time. |
| `VerificationDecision` | Independent verifier identity, qualification identity, per-predicate verdicts, overall `PASS | FAIL | BLOCKED`, evidence identities, and time. |
| `CanonicalCommitReceipt` | State-service identity, accepted proposal and verification identities, before/after revisions and digests, idempotency result, and commit time. |

State, memory, and authority remain separate types and dependencies. An evidence or memory record can inform a proposal; it cannot authorize or commit one.

## Transition rules

| From | Required external predicate | Proposed result | Disproven predicate | Missing or inadmissible evidence |
| --- | --- | --- | --- | --- |
| Stage 0 incomplete | All six objective fields resolved and approved | Stage 0 complete, Stage 1 eligible | `FAIL` if a stated predicate is false | `BLOCKED`, no mutation |
| Stage 0 complete | Attributable candidate problem observed | Stage 1 candidate recorded, Stage 2 eligible | Return learning without validation | `BLOCKED`, no mutation |
| Stage 1 candidate | All five validation gates true | `VERIFIED_PROBLEM` | `REJECTED_TO_SCOUTING` with evidence and learning | `BLOCKED`, no mutation |

The foundation exposes no edge to Stage 3. A later accepted plan must add that edge with its own requirements and fitness functions.

Every canonical transition follows:

```text
producer proposal
  -> evidence admission
  -> independent verification
  -> Action Gate and capability runtime
  -> state-transition service
  -> revision-vector compare-and-set
  -> canonical commit receipt
```

Internal activity, model text, a tool result, or a passing producer-local test cannot skip a step.

## Change sequence

Each change is a separate bounded pull request unless the maintainer explicitly freezes a different scope.

### Change 0: Resolve the architecture boundary

Entry:

- this candidate plan is structurally qualified;
- Lvvphole agrees that Stage 0 through Stage 2 is the next slice.

Outputs:

- ADR naming the state-transition service package and accountable owner;
- persistence, transaction, compare-and-set, idempotency, and rollback boundary;
- public proposal and private commit interfaces;
- initial domain measurement and evidence-admission decision or an explicit separate decision record;
- canonical install and narrow test commands with a lockfile if a dependency is introduced.

Checks:

- architecture invariant review;
- repository-path and dependency review;
- no direct agent, verifier, memory, or adapter write path;
- human decision record.

Exit:

- ADR merged by Lvvphole and blocking decisions updated to resolved.

Blockers:

- `DEC-PTRR-001`, `DEC-PTRR-002`, `DEC-PTRR-003`, and `DEC-PTRR-005`.

### Change 1: Add pure contracts

Entry:

- Change 0 merged;
- physical ownership and language are fixed;
- domain units and thresholds are versioned.

Outputs:

- the eight logical contracts;
- separate result namespaces;
- stable field and enum serialization;
- no persistence or model dependency.

Checks:

- `FF-PTRR-001`, `FF-PTRR-002`, `FF-PTRR-004`, `FF-PTRR-006`, `FF-PTRR-011`, and `FF-PTRR-013`;
- known-good schema fixtures;
- every declared field, enum, unit, and cross-assignment negative control.

Exit:

- all atomic schema checks pass with a qualified checker and independent review.

Blockers:

- missing lockfile or canonical command;
- unapproved schema semantics;
- any accepted negative control.

### Change 2: Add the pure transition kernel

Entry:

- Change 1 merged;
- evidence-admission policy is approved.

Outputs:

- deterministic Stage 0, Stage 1, and Stage 2 proposal validators;
- explicit rejection-to-scouting and blocking results;
- no persistence, queue, model, or external effect.

Checks:

- `FF-PTRR-003`, `FF-PTRR-005`, `FF-PTRR-006`, `FF-PTRR-007`, `FF-PTRR-012`, and `FF-PTRR-014`;
- six Stage 0 omissions;
- solution-first Stage 1 negative;
- ten single-gate Stage 2 mutations;
- proxy, stale, missing-provenance, and self-verification negatives.

Exit:

- the kernel accepts its known-good cases and rejects every declared invalid progression.

Blockers:

- ambiguous gate outcomes;
- domain policy not executable;
- checker unqualified.

### Change 3: Add the canonical commit adapter

Entry:

- Change 2 merged;
- state owner, persistence, authority, and resource policies approved.

Outputs:

- sole-writer state-transition adapter;
- Action Gate and capability-runtime entry path;
- revision-vector compare-and-set;
- idempotent commit receipt;
- no autonomous agent orchestration.

Checks:

- `FF-PTRR-008`, `FF-PTRR-009`, `FF-PTRR-010`, `FF-PTRR-015`, and `FF-PTRR-019`;
- direct-write dependency mutations;
- current, stale, conflicting, and replayed revision fixtures;
- missing, expired, wrong-principal, and overbroad authority fixtures.

Exit:

- only the authorized service can commit and at most one conflicting proposal wins.

Blockers:

- unclear transaction guarantees;
- no rollback or recovery path;
- any authority or stale-write negative accepted.

### Change 4: Qualify the full foundation

Entry:

- Changes 1 through 3 merged;
- independent Test and Review principals identified and qualified.

Outputs:

- end-to-end deterministic simulation;
- complete requirement coverage report;
- raw execution evidence and digests;
- maintainer decision packet.

Checks:

- all atomic functions in declared order;
- `FF-PTRR-014` and `FF-PTRR-021` only after atomic PASS;
- checker qualification against independent known-good and every declared negative;
- evidence-manifest integrity;
- regression run of the repository's canonical full gate.

Exit:

- independent Review returns `MERGE_READY`, `DO_NOT_MERGE`, or `BLOCKED` with admissible evidence;
- only Lvvphole may merge.

Blockers:

- any FAIL or BLOCKED prerequisite;
- missing raw evidence;
- producer-only verification;
- human merge decision absent.

## Testing strategy

### Plan qualification in this run

The plan checker must prove structural sensitivity with an independent fixture:

- accept one known-good Plan artifact set;
- reject missing source binding;
- reject uncovered requirement;
- reject a critical fitness function without negative controls;
- reject a missing common operating-record field;
- reject a missing Stage 2 validation gate;
- reject an unblocked implementation while decisions remain unresolved;
- reject production implementation scope; and
- reject missing manual human gates.

Passing these checks establishes only that the plan artifact set is structurally complete according to the encoded rules. It does not independently accept the plan or validate future runtime behavior.

### Future implementation qualification

Run atomic schema, transition, evidence, authority, writer, and concurrency fitness functions before the holistic Stage 0-to-verified-problem simulation. A critical checker that accepts any required negative is `UNQUALIFIED`; every dependent claim is then `BLOCKED`.

## Evidence contract

For every executed command preserve:

- repository commit or tree identity;
- exact command and working directory;
- Python/runtime and dependency versions;
- input and configuration digests;
- start and end UTC timestamps;
- exit status;
- unedited stdout and stderr;
- produced-artifact digests; and
- checker identity, digest, and qualification state.

The plan producer may run candidate checks but cannot independently accept the plan. The Test and Review roles remain separate from Build for consequential promotion.

## Rollback and recovery

- This planning change is documentation, checker, tests, and evidence only. Close the pull request or revert its commit to remove it; it has no runtime side effect.
- Contract and pure-kernel changes remain reversible by reverting their individual pull requests before persistence activation.
- The state adapter cannot be activated until Change 3 defines rollback, replay, conflict, and recovery behavior and those paths are tested.
- Never repair a failed check by weakening the approved specification, threshold, negative control, or locked invariant.

## Blocking decisions

| Decision | Required before | Current state |
| --- | --- | --- |
| `DEC-PTRR-001` state-service package, owner, and interface | Change 1 | `UNRESOLVED` |
| `DEC-PTRR-002` persistence and transaction boundary | Change 1 | `UNRESOLVED` |
| `DEC-PTRR-003` initial domain measurement and evidence policy | Change 1 | `UNRESOLVED` |
| `DEC-PTRR-004` independent verifier identity and qualification | Change 4 promotion | `UNRESOLVED` |
| `DEC-PTRR-005` attempt, time, cost, throughput, and latency budgets | Change 1 | `UNRESOLVED` |
| `MG-PTRR-004` human Plan acceptance and scope freeze | Build | `OPEN` |

These are true blockers. They are not assumptions and cannot be filled by an agent.

## Definition of done

### This planning run

Done requires:

- all four Plan-stage outputs and both Scout outputs exist and parse;
- every requirement has a stable ID, source binding, objective predicate, evidence contract, verifier, and failure state;
- every requirement maps to at least one fitness function or manual gate;
- the plan checker accepts the actual plan artifact set;
- its qualification suite accepts the independent known-good and rejects every required negative;
- raw command evidence and digests are preserved;
- a planning-only pull request exposes the candidate to independent review; and
- Build remains `BLOCKED` pending the recorded decisions and human gate.

### The future foundation implementation

Done requires all four bounded implementation changes, every applicable fitness function, qualified independent Test and Review evidence, no accepted negative control, a maintainer decision packet, and Lvvphole's merge decision. Even then, the result is a verified software intervention artifact, not realized client value or retained revenue.

## Promotion rule

The automated plan checker may return PASS for structural conformance. That does not authorize Build.

Promotion requires all of the following:

```text
structural plan check PASS
AND checker qualification PASS
AND independent plan verification PASS
AND DEC-PTRR-001..005 resolved at their required gates
AND MG-PTRR-001..004 satisfied
AND Lvvphole accepts and freezes the plan
```

Until then:

```text
PLAN = CANDIDATE
IMPLEMENTATION = BLOCKED
MERGE = HUMAN DECISION
```

# Locked Architecture

This file is the routed design reference. `AGENTS.md` remains the authoritative repository contract.

## System objective

Build a governed multi-agent software factory that turns a human-authorized task into a tested, independently reviewed change without allowing a model, tool, memory record, or organizational title to become authority.

## Governance order

```text
human / constitutional authority
  -> enterprise governance state
  -> existing governance kernel
  -> enterprise control
  -> bounded runtime enforcement
```

Enterprise governance state is governed configuration. Runtime enforcement remains outside the model.

## Runtime boundary

Out of sandbox:

- human approval and enterprise governance state;
- orchestrator and queue admission;
- principal registry and lifecycle;
- Action Gate and capability runtime;
- canonical enterprise state and state-transition service;
- A2A delivery, resource governance, evidence, and verification.

Inside each sandbox:

- one active principal and its SDK Agent;
- scoped task, state, memory, capability, budget, and lease projections;
- model reasoning and non-privileged local work;
- runtime-aware adapters that request governed external action.

The sandbox cannot authorize itself, activate its principal, mutate canonical state, or bypass the capability runtime.

## Software-factory trajectory

```text
Scout -> Plan -> Build -> Test -> Review -> human merge
```

Each named actor is a distinct principal. Handoffs use immutable artifacts and governed A2A envelopes. Test and Review remain independent of Build for consequential acceptance.

## Privileged action trajectory

```text
model request
  -> runtime-aware tool adapter
  -> Action Gate
  -> capabilityRuntime.invoke(...)
  -> registry
  -> resolve
  -> preconditions
  -> PRE-DISPATCH hooks
  -> dispatch
  -> POST-DISPATCH hooks
  -> evidence
  -> independent verification
  -> state-transition service
  -> compare-and-set
  -> canonical commit
```

`dispatch()` is internal. No model, actor, adapter, orchestrator, verifier, memory component, or domain owner may call it as a public entry point.

## Trusted boundaries

- Governance-kernel modules are sibling trusted-computing-base modules invoked at their applicable control points. They are not a processing chain.
- `registry -> resolve -> preconditions` is the sequential capability-admission path.
- PRE-DISPATCH and POST-DISPATCH hooks remain distinct.
- Observation labeling occurs after dispatch and before evidence-dependent acceptance.
- The verification harness returns `PASS | FAIL | BLOCKED`; `BLOCKED` is never acceptance.
- The state-transition service is the sole canonical writer.

## State and memory

Canonical enterprise state uses distributed ownership without distributed truth. Actors receive immutable, information-rights-filtered projections with per-domain revisions and `VERIFIED | OBSERVED | INFERRED` epistemic labels.

Memory is separate from state and authority. Retrieval passes lineage, admission, freshness, and role/goal projection before entering agent context. A child never inherits full parent memory or mutable conversation state.

## Dynamic principals and A2A

A dynamic principal follows:

```text
REQUESTED -> ADMITTED -> CREATED -> VERIFIED -> ACTIVE -> SUSPENDED | TERMINATED
```

Only an `ACTIVE` principal can claim work. Creation uses the normal proposal, authorization, execution, evidence, verification, and versioned activation path. Delegation depth, budget, information exposure, queue capacity, ownership lease, and stop conditions are mandatory.

## Repository architecture

```text
AGENTS.md                 root contract and context router
ARCHITECTURE.md           routed system design
authority/                scoped security, safety, memory, verification rules
governance/               executable governance rules and coverage
enterprise/               governed enterprise configuration
contracts/                schemas for all boundary artifacts
packages/                 orchestration, control, runtime, state, memory, verification
capabilities/             registered capabilities, tools, and hooks
agents/durable/           Scout, Plan, Build, Test, Review, corporate, assurance
workflows/                ICM development-stage contracts and promotion gates
evidence/                 prompts, snapshots, and run evidence
docs/                     ADRs, specifications, and runbooks
tests/                    fitness, qualification, integration, behavioral, and E2E tests
```

ICM structures the repository-development workflow and its context artifacts. It does not replace isolated principals, runtime A2A, queues, leases, canonical state, or capability enforcement.

## Change rule

Runtime evidence may invalidate an assumption and trigger a controlled architecture proposal. No agent may silently revise this design. Architecture changes require an ADR, affected fitness-function updates, independent verification, and human merge approval.

Decision rationale: [ADR-0001 - Authoritative AGENTS.md with ICM context routing](docs/adr/0001-authoritative-agents-and-icm-routing.md).

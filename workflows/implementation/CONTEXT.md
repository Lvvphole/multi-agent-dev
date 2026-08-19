# Implementation Workflow Context

Layer: 1 - workflow router.
Authority: subordinate to root `AGENTS.md`.
Use: repository changes executed through Scout, Plan, Build, Test, and Review.

## Context rule

Read root `AGENTS.md`, this router, the selected stage contract, and only the inputs named by that contract. Stable rules are Layer 3 references. Task-specific materials and stage outputs are Layer 4 working artifacts.

ICM supplies transparent, sequential context and human edit surfaces for this development workflow. It does not replace runtime principal isolation, A2A authorization, queueing, canonical state, or capability enforcement.

## Stage routes

| Order | Principal | Single job | Contract |
| --- | --- | --- | --- |
| 01 | Scout | Establish evidence-backed current state and uncertainty | [01-scout/CONTEXT.md](01-scout/CONTEXT.md) |
| 02 | Plan | Bind requirements, data, fitness functions, and the smallest implementation slice | [02-plan/CONTEXT.md](02-plan/CONTEXT.md) |
| 03 | Build | Implement only the accepted slice | [03-build/CONTEXT.md](03-build/CONTEXT.md) |
| 04 | Test | Independently execute and preserve verification evidence | [04-test/CONTEXT.md](04-test/CONTEXT.md) |
| 05 | Review | Adjudicate compliance and promotion readiness | [05-review/CONTEXT.md](05-review/CONTEXT.md) |

## Handoff contract

Each stage reads an accepted predecessor artifact and writes a complete, human-readable intermediate artifact to `evidence/runs/<run-id>/<stage>/`. Every handoff identifies the task, source commit, input digests, output digests, unresolved uncertainty, and human promotion decision.

No stage silently changes an earlier artifact. Correct the source artifact, record a new revision, and rerun only the dependent stages. No stage promotes itself.

## Promotion order

```text
Scout -> human gate -> Plan -> human gate -> Build -> Test -> Review -> human merge
```

If a gate rejects or changes an artifact, downstream artifacts are stale until their declared inputs are revalidated.

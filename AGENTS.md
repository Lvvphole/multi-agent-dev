# AGENTS.md

Status: authoritative repository contract and context router.
Scope: the entire repository.

## Authority and precedence

- Human and platform authority remain above repository instructions.
- Within repository-controlled instructions, this root file is authoritative.
- Referenced context files specialize this contract but MUST NOT weaken or contradict it.
- Do not add nested `AGENTS.md` or `AGENTS.override.md` files. They would create implicit precedence that can override this root contract.
- If applicable instructions conflict or a required route is missing, stop with `BLOCKED` and identify the conflict. Do not guess.
- This file governs coding-agent conduct. It does not grant runtime organizational authority.

## Mission

Implement the locked multi-agent software factory and enterprise control architecture through small, evidence-bearing changes.

The durable software-factory actors are Scout, Plan, Build, Test, and Review. Each actor is an isolated computational principal with its own sandbox, runtime identity, scoped context, authority, budget, and evidence trajectory.

## Canonical commands

- Validate this instruction system: `python3 scripts/verify_instruction_routes.py`
- Qualify the instruction checker: `python3 -m unittest discover -s tests/instructions -p 'test_*.py'`
- No canonical install, lint, typecheck, unit-test, integration-test, or run command exists yet. Do not invent one. Add each command with its implementation and lockfile.
- Prefer the narrowest applicable check. Run the full required gate before claiming completion.

## Non-negotiable invariants

- `MODEL != PRINCIPAL`
- `MODEL != AUTHORITY`
- `SDK AGENT != ACTOR CONTRACT`
- `TOOL AVAILABILITY != PERMISSION`
- `MEMORY != AUTHORITY`
- `STATE ACCESS != AUTHORITY`
- `TOOL RESULT != VERIFIED EFFECT`
- `CREATED PRINCIPAL != ACTIVE PRINCIPAL`
- The Authority Envelope is the sole runtime source of organizational authority.
- A delegated grant can narrow authority; it cannot increase it.
- Privileged execution enters only through the Action Gate and `capabilityRuntime.invoke(...)`.
- The internal execution order is `registry -> resolve -> preconditions -> PRE-DISPATCH hooks -> dispatch -> POST-DISPATCH hooks -> evidence -> verification`.
- Only the state-transition service may commit canonical enterprise state, using required revision vectors and compare-and-set.
- A producer cannot be the sole verifier of its consequential result.
- `BLOCKED != PASS`. Missing evidence, stale state, unresolved authority, or an unqualified checker fails closed.
- Every asynchronous queue is bounded and implements admission control and backpressure.
- Every retry loop has attempt, cost, and elapsed-time budgets, a progress test, idempotency semantics, and a stop condition.
- Cross-sandbox work uses authenticated A2A envelopes, scoped projections, leases, deduplication, and receiver admission.
- Governance, authority, acceptance, verification, memory-policy, sandbox, and capability-runtime changes require a pull request, independent verification, and human merge approval.

## Context-loading protocol

Use the ICM separation of context without replacing the runtime orchestration architecture:

- Layer 0: this file - identity, invariants, and authority.
- Layer 1: a routed workflow or subsystem context - where to work.
- Layer 2: the selected stage contract - inputs, process, outputs, verification, and promotion.
- Layer 3: stable references - architecture, authority, specifications, schemas, and ADRs.
- Layer 4: run-specific artifacts - task inputs, intermediate outputs, evidence, and results.

Load Layers 0-2 for the selected task, then only the Layer 3 and Layer 4 files explicitly listed by that route. Do not load the repository indiscriminately. Keep stable rules separate from mutable run artifacts.

## Context routes

| Trigger | Required route |
| --- | --- |
| Architecture, boundaries, topology, data ownership, control flow, or runtime design | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Identity, authority, capabilities, A2A trust, secrets, or external effects | [authority/SECURITY.md](authority/SECURITY.md) |
| Destructive action, safety constraint, approval, reversibility, or escalation | [authority/SAFETY.md](authority/SAFETY.md) |
| Context, retrieval, durable memory, provenance, freshness, or inheritance | [authority/MEMORY.md](authority/MEMORY.md) |
| Tests, checkers, evidence, acceptance, completion, or release claims | [authority/VERIFICATION.md](authority/VERIFICATION.md) |
| Scout, Plan, Build, Test, Review, sprint execution, or stage promotion | [workflows/implementation/CONTEXT.md](workflows/implementation/CONTEXT.md) |

When several triggers apply, load every applicable route. A route selects context; it does not grant permission.

## Change discipline

- Preserve user changes and keep the diff limited to the accepted task contract.
- Do not silently change architecture, acceptance criteria, test thresholds, or governance to make a check pass.
- Write requirements as testable predicates with stable identifiers and source bindings.
- Pair every architectural characteristic with an objective fitness function or an explicit manual gate.
- Record commands actually executed, tool versions, input digests, exit status, and raw results. Narrative claims are not execution evidence.
- Qualify critical checkers with known-good and known-bad fixtures or mutation tests before trusting their verdicts.
- Do not claim implemented, tested, verified, accepted, or complete unless the applicable evidence exists and the required verifier produced that state.

## Completion contract

Report exactly:

1. changed artifacts;
2. requirements satisfied;
3. commands actually executed and exit status;
4. evidence locations;
5. remaining `FAIL`, `BLOCKED`, uncertainty, or human decisions.

Only a human may merge or activate a controlled structural change.

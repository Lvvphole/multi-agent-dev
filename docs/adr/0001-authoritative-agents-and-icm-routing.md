# ADR-0001: Authoritative AGENTS.md with ICM Context Routing

- Status: Proposed
- Date: 2026-08-19

## Context

The repository needs one authoritative coding-agent contract while keeping task context small, explicit, inspectable, and compatible with the locked multi-agent runtime architecture.

Codex automatically composes instruction files from the repository root toward the working directory, with closer files taking precedence. Uncontrolled nested instruction files could therefore weaken a root invariant. A single monolithic root file would preserve precedence but would mix stable rules, subsystem detail, stage procedure, and run-specific artifacts.

ICM supplies a five-layer filesystem method for identity, routing, stage contracts, stable references, and working artifacts. Its native orchestration model is sequential and human-reviewed. The production architecture also requires isolated principals, concurrent A2A delivery, queueing, leases, runtime authorization, and canonical state, which ICM does not provide.

## Alternatives considered

1. Nested `AGENTS.md` files for every subsystem. This provides automatic directory scoping but creates implicit override precedence over the root contract.
2. One comprehensive root `AGENTS.md`. This preserves a single authority source but increases context size and duplicates detailed procedures.
3. One root `AGENTS.md` plus explicitly routed subordinate `CONTEXT.md` and authority documents. This preserves root authority while providing scoped context.

## Decision

Use alternative 3.

- Root `AGENTS.md` is the only repository-discovered instruction file.
- Root `AGENTS.md` contains the repository contract, locked invariants, exact canonical commands, and trigger-to-file routes.
- Subordinate files use standard Markdown and cannot override the root contract.
- `CONTEXT.md` files implement ICM Layer 1 workflow routing and Layer 2 stage contracts.
- Architecture and authority files are Layer 3 stable references.
- `evidence/runs/<run-id>/` contains Layer 4 working artifacts.
- ICM governs the repository-development workflow only. Runtime orchestration retains isolated principals, A2A authorization, bounded queues, leases, capability enforcement, evidence, verification, and canonical state control.

## Consequences

Positive:

- Root invariants have one repository-controlled authority source.
- Context selection is explicit, reviewable, and token-bounded.
- Stage inputs, outputs, verification, and human promotion points are inspectable files.
- Context and stage changes are diffable and reversible in Git.

Trade-offs:

- Routed `CONTEXT.md` files are not automatically discovered; the root contract must direct the agent to load them.
- Directory-specific instructions cannot silently specialize the root contract.
- New routes and stages must satisfy the instruction-routing fitness function.

## Affected quality attributes

- Improves authority consistency, inspectability, auditability, portability, context economy, and change isolation.
- Reduces implicit directory-based customization and automated branching flexibility.

## Verification

- `python3 scripts/verify_instruction_routes.py`
- `python3 -m unittest discover -s tests/instructions -p 'test_*.py'`

The checker verifies the single-root rule, root size, required invariants, route existence, stage order, and stage-contract structure. Its qualification suite proves rejection of nested instruction files, broken routes, changed stage order, missing stage sections, and missing root invariants.

## Sources

- [Official Codex AGENTS.md discovery behavior](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [AGENTS.md best-practices guide used for structure and command specificity](https://gist.github.com/0xfauzi/7c8f65572930a21efa62623557d83f6e)
- [Interpretable Context Methodology, arXiv:2603.16021v2](https://arxiv.org/abs/2603.16021)

Official Codex documentation controls discovery semantics. The best-practices guide is advisory. ICM supplies the context-layer and stage-contract method within the limits recorded above.

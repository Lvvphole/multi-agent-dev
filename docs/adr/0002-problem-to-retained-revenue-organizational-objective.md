# ADR-0002: Problem-to-Retained-Revenue Organizational Objective

- Status: Approved
- Date: 2026-08-19
- Decision authority: Lvvphole

## Context

The architecture previously described the software factory as the system objective. That framing made a delivery capability appear to be the purpose of the organization. The authorized business model instead defines the organization as a continuous problem-discovery, state-change, value-delivery, economic-capture, and learning system.

The operating model originally contained four structural ambiguities: it called stages `0` through `11` eleven stages; its short loop omitted Demand Generation; it said every cycle begins at Stage 0 while routing Stage 11 directly to Stage 1; and it did not distinguish an intentionally closed relationship from retained-revenue success.

## Alternatives considered

1. Retain the software factory as the system objective. Rejected because a merge is an intervention artifact, not client value or retained revenue.
2. Use revenue as the single terminal objective. Rejected because new revenue establishes expected value, not realized client value or continued economic viability.
3. Adopt the closed-loop Problem-to-Retained-Revenue model with separate client and business objectives, externally evidenced stage transitions, and the software factory as a subordinate module.

## Decision

Use alternative 3.

- The organizational goal is to repeatedly create, deliver, verify, and retain economically sustainable client value.
- The required paired outputs are realized client value and sustainable retained revenue.
- The system has 12 stages numbered `0` through `11`.
- The sequence includes `Distribution -> Demand Generation -> Behavioral Progression`.
- The return path is `Stage 11 -> Stage 0 -> Stage 1`.
- `CLOSED_SUCCESS` and `CLOSED_EXIT` are distinct terminal states.
- The Scout, Plan, Build, Test, and Review pipeline remains a subordinate software-delivery capability.
- A merge candidate does not establish client value, retention, or expansion.

## Consequences

Positive:

- Organizational work shares one client-value state model across departments.
- Revenue, implementation, usage, behavior, outcome, and retention remain distinct states.
- Each stage advances on externally evidenced exit conditions rather than internal activity.
- Software delivery can be evaluated rigorously without optimizing the whole organization around code production.

Trade-offs:

- The organization must preserve longer-lived client and economic state across multiple departments and time horizons.
- Value realization and retention require post-implementation observation that cannot be reduced to a repository test.
- Additional business-stage contracts, evidence qualifiers, and domain measures must be designed before runtime implementation.

## Affected quality attributes

- Improves goal alignment, modularity, traceability, outcome validity, economic sustainability, and organizational learning.
- Increases state-model breadth, cross-department coordination, measurement latency, and evidence requirements.

## Verification

- `python3 scripts/verify_instruction_routes.py`
- `python3 -m unittest discover -s tests/instructions -p 'test_*.py'`

The checker verifies the authoritative route, 12-stage declaration, Demand Generation adjacency, normalized return path, distinct success and exit semantics, and software-delivery boundary.

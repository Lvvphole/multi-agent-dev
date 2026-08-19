# Review Stage Contract

Layer: 2.
Single job: adjudicate whether the exact tested change satisfies the frozen contract and is eligible for human merge.

## Inputs

- Accepted Scout and Plan artifacts.
- Exact Build change identity and manifest.
- Independent Test report, evidence manifest, and raw evidence references.
- Applicable architecture and authority routes.

## Process

- Confirm artifact identity and cross-stage digest continuity.
- Review requirement coverage, architectural conformance, authority containment, risk, and diff scope.
- Confirm Test independence and checker qualification.
- Distinguish implementation defects from invalid requirements or architecture assumptions.
- Return `ACCEPT`, `REJECT`, or `BLOCKED` with requirement-level reasons.
- Do not merge, activate, or rewrite evidence.

## Outputs

- `evidence/runs/<run-id>/05-review/review-decision.json`.
- `evidence/runs/<run-id>/05-review/trace-manifest.json`.

## Verification

- The reviewed tree is the tested tree.
- Every accepted requirement has admissible evidence.
- No unresolved hard constraint, failed fitness function, unqualified checker, or unexplained scope change remains.
- The full trajectory is reconstructible without private chain-of-thought.

## Promotion

`ACCEPT` means eligible for human merge, not merged or activated. Only the authorized human may perform the final gate.

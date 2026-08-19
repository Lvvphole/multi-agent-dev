# Plan Stage Contract

Layer: 2.
Single job: turn accepted Scout evidence into an executable, bounded change contract.

## Inputs

- Accepted Scout findings and source manifest.
- Applicable architecture and authority routes.
- Human objective, constraints, and acceptance decisions.

## Process

- Define stable requirement IDs and source bindings.
- Specify current state, desired state, data contracts, boundaries, and affected architecture characteristics.
- Define objective atomic fitness functions first and selective holistic functions where interactions matter.
- Define checker qualification, evidence, rollback or compensation, and human gates.
- Select the smallest vertical slice that can falsify the central implementation hypothesis.
- Do not write production implementation.

## Outputs

- `evidence/runs/<run-id>/02-plan/plan.md`.
- `evidence/runs/<run-id>/02-plan/requirements.json`.
- `evidence/runs/<run-id>/02-plan/fitness-functions.json`.
- `evidence/runs/<run-id>/02-plan/input-manifest.json`.

## Verification

- Every in-scope requirement has an objective acceptance predicate and evidence contract.
- Every mandatory architecture characteristic maps to a fitness function or explicit manual gate.
- Required negative controls are defined for critical checkers.
- Scope, exclusions, dependencies, and unresolved human decisions are explicit.

## Promotion

Human acceptance freezes the implementation scope and acceptance criteria for Build and Test.

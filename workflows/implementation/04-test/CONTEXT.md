# Test Stage Contract

Layer: 2.
Single job: independently execute the accepted verification contract and preserve admissible evidence.

## Inputs

- Frozen Plan requirements and fitness-function registry.
- Build change identity and manifest.
- Applicable verification authority and checker-qualification fixtures.

## Process

- Confirm the exact source identity under test.
- Execute the specified static, lint, type, schema, security, unit, integration, behavioral, and architectural checks that apply.
- Execute known-good and known-bad controls for critical checkers; run planned mutations.
- Capture raw command results and artifact digests without relying on Build's narrative.
- Return only `PASS`, `FAIL`, or `BLOCKED` per required predicate and overall.
- Do not repair implementation while acting as the independent Test principal.

## Outputs

- `evidence/runs/<run-id>/04-test/test-report.json`.
- `evidence/runs/<run-id>/04-test/evidence-manifest.json`.
- Raw logs and produced artifacts referenced by digest.

## Verification

- Every required predicate has an executed result or an explicit `BLOCKED` reason.
- Critical checkers reject their negative controls.
- Evidence includes commands, versions, inputs, timestamps, exit statuses, and raw results.
- No `BLOCKED` or missing result is counted as `PASS`.

## Promotion

Only a complete `PASS` trajectory proceeds to Review. `FAIL` returns to Plan or Build according to root cause. `BLOCKED` escalates.

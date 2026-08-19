# Verification Authority

Load this file for tests, checkers, fitness functions, evidence, completion, promotion, or release claims.

## Verdicts

- `PASS`: every required predicate was executed and satisfied with admissible evidence.
- `FAIL`: at least one required predicate was executed and disproven.
- `BLOCKED`: a required predicate could not be executed or its evidence was inadmissible.

`BLOCKED != PASS`. Absence of a failure is not evidence of success.

## Evidence requirements

For every executed check, record:

- repository commit or tree identity;
- exact command and working directory;
- tool and dependency versions;
- input and configuration digests;
- start and end timestamps;
- exit status;
- unedited stdout and stderr or durable references;
- produced artifact digests;
- checker identity and qualification state.

An agent statement that it ran a command is not evidence that the command ran.

## Checker qualification

- Test every critical checker against a known-good case and one or more known-bad cases.
- Use mutation testing when a seeded rule violation can prove detection sensitivity.
- Keep qualification fixtures independent from the implementation under test.
- A checker that accepts its required negative control is unqualified and its result is `BLOCKED`.
- The producer of a consequential result cannot be its sole acceptance authority.

## Fitness functions

Each architectural fitness function has a stable ID, source requirement, characteristic, scope, trigger or cadence, objective predicate, implementation, evidence contract, owner, and failure action. Run atomic functions before selective holistic functions. Wire triggered functions into CI; use continual or temporal functions when change-triggered execution cannot measure the characteristic.

## Completion

Only report a verification verdict that was actually produced. Preserve raw run evidence under `evidence/runs/<run-id>/`. Human merge remains the final gate for controlled structural changes.

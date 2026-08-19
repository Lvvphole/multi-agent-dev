# Scout Stage Contract

Layer: 2.
Single job: establish the evidence-backed current state before design or implementation.

## Inputs

- Root `AGENTS.md`.
- `workflows/implementation/CONTEXT.md`.
- The human task and accepted scope.
- The current repository tree, commit identity, and applicable routed Layer 3 references.

## Process

- Inspect before concluding.
- Separate observed repository facts from inferences and unknowns.
- Identify applicable locked requirements, existing behavior, dependencies, risks, and missing authority or information.
- Do not design the solution, change files, or claim runtime behavior that was not executed.

## Outputs

- `evidence/runs/<run-id>/01-scout/findings.md`.
- `evidence/runs/<run-id>/01-scout/source-manifest.json`.

## Verification

- Every consequential fact cites a repository path, commit, command result, or governed source.
- Source identities and digests are recorded.
- Unknowns and conflicts are explicit.
- The working tree is unchanged.

## Promotion

Human acceptance of the findings and scope is required before Plan.

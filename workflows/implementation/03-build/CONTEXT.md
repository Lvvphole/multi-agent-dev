# Build Stage Contract

Layer: 2.
Single job: implement the accepted Plan without changing its governing predicates.

## Inputs

- Accepted Plan artifacts and input manifest.
- Exact source commit or tree.
- Applicable architecture, authority, schemas, and file-scoped conventions.

## Process

- Implement only the accepted vertical slice.
- Preserve architecture boundaries and unrelated user changes.
- Add or update the planned tests and fitness-function implementations.
- Use runtime controls for authority and safety; prompts are not enforcement.
- Run narrow developer checks for feedback, but do not issue the independent Test verdict.
- If the Plan is impossible or unsafe, stop with `BLOCKED`; do not lower acceptance criteria.

## Outputs

- Source changes in the scoped branch or worktree.
- `evidence/runs/<run-id>/03-build/change-manifest.json`.
- `evidence/runs/<run-id>/03-build/developer-checks.json`.

## Verification

- The change manifest lists every changed path and requirement addressed.
- Developer checks record exact commands and exit statuses.
- No unapproved dependency, architecture, authority, governance, or acceptance change is present.

## Promotion

Build hands the immutable change identity and evidence references to Test. Build cannot mark its own work accepted.

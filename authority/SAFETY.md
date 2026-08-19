# Safety Authority

Load this file for destructive actions, hard constraints, approvals, reversibility, compensation, or escalation.

## Required controls

- Stay inside the human-approved task and change scope.
- Resolve exact targets before consequential action.
- Prefer reversible operations and preserve user work.
- Do not delete, overwrite, force-push, rotate credentials, change production, or alter governed controls without explicit authority.
- Hard legal, constitutional, security, safety, and risk constraints cannot be traded against outcome metrics.
- Define rollback before a reversible consequential action and compensation before a non-reversible multi-step action.
- Bound retries by attempts, cost, elapsed time, progress, and duplicate semantics.
- Stop and escalate when authority, evidence, safety, legal interpretation, state freshness, ownership, or recovery is unresolved.
- Governance and other structural changes require pull-request review, independent verification, and human merge approval.

## Safety result

Fail closed. Use `BLOCKED` for missing authority or evidence, `FAIL` for a disproven predicate, and never treat either state as successful completion.

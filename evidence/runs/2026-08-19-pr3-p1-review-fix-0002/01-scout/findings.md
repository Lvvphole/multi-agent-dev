# Scout Findings: PR #3 P1 Review Repair

Run: `2026-08-19-pr3-p1-review-fix-0002`

## Human objective and accepted scope

The repository maintainer directed the agent to read and comply with `AGENTS.md`, fix every Codex review issue, and stop only after Codex reports no major issues. That directive accepts the bounded scope of each actionable Codex review finding; it does not authorize merge or architecture changes.

## Observed current state

- PR #3 review at head `94b8cb24d8e033a4e08e11656343c1989c2c9c20` exposed the absolute-target and missing-predecessor P1 findings described below.
- Thread `PRRT_kwDOT3jdV86aVzHN` shows that an absolute Markdown target inside the current checkout is normalized back to the expected repository-relative path. The current checker therefore accepts a machine-specific route.
- Thread `PRRT_kwDOT3jdV86aVzHP` shows that run `2026-08-19-pr1-p1-review-fix-0001` has Build and Test artifacts but no accepted Scout or frozen Plan inputs. Its PASS claim is not admissible under the implementation workflow.
- The existing route checker and its 17-test qualification suite pass at the reviewed head. This does not disprove either P1 because the suite has no absolute-path mutation and the run evidence lacks predecessor-stage continuity.
- Human merge remains the final gate. This task does not authorize merge.

### Scout revision 2

Codex review at head `47e903b2b68c8bb9315b54fd3be40b1121bd1dc1` exposed two further current P1 findings:

- Thread `PRRT_kwDOT3jdV86aV76u`: the raw-line link scan counts bindings hidden inside HTML comments or fenced code, so required routes can disappear from rendered Markdown while the checker passes.
- Thread `PRRT_kwDOT3jdV86aV76x`: the evidence-integrity result records only a prose method and PASS assertion, not an exact executable command or persisted verifier identity.

The accepted scope therefore adds rendered-Markdown filtering, negative controls for hidden route declarations, and a persisted, qualified evidence-manifest verifier with an exact invocation.

## Applicable locked requirements

- `AGENTS.md`: explicit routing, `BLOCKED != PASS`, source-to-evidence traceability, and human merge authority.
- `authority/VERIFICATION.md`: every PASS predicate needs admissible evidence; critical checkers need known-good and known-bad qualification.
- Scout, Plan, Build, and Test stage contracts under `workflows/implementation/`.

## Risks

- Normalizing before rejecting absolute paths can hide non-portable or invalid Markdown routing.
- Repairing only the old report label would leave no reconstructible Scout-to-Test trajectory.
- Updating evidence after binding a tested commit can stale recorded digests unless the final bytes are rehashed.

## Unknowns and boundaries

- External Codex acceptance is pending and cannot be claimed by the producer.
- No runtime, persistence, authority, dependency, or enterprise-architecture change is required.
- The prior run is historical evidence and must be marked `BLOCKED` rather than rewritten as if its missing predecessor stages had existed.
- Plan revision 2 must be frozen before implementing the two findings from review commit `47e903b2b68c8bb9315b54fd3be40b1121bd1dc1`.

## Scout disposition

`ACCEPTED_SCOPE_BY_HUMAN_DIRECTIVE`: repair the two current P1 findings, preserve the already-fixed P1 behaviors, execute a fresh complete Scout-to-Test run, and submit the exact head for another Codex review.

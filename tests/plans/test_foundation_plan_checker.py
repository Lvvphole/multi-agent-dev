from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.verify_foundation_plan import validate_plan  # noqa: E402


RUN_ID = "fixture-run"
BASE_COMMIT = "0" * 40


def _dump(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source(source_id: str, source_class: str = "repository_blob") -> dict[str, Any]:
    identity = (
        "user-request:fixture"
        if source_class == "human_instruction"
        else f"git-blob:{'0' * 40}"
    )
    return {
        "id": source_id,
        "class": source_class,
        "title": source_id,
        "locator": f"fixture/{source_id}",
        "identity": identity,
        "claims_used": ["Independent fixture claim."],
    }


def _build_fixture(repo_root: Path) -> Path:
    run_root = repo_root / "evidence" / "runs" / RUN_ID
    scout = run_root / "01-scout"
    plan = run_root / "02-plan"
    scout.mkdir(parents=True)
    plan.mkdir(parents=True)

    findings_path = scout / "findings.md"
    findings_path.write_text(
        "# Fixture Scout Findings\n\n"
        "Status: `ACCEPTED_FOR_PLANNING`\n\n"
        "Production implementation is forbidden in this fixture run.\n",
        encoding="utf-8",
    )

    sources_path = scout / "source-manifest.json"
    _dump(
        sources_path,
        {
            "schema_version": "1.0.0",
            "run_id": RUN_ID,
            "base_commit": BASE_COMMIT,
            "sources": [
                _source("SRC-USER-TASK", "human_instruction"),
                _source("SRC-AGENTS"),
                _source("SRC-ARCH"),
                _source("SRC-VERIFY"),
                _source("SRC-PLAN-CONTRACT"),
                _source("SRC-PTRR-SPEC"),
            ],
        },
    )

    requirements_path = plan / "requirements.json"
    _dump(
        requirements_path,
        {
            "schema_version": "1.0.0",
            "run_id": RUN_ID,
            "requirements": [
                {
                    "id": "PTRR-FND-001",
                    "title": "Fixture requirement",
                    "source_ids": ["SRC-PTRR-SPEC"],
                    "source_locator": "fixture source",
                    "statement": "The fixture is structurally valid.",
                    "acceptance_predicate": "The checker accepts it.",
                    "evidence_contract": ["checker output"],
                    "verifier": "independent fixture verifier",
                    "failure_state": "FAIL",
                    "priority": "MUST",
                }
            ],
        },
    )

    fitness_path = plan / "fitness-functions.json"
    manual_gates = []
    for number in range(1, 5):
        manual_gates.append(
            {
                "id": f"MG-PTRR-{number:03d}",
                "source_requirement_ids": ["PTRR-FND-001"],
                "characteristic": "fixture human gate",
                "predicate": "A human supplies the named decision.",
                "owner": "fixture human",
                "status": "OPEN",
                "failure_action": "BLOCK_BUILD",
            }
        )
    _dump(
        fitness_path,
        {
            "schema_version": "1.0.0",
            "run_id": RUN_ID,
            "design_rule": "Fitness functions are independent acceptance predicates, not one compensating composite score.",
            "functions": [
                {
                    "id": "FF-PTRR-001",
                    "kind": "atomic",
                    "critical": True,
                    "source_requirement_ids": ["PTRR-FND-001"],
                    "characteristic": "fixture integrity",
                    "scope": "fixture",
                    "trigger": "fixture change",
                    "predicate": "The fixture remains valid.",
                    "implementation": {"status": "FIXTURE"},
                    "evidence_contract": ["fixture output"],
                    "owner": "fixture verifier",
                    "failure_action": "FAIL",
                    "negative_controls": [
                        {
                            "id": "NC-FIXTURE-001",
                            "mutation": "remove a required field",
                            "expected": "reject",
                        }
                    ],
                }
            ],
            "manual_gates": manual_gates,
            "execution_order": ["FF-PTRR-001"],
        },
    )

    plan_text = """# Fixture Plan

Plan status: `CANDIDATE`
Implementation gate: `BLOCKED`

## Single next best path
Stage 0 Objective Definition -> Stage 1 Problem Scouting -> Stage 2 Problem Validation.
No production implementation is permitted in this planning run.

## User and experience
The human receives evidence.

## Current state
No foundation exists.

## Desired state for this foundation
A bounded foundation exists.

## Objective and hard constraints
BLOCKED != PASS.

## Scope
Planning only.

## Logical contracts
Contracts are logical.

## Transition rules
Invalid transitions are rejected.

## Change sequence
Decide, contract, validate, commit, qualify.

## Testing strategy
Use known-good and known-bad fixtures.

## Evidence contract
Preserve raw outputs.

## Rollback and recovery
Revert the planning change.

## Blocking decisions
DEC-PTRR-001 through DEC-PTRR-005 remain unresolved. MG-PTRR-004 is open.

## Definition of done
The candidate is tested and independently reviewed.

## Promotion rule
MERGE = HUMAN DECISION.
"""
    (plan / "plan.md").write_text(plan_text, encoding="utf-8")

    common_fields = [
        "Goal",
        "Current State",
        "Desired State",
        "Gap",
        "Limitation",
        "Verified Need",
        "Target Behavior",
        "Constraint",
        "Intervention",
        "Expected Effect",
        "Evidence",
        "Buyer State",
        "Economic State",
        "Actual Outcome",
        "Value State",
        "Retention State",
        "Learning",
    ]
    decisions = []
    for number in range(1, 6):
        decisions.append(
            {
                "id": f"DEC-PTRR-{number:03d}",
                "question": "Fixture decision?",
                "decision_authority": "fixture human",
                "required_evidence": "fixture decision record",
                "status": "UNRESOLVED",
                "blocks": "BUILD",
            }
        )

    input_path = plan / "input-manifest.json"
    _dump(
        input_path,
        {
            "schema_version": "1.0.0",
            "run_id": RUN_ID,
            "base_commit": BASE_COMMIT,
            "plan_decision": {
                "candidate_status": "FIXTURE",
                "implementation_gate": "BLOCKED",
            },
            "business_slice": {
                "name": "Fixture foundation",
                "stages": [
                    {
                        "number": 0,
                        "name": "Objective Definition",
                        "required_fields": [
                            "Goal",
                            "Current State",
                            "Desired State",
                            "Definition of Done",
                            "Objective Function",
                            "Constraints",
                        ],
                        "exit_condition": "complete",
                    },
                    {
                        "number": 1,
                        "name": "Problem Scouting",
                        "required_output": "Candidate Problem",
                        "exit_condition": "candidate",
                    },
                    {
                        "number": 2,
                        "name": "Problem Validation",
                        "validation_gates": [
                            "Real",
                            "Unsatisfied",
                            "Consequential",
                            "Reachable",
                            "Solvable",
                        ],
                        "exit_condition": "validated",
                    },
                ],
                "allowed_outcomes": [
                    "VERIFIED_PROBLEM",
                    "REJECTED_TO_SCOUTING",
                    "BLOCKED",
                ],
                "forbidden_progression": "Stage 3 and later",
            },
            "common_operating_record_fields": common_fields,
            "status_namespaces": {
                "verification_verdicts": ["PASS", "FAIL", "BLOCKED"],
                "value_cycle_states": [
                    "CLOSED_SUCCESS",
                    "CLOSED_EXIT",
                    "BLOCKED",
                    "FAIL",
                    "CANCELLED",
                ],
                "software_delivery_outputs": [
                    "MERGE_READY",
                    "DO_NOT_MERGE",
                    "BLOCKED",
                ],
            },
            "change_scope": {
                "production_changes_allowed": False,
                "allowed_path_patterns": [
                    f"evidence/runs/{RUN_ID}/**",
                    "scripts/verify_foundation_plan.py",
                    "tests/plans/test_foundation_plan_checker.py",
                ],
                "forbidden_artifact_classes": [
                    "runtime",
                    "agent",
                    "capability",
                    "persistence",
                    "deployment",
                ],
                "rollback": "Delete the temporary fixture.",
            },
            "unresolved_decisions": decisions,
            "inputs": [
                {
                    "path": str(findings_path.relative_to(repo_root)),
                    "identity": f"sha256:{_digest(findings_path)}",
                    "role": "fixture findings",
                },
                {
                    "path": str(sources_path.relative_to(repo_root)),
                    "identity": f"sha256:{_digest(sources_path)}",
                    "role": "fixture sources",
                },
                {
                    "path": str(requirements_path.relative_to(repo_root)),
                    "identity": f"sha256:{_digest(requirements_path)}",
                    "role": "fixture requirements",
                },
                {
                    "path": str(fitness_path.relative_to(repo_root)),
                    "identity": f"sha256:{_digest(fitness_path)}",
                    "role": "fixture fitness",
                },
            ],
        },
    )
    return run_root


class FoundationPlanCheckerQualificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temporary_directory.name)
        self.run_root = _build_fixture(self.repo_root)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def _codes(self, changed_paths_file: Path | None = None) -> set[str]:
        return {
            finding.code
            for finding in validate_plan(
                self.run_root,
                self.repo_root,
                changed_paths_file,
            )
        }

    def _mutate_json(
        self, relative_path: str, mutation: Callable[[dict[str, Any]], None]
    ) -> None:
        path = self.run_root / relative_path
        data = _load(path)
        mutation(data)
        _dump(path, data)

    def test_known_good_fixture_is_accepted(self) -> None:
        self.assertEqual(set(), self._codes())

    def test_missing_source_binding_is_rejected(self) -> None:
        self._mutate_json(
            "02-plan/requirements.json",
            lambda data: data["requirements"][0].__setitem__("source_ids", []),
        )
        self.assertIn("REQ_SOURCE_EMPTY", self._codes())

    def test_uncovered_requirement_is_rejected(self) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data["functions"][0]["source_requirement_ids"] = []
            for gate in data["manual_gates"]:
                gate["source_requirement_ids"] = []

        self._mutate_json("02-plan/fitness-functions.json", mutate)
        self.assertIn("REQ_UNCOVERED", self._codes())

    def test_critical_checker_without_negative_control_is_rejected(self) -> None:
        self._mutate_json(
            "02-plan/fitness-functions.json",
            lambda data: data["functions"][0].__setitem__("negative_controls", []),
        )
        self.assertIn("FF_NEGATIVE_CONTROLS", self._codes())

    def test_missing_common_record_field_is_rejected(self) -> None:
        self._mutate_json(
            "02-plan/input-manifest.json",
            lambda data: data["common_operating_record_fields"].pop(),
        )
        self.assertIn("COMMON_FIELDS", self._codes())

    def test_missing_problem_validation_gate_is_rejected(self) -> None:
        self._mutate_json(
            "02-plan/input-manifest.json",
            lambda data: data["business_slice"]["stages"][2][
                "validation_gates"
            ].pop(),
        )
        self.assertIn("VALIDATION_GATES", self._codes())

    def test_unblocked_implementation_is_rejected(self) -> None:
        self._mutate_json(
            "02-plan/input-manifest.json",
            lambda data: data["plan_decision"].__setitem__(
                "implementation_gate", "OPEN"
            ),
        )
        self.assertIn("IMPLEMENTATION_GATE", self._codes())

    def test_production_scope_is_rejected(self) -> None:
        self._mutate_json(
            "02-plan/input-manifest.json",
            lambda data: data["change_scope"].__setitem__(
                "production_changes_allowed", True
            ),
        )
        self.assertIn("PRODUCTION_SCOPE", self._codes())

    def test_missing_human_gate_is_rejected(self) -> None:
        self._mutate_json(
            "02-plan/fitness-functions.json",
            lambda data: data["manual_gates"].pop(),
        )
        self.assertIn("MANUAL_GATES", self._codes())

    def test_changed_runtime_path_is_rejected(self) -> None:
        inventory = self.repo_root / "changed-paths.txt"
        inventory.write_text("contracts/runtime.py\n", encoding="utf-8")
        self.assertIn("CHANGED_PATH_SCOPE", self._codes(inventory))


if __name__ == "__main__":
    unittest.main()

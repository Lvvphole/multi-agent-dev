#!/usr/bin/env python3
"""Validate and qualify the Objective-to-Verified-Problem Plan artifacts.

This checker establishes structural conformance only. A PASS does not accept the
plan, authorize Build, or verify any future runtime behavior.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


CHECKER_ID = "foundation-plan-structure"
CHECKER_VERSION = "1.0.0"

COMMON_FIELDS = [
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

OBJECTIVE_FIELDS = [
    "Goal",
    "Current State",
    "Desired State",
    "Definition of Done",
    "Objective Function",
    "Constraints",
]

VALIDATION_GATES = [
    "Real",
    "Unsatisfied",
    "Consequential",
    "Reachable",
    "Solvable",
]

REQUIRED_SOURCE_IDS = {
    "SRC-USER-TASK",
    "SRC-AGENTS",
    "SRC-ARCH",
    "SRC-VERIFY",
    "SRC-PLAN-CONTRACT",
    "SRC-PTRR-SPEC",
}

REQUIRED_MANUAL_GATES = {
    "MG-PTRR-001",
    "MG-PTRR-002",
    "MG-PTRR-003",
    "MG-PTRR-004",
}

REQUIRED_PLAN_HEADINGS = [
    "## Single next best path",
    "## User and experience",
    "## Current state",
    "## Desired state for this foundation",
    "## Objective and hard constraints",
    "## Scope",
    "## Logical contracts",
    "## Transition rules",
    "## Change sequence",
    "## Testing strategy",
    "## Evidence contract",
    "## Rollback and recovery",
    "## Blocking decisions",
    "## Definition of done",
    "## Promotion rule",
]

REQUIRED_FILES = {
    "findings": Path("01-scout/findings.md"),
    "sources": Path("01-scout/source-manifest.json"),
    "plan": Path("02-plan/plan.md"),
    "requirements": Path("02-plan/requirements.json"),
    "fitness": Path("02-plan/fitness-functions.json"),
    "inputs": Path("02-plan/input-manifest.json"),
}


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    message: str


def _add(findings: list[Finding], code: str, message: str) -> None:
    findings.append(Finding(code, message))


def _load_json(path: Path, findings: list[Finding], label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _add(findings, "JSON_INVALID", f"{label}: {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        _add(findings, "JSON_ROOT_TYPE", f"{label}: JSON root must be an object")
        return {}
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_sources(
    data: dict[str, Any], findings: list[Finding]
) -> set[str]:
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        _add(findings, "SOURCES_EMPTY", "source manifest must contain sources")
        return set()

    source_ids: set[str] = set()
    for index, source in enumerate(sources):
        prefix = f"sources[{index}]"
        if not isinstance(source, dict):
            _add(findings, "SOURCE_TYPE", f"{prefix} must be an object")
            continue
        source_id = source.get("id")
        if not _is_nonempty_string(source_id):
            _add(findings, "SOURCE_ID", f"{prefix}.id must be non-empty")
            continue
        if source_id in source_ids:
            _add(findings, "SOURCE_DUPLICATE", f"duplicate source ID {source_id}")
        source_ids.add(source_id)
        for field in ("class", "title", "locator", "identity"):
            if not _is_nonempty_string(source.get(field)):
                _add(
                    findings,
                    "SOURCE_FIELD",
                    f"{source_id}.{field} must be non-empty",
                )
        claims = source.get("claims_used")
        if not isinstance(claims, list) or not claims or not all(
            _is_nonempty_string(claim) for claim in claims
        ):
            _add(
                findings,
                "SOURCE_CLAIMS",
                f"{source_id}.claims_used must contain non-empty claims",
            )

        identity = source.get("identity")
        if _is_nonempty_string(identity):
            recognized = bool(
                re.fullmatch(r"git-blob:[0-9a-f]{40}", identity)
                or re.fullmatch(r"sha256:[0-9a-f]{64}", identity)
                or identity.startswith("user-request:")
            )
            if not recognized:
                _add(
                    findings,
                    "SOURCE_IDENTITY",
                    f"{source_id}.identity is not a supported immutable identity",
                )

    missing = sorted(REQUIRED_SOURCE_IDS - source_ids)
    if missing:
        _add(
            findings,
            "SOURCE_REQUIRED",
            f"required source IDs missing: {', '.join(missing)}",
        )
    return source_ids


def _validate_requirements(
    data: dict[str, Any], source_ids: set[str], findings: list[Finding]
) -> set[str]:
    requirements = data.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        _add(findings, "REQUIREMENTS_EMPTY", "requirements must be a non-empty list")
        return set()

    requirement_ids: set[str] = set()
    required_fields = (
        "title",
        "source_locator",
        "statement",
        "acceptance_predicate",
        "verifier",
        "failure_state",
        "priority",
    )
    for index, requirement in enumerate(requirements):
        prefix = f"requirements[{index}]"
        if not isinstance(requirement, dict):
            _add(findings, "REQ_TYPE", f"{prefix} must be an object")
            continue
        requirement_id = requirement.get("id")
        if not isinstance(requirement_id, str) or not re.fullmatch(
            r"PTRR-FND-[0-9]{3}", requirement_id
        ):
            _add(findings, "REQ_ID", f"{prefix}.id must match PTRR-FND-NNN")
            continue
        if requirement_id in requirement_ids:
            _add(findings, "REQ_DUPLICATE", f"duplicate requirement {requirement_id}")
        requirement_ids.add(requirement_id)

        for field in required_fields:
            if not _is_nonempty_string(requirement.get(field)):
                _add(
                    findings,
                    "REQ_FIELD",
                    f"{requirement_id}.{field} must be non-empty",
                )

        bindings = requirement.get("source_ids")
        if not isinstance(bindings, list) or not bindings:
            _add(
                findings,
                "REQ_SOURCE_EMPTY",
                f"{requirement_id}.source_ids must be non-empty",
            )
        else:
            unknown = sorted(
                binding
                for binding in bindings
                if not isinstance(binding, str) or binding not in source_ids
            )
            if unknown:
                _add(
                    findings,
                    "REQ_SOURCE_UNKNOWN",
                    f"{requirement_id} references unknown sources: {unknown}",
                )

        evidence = requirement.get("evidence_contract")
        if not isinstance(evidence, list) or not evidence or not all(
            _is_nonempty_string(item) for item in evidence
        ):
            _add(
                findings,
                "REQ_EVIDENCE",
                f"{requirement_id}.evidence_contract must be non-empty",
            )

        if requirement.get("failure_state") not in {"FAIL", "BLOCKED"}:
            _add(
                findings,
                "REQ_FAILURE_STATE",
                f"{requirement_id}.failure_state must be FAIL or BLOCKED",
            )
        if requirement.get("priority") != "MUST":
            _add(
                findings,
                "REQ_PRIORITY",
                f"{requirement_id}.priority must be MUST for this foundation",
            )

    return requirement_ids


def _validate_fitness(
    data: dict[str, Any], requirement_ids: set[str], findings: list[Finding]
) -> tuple[set[str], set[str]]:
    functions = data.get("functions")
    if not isinstance(functions, list) or not functions:
        _add(findings, "FITNESS_EMPTY", "fitness functions must be non-empty")
        functions = []

    function_ids: set[str] = set()
    covered: set[str] = set()
    kind_by_id: dict[str, str] = {}
    required_fields = (
        "kind",
        "characteristic",
        "scope",
        "trigger",
        "predicate",
        "implementation",
        "evidence_contract",
        "owner",
        "failure_action",
    )
    negative_ids: set[str] = set()

    for index, function in enumerate(functions):
        prefix = f"functions[{index}]"
        if not isinstance(function, dict):
            _add(findings, "FF_TYPE", f"{prefix} must be an object")
            continue
        function_id = function.get("id")
        if not isinstance(function_id, str) or not re.fullmatch(
            r"FF-PTRR-[0-9]{3}", function_id
        ):
            _add(findings, "FF_ID", f"{prefix}.id must match FF-PTRR-NNN")
            continue
        if function_id in function_ids:
            _add(findings, "FF_DUPLICATE", f"duplicate fitness function {function_id}")
        function_ids.add(function_id)

        for field in required_fields:
            value = function.get(field)
            if field in {"implementation"}:
                valid = isinstance(value, dict) and bool(value)
            elif field in {"evidence_contract"}:
                valid = isinstance(value, list) and bool(value) and all(
                    _is_nonempty_string(item) for item in value
                )
            else:
                valid = _is_nonempty_string(value)
            if not valid:
                _add(
                    findings,
                    "FF_FIELD",
                    f"{function_id}.{field} is missing or invalid",
                )

        kind = function.get("kind")
        kind_by_id[function_id] = kind if isinstance(kind, str) else ""
        if kind not in {"atomic", "holistic", "continual", "temporal"}:
            _add(
                findings,
                "FF_KIND",
                f"{function_id}.kind must be an approved fitness kind",
            )

        bindings = function.get("source_requirement_ids")
        if not isinstance(bindings, list) or not bindings:
            _add(
                findings,
                "FF_REQUIREMENTS_EMPTY",
                f"{function_id}.source_requirement_ids must be non-empty",
            )
        else:
            for binding in bindings:
                if binding not in requirement_ids:
                    _add(
                        findings,
                        "FF_REQUIREMENT_UNKNOWN",
                        f"{function_id} references unknown requirement {binding}",
                    )
                else:
                    covered.add(binding)

        if function.get("critical") is not True:
            _add(
                findings,
                "FF_CRITICAL",
                f"{function_id}.critical must be true for this foundation",
            )

        negatives = function.get("negative_controls")
        if not isinstance(negatives, list) or not negatives:
            _add(
                findings,
                "FF_NEGATIVE_CONTROLS",
                f"{function_id} must declare negative controls",
            )
        else:
            for negative_index, negative in enumerate(negatives):
                if not isinstance(negative, dict):
                    _add(
                        findings,
                        "FF_NEGATIVE_TYPE",
                        f"{function_id}.negative_controls[{negative_index}] must be an object",
                    )
                    continue
                negative_id = negative.get("id")
                if not _is_nonempty_string(negative_id):
                    _add(
                        findings,
                        "FF_NEGATIVE_ID",
                        f"{function_id} has a negative without an ID",
                    )
                elif negative_id in negative_ids:
                    _add(
                        findings,
                        "FF_NEGATIVE_DUPLICATE",
                        f"duplicate negative-control ID {negative_id}",
                    )
                else:
                    negative_ids.add(negative_id)
                for field in ("mutation", "expected"):
                    if not _is_nonempty_string(negative.get(field)):
                        _add(
                            findings,
                            "FF_NEGATIVE_FIELD",
                            f"{function_id}.{negative_id}.{field} must be non-empty",
                        )

    manual_gates = data.get("manual_gates")
    if not isinstance(manual_gates, list) or not manual_gates:
        _add(findings, "MANUAL_GATES_EMPTY", "manual_gates must be non-empty")
        manual_gates = []

    manual_gate_ids: set[str] = set()
    for index, gate in enumerate(manual_gates):
        prefix = f"manual_gates[{index}]"
        if not isinstance(gate, dict):
            _add(findings, "MANUAL_GATE_TYPE", f"{prefix} must be an object")
            continue
        gate_id = gate.get("id")
        if not _is_nonempty_string(gate_id):
            _add(findings, "MANUAL_GATE_ID", f"{prefix}.id must be non-empty")
            continue
        if gate_id in manual_gate_ids:
            _add(findings, "MANUAL_GATE_DUPLICATE", f"duplicate gate {gate_id}")
        manual_gate_ids.add(gate_id)
        for field in ("characteristic", "predicate", "owner", "failure_action"):
            if not _is_nonempty_string(gate.get(field)):
                _add(
                    findings,
                    "MANUAL_GATE_FIELD",
                    f"{gate_id}.{field} must be non-empty",
                )
        if gate.get("status") not in {"OPEN", "SATISFIED"}:
            _add(
                findings,
                "MANUAL_GATE_STATUS",
                f"{gate_id}.status must be OPEN or SATISFIED",
            )
        bindings = gate.get("source_requirement_ids")
        if not isinstance(bindings, list) or not bindings:
            _add(
                findings,
                "MANUAL_GATE_REQUIREMENTS",
                f"{gate_id}.source_requirement_ids must be non-empty",
            )
        else:
            for binding in bindings:
                if binding not in requirement_ids:
                    _add(
                        findings,
                        "MANUAL_GATE_REQUIREMENT_UNKNOWN",
                        f"{gate_id} references unknown requirement {binding}",
                    )
                else:
                    covered.add(binding)

    if manual_gate_ids != REQUIRED_MANUAL_GATES:
        _add(
            findings,
            "MANUAL_GATES",
            "manual gate IDs must be exactly "
            + ", ".join(sorted(REQUIRED_MANUAL_GATES)),
        )

    uncovered = sorted(requirement_ids - covered)
    if uncovered:
        _add(
            findings,
            "REQ_UNCOVERED",
            f"requirements without a fitness function or manual gate: {', '.join(uncovered)}",
        )

    execution_order = data.get("execution_order")
    if not isinstance(execution_order, list):
        _add(findings, "FF_EXECUTION_ORDER", "execution_order must be a list")
    else:
        if len(execution_order) != len(set(execution_order)):
            _add(
                findings,
                "FF_EXECUTION_DUPLICATE",
                "execution_order contains duplicates",
            )
        if set(execution_order) != function_ids:
            _add(
                findings,
                "FF_EXECUTION_COVERAGE",
                "execution_order must contain every fitness function exactly once",
            )
        holistic_seen = False
        for function_id in execution_order:
            kind = kind_by_id.get(function_id)
            if kind == "holistic":
                holistic_seen = True
            elif kind == "atomic" and holistic_seen:
                _add(
                    findings,
                    "FF_EXECUTION_SEQUENCE",
                    "atomic functions must execute before holistic functions",
                )
                break

    if data.get("design_rule") != (
        "Fitness functions are independent acceptance predicates, not one "
        "compensating composite score."
    ):
        _add(
            findings,
            "FF_DESIGN_RULE",
            "fitness design must forbid a compensating composite score",
        )

    return function_ids, manual_gate_ids


def _validate_business_slice(data: dict[str, Any], findings: list[Finding]) -> None:
    if data.get("common_operating_record_fields") != COMMON_FIELDS:
        _add(
            findings,
            "COMMON_FIELDS",
            "common operating-record fields must exactly match the approved 17-field order",
        )

    business_slice = data.get("business_slice")
    if not isinstance(business_slice, dict):
        _add(findings, "BUSINESS_SLICE", "business_slice must be an object")
        return
    stages = business_slice.get("stages")
    if not isinstance(stages, list) or len(stages) != 3:
        _add(findings, "BUSINESS_STAGES", "business_slice must contain three stages")
        return
    stage_keys = [(stage.get("number"), stage.get("name")) for stage in stages if isinstance(stage, dict)]
    expected = [
        (0, "Objective Definition"),
        (1, "Problem Scouting"),
        (2, "Problem Validation"),
    ]
    if stage_keys != expected:
        _add(
            findings,
            "BUSINESS_STAGES",
            "business stages must be exactly 0 Objective Definition, 1 Problem Scouting, and 2 Problem Validation",
        )
        return
    if stages[0].get("required_fields") != OBJECTIVE_FIELDS:
        _add(
            findings,
            "OBJECTIVE_FIELDS",
            "Stage 0 required fields do not match the approved objective contract",
        )
    if stages[1].get("required_output") != "Candidate Problem":
        _add(
            findings,
            "SCOUT_OUTPUT",
            "Stage 1 output must be Candidate Problem",
        )
    if stages[2].get("validation_gates") != VALIDATION_GATES:
        _add(
            findings,
            "VALIDATION_GATES",
            "Stage 2 gates must be exactly Real, Unsatisfied, Consequential, Reachable, and Solvable",
        )
    if business_slice.get("allowed_outcomes") != [
        "VERIFIED_PROBLEM",
        "REJECTED_TO_SCOUTING",
        "BLOCKED",
    ]:
        _add(
            findings,
            "BUSINESS_OUTCOMES",
            "foundation outcomes do not match the approved bounded slice",
        )
    if "Stage 3" not in str(business_slice.get("forbidden_progression", "")):
        _add(
            findings,
            "FORBIDDEN_PROGRESSION",
            "the foundation must explicitly forbid Stage 3 progression",
        )


def _validate_statuses(data: dict[str, Any], findings: list[Finding]) -> None:
    statuses = data.get("status_namespaces")
    expected = {
        "verification_verdicts": ["PASS", "FAIL", "BLOCKED"],
        "value_cycle_states": [
            "CLOSED_SUCCESS",
            "CLOSED_EXIT",
            "BLOCKED",
            "FAIL",
            "CANCELLED",
        ],
        "software_delivery_outputs": ["MERGE_READY", "DO_NOT_MERGE", "BLOCKED"],
    }
    if statuses != expected:
        _add(
            findings,
            "STATUS_NAMESPACES",
            "verification, value-cycle, and software-delivery statuses must remain distinct",
        )


def _validate_scope_and_decisions(
    data: dict[str, Any], run_id: str, findings: list[Finding]
) -> list[str]:
    scope = data.get("change_scope")
    allowed_patterns: list[str] = []
    if not isinstance(scope, dict):
        _add(findings, "CHANGE_SCOPE", "change_scope must be an object")
    else:
        if scope.get("production_changes_allowed") is not False:
            _add(
                findings,
                "PRODUCTION_SCOPE",
                "production changes must be forbidden in this planning run",
            )
        patterns = scope.get("allowed_path_patterns")
        if not isinstance(patterns, list) or not all(
            _is_nonempty_string(pattern) for pattern in patterns
        ):
            _add(
                findings,
                "ALLOWED_PATHS",
                "allowed_path_patterns must be a non-empty string list",
            )
        else:
            allowed_patterns = patterns
            required = {
                f"evidence/runs/{run_id}/**",
                "scripts/verify_foundation_plan.py",
                "tests/plans/test_foundation_plan_checker.py",
            }
            missing = sorted(required - set(patterns))
            if missing:
                _add(
                    findings,
                    "ALLOWED_PATHS",
                    f"planning path patterns missing: {', '.join(missing)}",
                )
        forbidden = scope.get("forbidden_artifact_classes")
        if not isinstance(forbidden, list) or len(forbidden) < 5:
            _add(
                findings,
                "FORBIDDEN_ARTIFACTS",
                "planning scope must explicitly exclude runtime artifact classes",
            )
        if not _is_nonempty_string(scope.get("rollback")):
            _add(findings, "ROLLBACK", "planning scope must define rollback")

    decisions = data.get("unresolved_decisions")
    if not isinstance(decisions, list) or not decisions:
        _add(
            findings,
            "UNRESOLVED_DECISIONS",
            "unresolved decisions must be explicit and non-empty",
        )
    else:
        decision_ids: set[str] = set()
        for index, decision in enumerate(decisions):
            if not isinstance(decision, dict):
                _add(
                    findings,
                    "DECISION_TYPE",
                    f"unresolved_decisions[{index}] must be an object",
                )
                continue
            decision_id = decision.get("id")
            if not _is_nonempty_string(decision_id):
                _add(findings, "DECISION_ID", f"decision {index} has no ID")
                continue
            if decision_id in decision_ids:
                _add(
                    findings,
                    "DECISION_DUPLICATE",
                    f"duplicate decision {decision_id}",
                )
            decision_ids.add(decision_id)
            for field in (
                "question",
                "decision_authority",
                "required_evidence",
                "blocks",
            ):
                if not _is_nonempty_string(decision.get(field)):
                    _add(
                        findings,
                        "DECISION_FIELD",
                        f"{decision_id}.{field} must be non-empty",
                    )
            if decision.get("status") != "UNRESOLVED":
                _add(
                    findings,
                    "DECISION_STATUS",
                    f"{decision_id} must remain UNRESOLVED until decision evidence exists",
                )
        if decision_ids != {f"DEC-PTRR-{number:03d}" for number in range(1, 6)}:
            _add(
                findings,
                "DECISION_SET",
                "decision IDs must be exactly DEC-PTRR-001 through DEC-PTRR-005",
            )

    decision = data.get("plan_decision")
    if not isinstance(decision, dict) or decision.get("implementation_gate") != "BLOCKED":
        _add(
            findings,
            "IMPLEMENTATION_GATE",
            "implementation must remain BLOCKED while decisions or human gates are open",
        )
    return allowed_patterns


def _validate_input_digests(
    data: dict[str, Any], repo_root: Path, findings: list[Finding]
) -> None:
    inputs = data.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        _add(findings, "INPUTS_EMPTY", "input manifest must list inputs")
        return
    seen: set[str] = set()
    for index, item in enumerate(inputs):
        if not isinstance(item, dict):
            _add(findings, "INPUT_TYPE", f"inputs[{index}] must be an object")
            continue
        relative = item.get("path")
        identity = item.get("identity")
        if not _is_nonempty_string(relative) or not _is_nonempty_string(identity):
            _add(
                findings,
                "INPUT_FIELD",
                f"inputs[{index}] needs path and identity",
            )
            continue
        if relative in seen:
            _add(findings, "INPUT_DUPLICATE", f"duplicate input path {relative}")
        seen.add(relative)
        if relative.startswith("/") or ".." in Path(relative).parts:
            _add(findings, "INPUT_PATH", f"unsafe input path {relative}")
            continue
        path = repo_root / relative
        if not path.is_file():
            _add(findings, "INPUT_MISSING", f"input does not exist: {relative}")
            continue
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", identity):
            _add(
                findings,
                "INPUT_IDENTITY",
                f"input identity is not sha256: {relative}",
            )
            continue
        actual = _sha256(path)
        if identity != f"sha256:{actual}":
            _add(
                findings,
                "INPUT_DIGEST",
                f"input digest mismatch: {relative}",
            )


def _validate_plan_text(text: str, findings: list[Finding]) -> None:
    for heading in REQUIRED_PLAN_HEADINGS:
        if heading not in text:
            _add(findings, "PLAN_HEADING", f"plan missing heading: {heading}")
    required_tokens = [
        "Plan status: `CANDIDATE`",
        "Implementation gate: `BLOCKED`",
        "No production implementation is permitted in this planning run.",
        "Stage 0 Objective Definition",
        "Stage 1 Problem Scouting",
        "Stage 2 Problem Validation",
        "DEC-PTRR-001",
        "DEC-PTRR-005",
        "MG-PTRR-004",
        "BLOCKED != PASS",
        "MERGE = HUMAN DECISION",
    ]
    for token in required_tokens:
        if token not in text:
            _add(findings, "PLAN_TOKEN", f"plan missing required token: {token}")


def _validate_changed_paths(
    changed_paths_file: Path | None,
    allowed_patterns: list[str],
    findings: list[Finding],
) -> None:
    if changed_paths_file is None:
        return
    try:
        paths = [
            line.strip()
            for line in changed_paths_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    except (OSError, UnicodeError) as exc:
        _add(
            findings,
            "CHANGED_PATHS_FILE",
            f"cannot read changed-path inventory: {exc}",
        )
        return
    if not paths:
        _add(findings, "CHANGED_PATHS_EMPTY", "changed-path inventory is empty")
        return
    for path in paths:
        if path.startswith("/") or ".." in Path(path).parts:
            _add(findings, "CHANGED_PATH_UNSAFE", f"unsafe changed path: {path}")
            continue
        if not any(fnmatch.fnmatchcase(path, pattern) for pattern in allowed_patterns):
            _add(
                findings,
                "CHANGED_PATH_SCOPE",
                f"changed path is outside planning-only scope: {path}",
            )


def validate_plan(
    run_root: Path,
    repo_root: Path,
    changed_paths_file: Path | None = None,
) -> list[Finding]:
    """Return deterministic structural findings for one Plan run."""

    run_root = run_root.resolve()
    repo_root = repo_root.resolve()
    findings: list[Finding] = []
    paths = {name: run_root / relative for name, relative in REQUIRED_FILES.items()}
    for name, path in paths.items():
        if not path.is_file():
            _add(findings, "FILE_MISSING", f"required {name} file missing: {path}")
    if findings:
        return sorted(set(findings))

    sources = _load_json(paths["sources"], findings, "source manifest")
    requirements = _load_json(paths["requirements"], findings, "requirements")
    fitness = _load_json(paths["fitness"], findings, "fitness functions")
    inputs = _load_json(paths["inputs"], findings, "input manifest")
    try:
        plan_text = paths["plan"].read_text(encoding="utf-8")
        findings_text = paths["findings"].read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        _add(findings, "TEXT_INVALID", str(exc))
        return sorted(set(findings))

    run_ids = {
        sources.get("run_id"),
        requirements.get("run_id"),
        fitness.get("run_id"),
        inputs.get("run_id"),
    }
    expected_run_id = run_root.name
    if run_ids != {expected_run_id}:
        _add(
            findings,
            "RUN_ID",
            f"all structured artifacts must use run ID {expected_run_id}",
        )

    base_commits = {sources.get("base_commit"), inputs.get("base_commit")}
    if len(base_commits) != 1 or not re.fullmatch(
        r"[0-9a-f]{40}", str(next(iter(base_commits), ""))
    ):
        _add(
            findings,
            "BASE_COMMIT",
            "source and input manifests must share one 40-character base commit",
        )

    if "Status: `ACCEPTED_FOR_PLANNING`" not in findings_text:
        _add(
            findings,
            "SCOUT_ACCEPTANCE",
            "Scout findings must be accepted for planning",
        )
    if "production implementation is forbidden" not in findings_text.lower():
        _add(
            findings,
            "SCOUT_SCOPE",
            "Scout findings must forbid production implementation in this run",
        )

    source_ids = _validate_sources(sources, findings)
    requirement_ids = _validate_requirements(requirements, source_ids, findings)
    _validate_fitness(fitness, requirement_ids, findings)
    _validate_business_slice(inputs, findings)
    _validate_statuses(inputs, findings)
    allowed_patterns = _validate_scope_and_decisions(
        inputs, expected_run_id, findings
    )
    _validate_input_digests(inputs, repo_root, findings)
    _validate_plan_text(plan_text, findings)
    _validate_changed_paths(changed_paths_file, allowed_patterns, findings)

    return sorted(set(findings))


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-root",
        required=True,
        type=Path,
        help="Run root containing 01-scout and 02-plan",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root used to resolve input-manifest paths",
    )
    parser.add_argument(
        "--changed-paths-file",
        type=Path,
        default=None,
        help="Optional newline-delimited candidate changed-path inventory",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    findings = validate_plan(
        args.run_root,
        args.repo_root,
        args.changed_paths_file,
    )
    report = {
        "checker_id": CHECKER_ID,
        "checker_version": CHECKER_VERSION,
        "run_id": args.run_root.name,
        "verdict": "FAIL" if findings else "PASS",
        "scope": "plan artifact structural conformance only",
        "authorizes_build": False,
        "findings": [asdict(finding) for finding in findings],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())

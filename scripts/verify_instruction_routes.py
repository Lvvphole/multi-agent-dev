#!/usr/bin/env python3
"""Deterministically validate the repository instruction-routing structure."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path, PurePosixPath, PureWindowsPath


ROOT = Path(__file__).resolve().parents[1]
ROOT_CONTRACT_NAME = "AGENTS.md"
ROOT_OVERRIDE_NAME = "AGENTS.override.md"
CONTEXT_NAME = "CONTEXT.md"
ROOT_CONTRACT = ROOT / ROOT_CONTRACT_NAME
BUSINESS_OPERATING_SPEC = (
    ROOT / "docs" / "specs" / "problem-to-retained-revenue-operating-system.md"
)
EXPECTED_STAGES = (
    "01-scout",
    "02-plan",
    "03-build",
    "04-test",
    "05-review",
)
EXPECTED_BUSINESS_STAGES = (
    "Objective Definition",
    "Problem Scouting",
    "Problem Validation",
    "Gap Diagnosis",
    "Solution Design",
    "Distribution",
    "Demand Generation",
    "Behavioral Progression",
    "Revenue",
    "Implementation",
    "Value Realization",
    "Retention and Expansion",
)
EXPECTED_CANONICAL_SEQUENCE = tuple(enumerate(EXPECTED_BUSINESS_STAGES)) + (
    (0, "Objective Definition revalidation"),
    (1, "Problem Scouting"),
)
REQUIRED_STAGE_HEADINGS = (
    "## Inputs",
    "## Process",
    "## Outputs",
    "## Verification",
    "## Promotion",
)
REQUIRED_ROOT_MARKERS = (
    "Problem-to-Retained-Revenue Operating System",
    "software pipeline is a subordinate delivery capability",
    "MODEL != AUTHORITY",
    "TOOL AVAILABILITY != PERMISSION",
    "BLOCKED != PASS",
    "capabilityRuntime.invoke(...)",
    "Only the state-transition service may commit canonical enterprise state",
)
REQUIRED_BUSINESS_MARKERS = (
    (
        "The system has **12 operating stages**, numbered `0` through `11`",
        "12-stage declaration",
    ),
    (
        "Stage 5 Distribution\n  -> Stage 6 Demand Generation\n  -> Stage 7 Behavioral Progression",
        "Distribution-to-Demand-Generation sequence",
    ),
    ("Stage 11 -> Stage 0 -> Stage 1", "normalized return path"),
    (
        "`CLOSED_EXIT`: the relationship was intentionally ended and learning "
        "was captured. This closes the cycle but is not retained-revenue success.",
        "closed-exit distinction",
    ),
    (
        "The software factory cannot claim target behavior change, realized "
        "client value, retained revenue, or expansion.",
        "software-delivery boundary",
    ),
)
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BUSINESS_STAGE_PATTERN = re.compile(r"^\| (\d+) \| ([^|]+?) \|", re.MULTILINE)
CANONICAL_SEQUENCE_PATTERN = re.compile(
    r"The canonical sequence is:\s*```text\n(?P<body>.*?)\n```",
    re.DOTALL,
)
CANONICAL_STAGE_LINE_PATTERN = re.compile(r"(?:->\s+)?Stage (\d+) (.+)")


def path_label_binding(
    declaration: str,
    target: str,
) -> tuple[str, str, str]:
    return declaration, target, target


def is_absolute_route_target(target: str) -> bool:
    return PurePosixPath(target).is_absolute() or PureWindowsPath(target).is_absolute()


EXPECTED_ROUTE_BINDINGS = {
    ROOT_CONTRACT_NAME: (
        path_label_binding(
            "| Architecture, boundaries, topology, data ownership, control flow, or runtime design |",
            "ARCHITECTURE.md",
        ),
        path_label_binding(
            "| Identity, authority, capabilities, A2A trust, secrets, or external effects |",
            "authority/SECURITY.md",
        ),
        path_label_binding(
            "| Destructive action, safety constraint, approval, reversibility, or escalation |",
            "authority/SAFETY.md",
        ),
        path_label_binding(
            "| Context, retrieval, durable memory, provenance, freshness, or inheritance |",
            "authority/MEMORY.md",
        ),
        path_label_binding(
            "| Tests, checkers, evidence, acceptance, completion, or release claims |",
            "authority/VERIFICATION.md",
        ),
        path_label_binding(
            "| Enterprise goal, client state, customer gap, value cycle, revenue, retention, business stage, or operating metric |",
            "docs/specs/problem-to-retained-revenue-operating-system.md",
        ),
        path_label_binding(
            "| Scout, Plan, Build, Test, Review, sprint execution, or stage promotion |",
            "workflows/implementation/CONTEXT.md",
        ),
    ),
    "ARCHITECTURE.md": (
        (
            "Build a governed multi-agent organization that implements the",
            "Problem-to-Retained-Revenue Operating System",
            "docs/specs/problem-to-retained-revenue-operating-system.md",
        ),
        (
            "-",
            "ADR-0001 - Authoritative AGENTS.md with ICM context routing",
            "docs/adr/0001-authoritative-agents-and-icm-routing.md",
        ),
        (
            "-",
            "ADR-0002 - Problem-to-Retained-Revenue organizational objective",
            "docs/adr/0002-problem-to-retained-revenue-organizational-objective.md",
        ),
    ),
    "workflows/implementation/CONTEXT.md": (
        (
            "| 01 | Scout | Establish evidence-backed current state and uncertainty |",
            "01-scout/CONTEXT.md",
            "workflows/implementation/01-scout/CONTEXT.md",
        ),
        (
            "| 02 | Plan | Bind requirements, data, fitness functions, and the smallest implementation slice |",
            "02-plan/CONTEXT.md",
            "workflows/implementation/02-plan/CONTEXT.md",
        ),
        (
            "| 03 | Build | Implement only the accepted slice |",
            "03-build/CONTEXT.md",
            "workflows/implementation/03-build/CONTEXT.md",
        ),
        (
            "| 04 | Test | Independently execute and preserve verification evidence |",
            "04-test/CONTEXT.md",
            "workflows/implementation/04-test/CONTEXT.md",
        ),
        (
            "| 05 | Review | Adjudicate compliance and promotion readiness |",
            "05-review/CONTEXT.md",
            "workflows/implementation/05-review/CONTEXT.md",
        ),
    ),
}


def local_route_bindings(
    path: Path,
    errors: list[str],
) -> tuple[tuple[str, str, str], ...]:
    source = path.relative_to(ROOT).as_posix()
    bindings: list[tuple[str, str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        for link in LINK_PATTERN.finditer(line):
            label, target = link.groups()
            if "://" in target or target.startswith("#"):
                continue
            clean_target = target.split("#", 1)[0]
            if is_absolute_route_target(clean_target):
                errors.append(f"absolute route target in {source}: {target}")
                continue
            resolved_target = (path.parent / clean_target).resolve()
            try:
                repository_target = resolved_target.relative_to(ROOT)
            except ValueError:
                errors.append(f"route outside repository in {source}: {target}")
                continue

            repository_target_text = repository_target.as_posix()
            declaration = line[: link.start()].strip()
            bindings.append((declaration, label, repository_target_text))
            if not resolved_target.is_file():
                errors.append(f"broken route in {source}: {repository_target_text}")

    return tuple(bindings)


def canonical_business_sequence(business_text: str) -> tuple[tuple[int, str], ...]:
    block = CANONICAL_SEQUENCE_PATTERN.search(business_text)
    if block is None:
        return ()

    sequence: list[tuple[int, str]] = []
    for line in block.group("body").splitlines():
        stage = CANONICAL_STAGE_LINE_PATTERN.fullmatch(line.strip())
        if stage is None:
            return ()
        sequence.append((int(stage.group(1)), stage.group(2)))
    return tuple(sequence)


def main() -> int:
    errors: list[str] = []

    if not ROOT_CONTRACT.is_file():
        errors.append(f"missing root {ROOT_CONTRACT_NAME}")
    else:
        root_text = ROOT_CONTRACT.read_text(encoding="utf-8")
        line_count = len(root_text.splitlines())
        byte_count = len(root_text.encode("utf-8"))
        if line_count > 200:
            errors.append(f"root {ROOT_CONTRACT_NAME} exceeds 200 lines: {line_count}")
        if byte_count > 32 * 1024:
            errors.append(
                f"root {ROOT_CONTRACT_NAME} exceeds 32 KiB: {byte_count} bytes"
            )
        for marker in REQUIRED_ROOT_MARKERS:
            if marker not in root_text:
                errors.append(
                    f"root {ROOT_CONTRACT_NAME} missing invariant: {marker}"
                )

    discovered_instruction_files = sorted(
        path.relative_to(ROOT).as_posix()
        for pattern in (ROOT_CONTRACT_NAME, ROOT_OVERRIDE_NAME)
        for path in ROOT.rglob(pattern)
    )
    if discovered_instruction_files != [ROOT_CONTRACT_NAME]:
        errors.append(
            "implicit instruction precedence detected: "
            + ", ".join(discovered_instruction_files)
        )

    for source_name, expected_bindings in EXPECTED_ROUTE_BINDINGS.items():
        source = ROOT / source_name
        if not source.is_file():
            errors.append(f"missing route source: {source.relative_to(ROOT)}")
            continue
        actual_bindings = local_route_bindings(source, errors)
        if Counter(actual_bindings) != Counter(expected_bindings):
            errors.append(
                f"route binding mismatch in {source_name}: "
                f"expected {tuple(sorted(expected_bindings))}, "
                f"got {tuple(sorted(actual_bindings))}"
            )

    if not BUSINESS_OPERATING_SPEC.is_file():
        errors.append(
            f"missing business operating specification: "
            f"{BUSINESS_OPERATING_SPEC.relative_to(ROOT)}"
        )
    else:
        business_text = BUSINESS_OPERATING_SPEC.read_text(encoding="utf-8")
        for marker, label in REQUIRED_BUSINESS_MARKERS:
            if marker not in business_text:
                errors.append(f"business operating specification missing: {label}")

        actual_business_stages = tuple(
            (int(number), name.strip())
            for number, name in BUSINESS_STAGE_PATTERN.findall(business_text)
        )
        expected_business_stages = tuple(enumerate(EXPECTED_BUSINESS_STAGES))
        if actual_business_stages != expected_business_stages:
            errors.append(
                "business stage order mismatch: "
                f"expected {expected_business_stages}, got {actual_business_stages}"
            )

        actual_canonical_sequence = canonical_business_sequence(business_text)
        if actual_canonical_sequence != EXPECTED_CANONICAL_SEQUENCE:
            errors.append(
                "business canonical sequence mismatch: "
                f"expected {EXPECTED_CANONICAL_SEQUENCE}, "
                f"got {actual_canonical_sequence}"
            )

    stages_root = ROOT / "workflows" / "implementation"
    actual_stages = tuple(
        sorted(
            path.name
            for path in stages_root.iterdir()
            if path.is_dir() and re.fullmatch(r"\d{2}-[a-z]+", path.name)
        )
    ) if stages_root.is_dir() else ()
    if actual_stages != EXPECTED_STAGES:
        errors.append(
            f"stage order mismatch: expected {EXPECTED_STAGES}, got {actual_stages}"
        )

    for stage in EXPECTED_STAGES:
        contract = stages_root / stage / CONTEXT_NAME
        if not contract.is_file():
            errors.append(f"missing stage contract: {contract.relative_to(ROOT)}")
            continue
        text = contract.read_text(encoding="utf-8")
        for heading in REQUIRED_STAGE_HEADINGS:
            if heading not in text:
                errors.append(
                    f"{contract.relative_to(ROOT)} missing heading: {heading}"
                )

    if errors:
        print("INSTRUCTION_ROUTING: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("INSTRUCTION_ROUTING: PASS")
    print(f"root_contract={ROOT_CONTRACT_NAME}")
    print(f"root_lines={len(ROOT_CONTRACT.read_text(encoding='utf-8').splitlines())}")
    print(f"stages={','.join(EXPECTED_STAGES)}")
    print(f"business_operating_stages={len(EXPECTED_BUSINESS_STAGES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

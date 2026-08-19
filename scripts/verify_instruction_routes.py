#!/usr/bin/env python3
"""Deterministically validate the repository instruction-routing structure."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOT_CONTRACT_NAME = "AGENTS.md"
ROOT_OVERRIDE_NAME = "AGENTS.override.md"
CONTEXT_NAME = "CONTEXT.md"
ROOT_CONTRACT = ROOT / ROOT_CONTRACT_NAME
ARCHITECTURE_REFERENCE = ROOT / "ARCHITECTURE.md"
WORKFLOW_ROUTER = ROOT / "workflows" / "implementation" / CONTEXT_NAME
EXPECTED_STAGES = (
    "01-scout",
    "02-plan",
    "03-build",
    "04-test",
    "05-review",
)
REQUIRED_STAGE_HEADINGS = (
    "## Inputs",
    "## Process",
    "## Outputs",
    "## Verification",
    "## Promotion",
)
REQUIRED_ROOT_MARKERS = (
    "MODEL != AUTHORITY",
    "TOOL AVAILABILITY != PERMISSION",
    "BLOCKED != PASS",
    "capabilityRuntime.invoke(...)",
    "Only the state-transition service may commit canonical enterprise state",
)
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def local_links(path: Path) -> list[Path]:
    links: list[Path] = []
    for target in LINK_PATTERN.findall(path.read_text(encoding="utf-8")):
        if "://" in target or target.startswith("#"):
            continue
        clean_target = target.split("#", 1)[0]
        links.append((path.parent / clean_target).resolve())
    return links


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

    route_sources = [ROOT_CONTRACT, ARCHITECTURE_REFERENCE, WORKFLOW_ROUTER]
    for source in route_sources:
        if not source.is_file():
            errors.append(f"missing route source: {source.relative_to(ROOT)}")
            continue
        for target in local_links(source):
            if not target.exists():
                errors.append(
                    f"broken route in {source.relative_to(ROOT)}: "
                    f"{target.relative_to(ROOT)}"
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
    return 0


if __name__ == "__main__":
    sys.exit(main())

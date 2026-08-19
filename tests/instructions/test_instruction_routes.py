from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = Path("scripts/verify_instruction_routes.py")


class InstructionRouteCheckerTest(unittest.TestCase):
    def run_checker(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, CHECKER_PATH.as_posix()],
            cwd=root,
            capture_output=True,
            check=False,
            text=True,
        )

    def assert_rejected(
        self,
        mutation: Callable[[Path], None],
        expected_reason: str,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            candidate = Path(temporary_directory) / "repository"
            shutil.copytree(REPOSITORY_ROOT, candidate)
            mutation(candidate)
            result = self.run_checker(candidate)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(expected_reason, result.stdout)

    def test_known_good_repository_is_accepted(self) -> None:
        result = self.run_checker(REPOSITORY_ROOT)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("INSTRUCTION_ROUTING: PASS", result.stdout)

    def test_nested_instruction_file_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            shutil.copyfile(root / "AGENTS.md", root / "authority" / "AGENTS.md")

        self.assert_rejected(mutate, "implicit instruction precedence detected")

    def test_broken_route_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            (root / "authority" / "SECURITY.md").rename(
                root / "authority" / "SECURITY.missing"
            )

        self.assert_rejected(mutate, "broken route in AGENTS.md")

    def test_redirected_required_route_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            contract = root / "AGENTS.md"
            text = contract.read_text(encoding="utf-8")
            contract.write_text(
                text.replace(
                    "(authority/SECURITY.md)",
                    "(AGENTS.md)",
                    1,
                ),
                encoding="utf-8",
            )

        self.assert_rejected(mutate, "route destination mismatch in AGENTS.md")

    def test_redirected_architecture_route_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            architecture = root / "ARCHITECTURE.md"
            text = architecture.read_text(encoding="utf-8")
            architecture.write_text(
                text.replace(
                    "(docs/specs/problem-to-retained-revenue-operating-system.md)",
                    "(AGENTS.md)",
                    1,
                ),
                encoding="utf-8",
            )

        self.assert_rejected(
            mutate,
            "route destination mismatch in ARCHITECTURE.md",
        )

    def test_redirected_workflow_route_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            workflow = root / "workflows" / "implementation" / "CONTEXT.md"
            text = workflow.read_text(encoding="utf-8")
            workflow.write_text(
                text.replace(
                    "(01-scout/CONTEXT.md)",
                    "(02-plan/CONTEXT.md)",
                    1,
                ),
                encoding="utf-8",
            )

        self.assert_rejected(
            mutate,
            "route destination mismatch in workflows/implementation/CONTEXT.md",
        )

    def test_out_of_repository_route_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            outside_target = root.parent / "outside.md"
            outside_target.write_text("outside", encoding="utf-8")
            contract = root / "AGENTS.md"
            text = contract.read_text(encoding="utf-8")
            contract.write_text(
                text.replace(
                    "(authority/SECURITY.md)",
                    "(../outside.md)",
                    1,
                ),
                encoding="utf-8",
            )

        self.assert_rejected(mutate, "route outside repository in AGENTS.md")

    def test_stage_order_change_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            stages = root / "workflows" / "implementation"
            (stages / "03-build").rename(stages / "06-build")

        self.assert_rejected(mutate, "stage order mismatch")

    def test_missing_stage_heading_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            contract = (
                root
                / "workflows"
                / "implementation"
                / "04-test"
                / "CONTEXT.md"
            )
            text = contract.read_text(encoding="utf-8")
            contract.write_text(
                text.replace("## Verification\n", "", 1),
                encoding="utf-8",
            )

        self.assert_rejected(mutate, "missing heading: ## Verification")

    def test_missing_root_invariant_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            contract = root / "AGENTS.md"
            text = contract.read_text(encoding="utf-8")
            contract.write_text(
                text.replace("- `MODEL != AUTHORITY`\n", "", 1),
                encoding="utf-8",
            )

        self.assert_rejected(mutate, "missing invariant: MODEL != AUTHORITY")

    def test_business_stage_change_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            specification = (
                root
                / "docs"
                / "specs"
                / "problem-to-retained-revenue-operating-system.md"
            )
            text = specification.read_text(encoding="utf-8")
            specification.write_text(
                text.replace(
                    "| 6 | Demand Generation |",
                    "| 6 | Lead Generation |",
                    1,
                ),
                encoding="utf-8",
            )

        self.assert_rejected(mutate, "business stage order mismatch")

    def test_business_return_path_change_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            specification = (
                root
                / "docs"
                / "specs"
                / "problem-to-retained-revenue-operating-system.md"
            )
            text = specification.read_text(encoding="utf-8")
            specification.write_text(
                text.replace("Stage 11 -> Stage 0 -> Stage 1", "Stage 11 -> Stage 1"),
                encoding="utf-8",
            )

        self.assert_rejected(mutate, "missing: normalized return path")

    def test_business_canonical_return_sequence_bypass_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            specification = (
                root
                / "docs"
                / "specs"
                / "problem-to-retained-revenue-operating-system.md"
            )
            text = specification.read_text(encoding="utf-8")
            specification.write_text(
                text.replace(
                    "  -> Stage 0 Objective Definition revalidation\n"
                    "  -> Stage 1 Problem Scouting",
                    "  -> Stage 1 Problem Scouting",
                    1,
                ),
                encoding="utf-8",
            )

        self.assert_rejected(mutate, "business canonical sequence mismatch")

    def test_closed_exit_success_conflation_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            specification = (
                root
                / "docs"
                / "specs"
                / "problem-to-retained-revenue-operating-system.md"
            )
            text = specification.read_text(encoding="utf-8")
            specification.write_text(
                text.replace(
                    "This closes the cycle but is not retained-revenue success.",
                    "This closes the cycle as retained-revenue success.",
                    1,
                ),
                encoding="utf-8",
            )

        self.assert_rejected(mutate, "missing: closed-exit distinction")

    def test_software_value_overclaim_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            specification = (
                root
                / "docs"
                / "specs"
                / "problem-to-retained-revenue-operating-system.md"
            )
            text = specification.read_text(encoding="utf-8")
            specification.write_text(
                text.replace(
                    "cannot claim target behavior change",
                    "can claim target behavior change",
                    1,
                ),
                encoding="utf-8",
            )

        self.assert_rejected(mutate, "missing: software-delivery boundary")


if __name__ == "__main__":
    unittest.main()

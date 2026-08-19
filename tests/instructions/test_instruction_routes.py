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


if __name__ == "__main__":
    unittest.main()

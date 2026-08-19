from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = REPOSITORY_ROOT / "scripts" / "verify_evidence_manifest.py"


class EvidenceManifestVerifierTest(unittest.TestCase):
    def run_verifier(self, manifest: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, CHECKER_PATH.as_posix(), manifest.as_posix()],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            check=False,
            text=True,
        )

    def fixture(self, digest: str | None = None) -> tuple[Path, tempfile.TemporaryDirectory[str]]:
        temporary_directory = tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT)
        root = Path(temporary_directory.name)
        payload = root / "payload.txt"
        payload.write_text("verified evidence\n", encoding="utf-8")
        expected_digest = digest or hashlib.sha256(payload.read_bytes()).hexdigest()
        manifest = root / "evidence-manifest.json"
        manifest.write_text(
            json.dumps(
                {
                    "inputs": [
                        {"path": "payload.txt", "sha256": expected_digest}
                    ],
                    "produced_artifacts": [],
                    "executions": [],
                }
            ),
            encoding="utf-8",
        )
        return manifest, temporary_directory

    def test_known_good_manifest_is_accepted(self) -> None:
        manifest, temporary_directory = self.fixture()
        with temporary_directory:
            result = self.run_verifier(manifest)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("EVIDENCE_MANIFEST: PASS", result.stdout)

    def test_digest_mismatch_is_rejected(self) -> None:
        manifest, temporary_directory = self.fixture("0" * 64)
        with temporary_directory:
            result = self.run_verifier(manifest)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("artifact digest mismatch", result.stdout)

    def test_malformed_digest_is_rejected(self) -> None:
        manifest, temporary_directory = self.fixture("not-a-digest")
        with temporary_directory:
            result = self.run_verifier(manifest)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("invalid SHA-256", result.stdout)

    def test_missing_artifact_is_rejected(self) -> None:
        manifest, temporary_directory = self.fixture()
        with temporary_directory:
            Path(temporary_directory.name, "payload.txt").unlink()
            result = self.run_verifier(manifest)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("artifact does not exist", result.stdout)

    def test_repository_escape_is_rejected(self) -> None:
        manifest, temporary_directory = self.fixture()
        with temporary_directory:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            data["inputs"][0]["path"] = "../../outside.txt"
            manifest.write_text(json.dumps(data), encoding="utf-8")
            result = self.run_verifier(manifest)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("artifact outside repository", result.stdout)

    def test_absolute_artifact_path_is_rejected(self) -> None:
        manifest, temporary_directory = self.fixture()
        with temporary_directory:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            data["inputs"][0]["path"] = "C:/repository/evidence.txt"
            manifest.write_text(json.dumps(data), encoding="utf-8")
            result = self.run_verifier(manifest)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("absolute artifact path", result.stdout)

    def test_empty_manifest_is_rejected(self) -> None:
        manifest, temporary_directory = self.fixture()
        with temporary_directory:
            manifest.write_text("{}", encoding="utf-8")
            result = self.run_verifier(manifest)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("manifest contains no artifact declarations", result.stdout)


if __name__ == "__main__":
    unittest.main()

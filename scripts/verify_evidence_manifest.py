#!/usr/bin/env python3
"""Verify repository evidence-manifest artifact digests."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Iterable
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_declarations(manifest: dict[str, Any]) -> Iterable[dict[str, Any]]:
    yield from manifest.get("inputs", [])
    yield from manifest.get("produced_artifacts", [])
    for execution in manifest.get("executions", []):
        yield execution.get("stdout", {})
    for diagnostic in manifest.get("diagnostics", []):
        yield diagnostic.get("raw_output", {})


def verify_manifest(manifest_path: Path) -> tuple[str, ...]:
    errors: list[str] = []
    try:
        manifest_path = manifest_path.resolve(strict=True)
        manifest_path.relative_to(ROOT)
    except FileNotFoundError:
        return (f"manifest does not exist: {manifest_path}",)
    except ValueError:
        return (f"manifest outside repository: {manifest_path}",)

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return (f"manifest is not valid UTF-8 JSON: {error}",)
    if not isinstance(manifest, dict):
        return ("manifest root must be an object",)

    declaration_count = 0
    for declaration in artifact_declarations(manifest):
        declaration_count += 1
        if not isinstance(declaration, dict):
            errors.append(f"artifact declaration {declaration_count} is not an object")
            continue
        path_text = declaration.get("path")
        expected_digest = declaration.get("sha256")
        if not isinstance(path_text, str) or not path_text:
            errors.append(f"artifact declaration {declaration_count} missing path")
            continue
        if not isinstance(expected_digest, str) or SHA256_PATTERN.fullmatch(
            expected_digest
        ) is None:
            errors.append(f"invalid SHA-256 for {path_text}")
            continue

        declared_path = Path(path_text)
        if (
            PurePosixPath(path_text).is_absolute()
            or PureWindowsPath(path_text).is_absolute()
        ):
            errors.append(f"absolute artifact path: {path_text}")
            continue
        resolved_path = (manifest_path.parent / declared_path).resolve()
        try:
            resolved_path.relative_to(ROOT)
        except ValueError:
            errors.append(f"artifact outside repository: {path_text}")
            continue
        if not resolved_path.is_file():
            errors.append(f"artifact does not exist: {path_text}")
            continue

        actual_digest = sha256(resolved_path)
        if actual_digest != expected_digest:
            errors.append(
                f"artifact digest mismatch: {path_text}; "
                f"expected={expected_digest}; actual={actual_digest}"
            )

    if declaration_count == 0:
        errors.append("manifest contains no artifact declarations")
    return tuple(errors)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    arguments = parser.parse_args()

    errors = verify_manifest(arguments.manifest)
    if errors:
        print("EVIDENCE_MANIFEST: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    manifest = json.loads(arguments.manifest.read_text(encoding="utf-8"))
    checked_artifacts = sum(1 for _ in artifact_declarations(manifest))
    print("EVIDENCE_MANIFEST: PASS")
    print(f"manifest={arguments.manifest.as_posix()}")
    print(f"checked_artifacts={checked_artifacts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

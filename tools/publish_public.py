#!/usr/bin/env python3
"""Publish the reviewed election wiki into the Quartz content directory.

This script deliberately treats the private Obsidian vault as the source of truth.
It copies an allowlisted subset into a clean output directory and refuses to publish
obvious local paths or credential-like material.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Iterable


class PublicationError(RuntimeError):
    pass


GROUPS = ("races", "entities", "sources")
META_FILES = ("about.md", "changelog.md")
ROOT_FILES = ("index.md",)

SECRET_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("local user path", re.compile(r"/Users/[A-Za-z0-9._-]+/")),
    ("private vault name", re.compile(r"Levi['’]s Vault")),
    ("API key assignment", re.compile(r"(?i)\bapi[_ -]?key\b\s*[:=]")),
    (
        "credential assignment",
        re.compile(
            r"(?i)\b(?:access[_ -]?token|token|password|secret(?:[_ -]?key)?)\b"
            r"\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{8,}"
        ),
    ),
    (".env reference", re.compile(r"(?i)(?:^|[\s`/])\.env(?:[\s`/.\n]|$)")),
    ("private key material", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("known token format", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})\b")),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", required=True, type=Path, help="Private Obsidian vault path")
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Quartz content directory to recreate",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).resolve().with_name("publication-manifest.json"),
        help="Publication manifest JSON path",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PublicationError(f"manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PublicationError(f"invalid manifest JSON: {path}: {exc}") from exc


def resolve_directory(path: Path, label: str) -> Path:
    path = path.expanduser().resolve()
    if not path.is_dir():
        raise PublicationError(f"{label} directory not found: {path}")
    return path


def validate_output_path(output: Path, vault: Path) -> Path:
    output = output.expanduser().resolve()
    if output in {Path("/"), Path.home().resolve(), vault}:
        raise PublicationError(f"refusing to publish to unsafe output directory: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    return output


def create_staging_directory(output: Path) -> Path:
    return Path(tempfile.mkdtemp(prefix=f".{output.name}.staging-", dir=output.parent))


def replace_output(staging: Path, output: Path) -> None:
    """Replace the public tree only after the staged export has passed all checks."""
    backup = output.with_name(f".{output.name}.backup-{uuid.uuid4().hex}")
    previous_output_exists = output.exists()
    try:
        if previous_output_exists:
            output.rename(backup)
        staging.rename(output)
    except OSError as exc:
        if previous_output_exists and backup.exists() and not output.exists():
            backup.rename(output)
        raise PublicationError(f"could not replace public output directory: {exc}") from exc
    else:
        if backup.exists():
            shutil.rmtree(backup)


def normalize_public_markdown(text: str) -> str:
    """Add Quartz's date field without changing the canonical vault note."""
    if not text.startswith("---\n"):
        return text
    frontmatter_end = text.find("\n---\n", 4)
    if frontmatter_end == -1:
        return text

    frontmatter = text[:frontmatter_end]
    if re.search(r"(?m)^modified\s*:", frontmatter):
        return text
    match = re.search(r"(?m)^last_updated\s*:\s*(.+)$", frontmatter)
    if match is None:
        return text

    insertion = f"\nmodified: {match.group(1)}"
    return text[:frontmatter_end] + insertion + text[frontmatter_end:]


def copy_markdown_tree(source: Path, destination: Path) -> list[Path]:
    if not source.is_dir():
        raise PublicationError(f"required source directory not found: {source}")
    copied: list[Path] = []
    for source_file in sorted(source.rglob("*.md")):
        relative = source_file.relative_to(source)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(normalize_public_markdown(source_file.read_text(encoding="utf-8")), encoding="utf-8")
        copied.append(target)
    return copied


def copy_required_file(source: Path, target: Path) -> Path:
    if not source.is_file():
        raise PublicationError(f"required source file not found: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(normalize_public_markdown(source.read_text(encoding="utf-8")), encoding="utf-8")
    return target


def find_findings(content_root: Path, allowlist: Iterable[str]) -> list[str]:
    findings: list[str] = []
    allowlist = tuple(allowlist)
    for path in sorted(content_root.rglob("*.md")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if any(item in line for item in allowlist):
                continue
            for label, rule in SECRET_RULES:
                if rule.search(line):
                    relative = path.relative_to(content_root)
                    findings.append(f"{relative}:{line_number}: {label}")
    return findings


def verify_manifest(content_root: Path, manifest: dict) -> dict[str, int]:
    counts: dict[str, int] = {}
    for group in GROUPS:
        counts[group] = len(list((content_root / "pages" / group).rglob("*.md")))
    counts["meta"] = sum((content_root / name).is_file() for name in META_FILES)
    counts["root"] = sum((content_root / name).is_file() for name in ROOT_FILES)
    counts["total"] = len(list(content_root.rglob("*.md")))

    expected_groups = manifest.get("groups", {})
    for group in GROUPS:
        expected = expected_groups.get(group)
        if expected is not None and counts[group] != expected:
            raise PublicationError(f"manifest mismatch for {group}: expected {expected}, got {counts[group]}")

    expected_meta = len(manifest.get("meta_files", list(META_FILES)))
    if counts["meta"] != expected_meta:
        raise PublicationError(f"manifest mismatch for meta files: expected {expected_meta}, got {counts['meta']}")

    expected_root = len(manifest.get("root_files", list(ROOT_FILES)))
    if counts["root"] != expected_root:
        raise PublicationError(f"manifest mismatch for root files: expected {expected_root}, got {counts['root']}")

    expected_total = manifest.get("total_markdown_files")
    if expected_total is not None and counts["total"] != expected_total:
        raise PublicationError(f"manifest mismatch for total Markdown files: expected {expected_total}, got {counts['total']}")

    return counts


def publish(vault: Path, output: Path, manifest_path: Path) -> dict:
    vault = resolve_directory(vault, "vault")
    output = validate_output_path(output, vault)
    manifest = load_manifest(manifest_path.resolve())
    staging = create_staging_directory(output)

    try:
        copied: list[Path] = []
        copied.append(copy_required_file(vault / "index.md", staging / "index.md"))
        for group in GROUPS:
            copied.extend(copy_markdown_tree(vault / "pages" / group, staging / "pages" / group))
        for name in META_FILES:
            copied.append(copy_required_file(vault / "publish" / name, staging / name))

        findings = find_findings(staging, manifest.get("secret_scan_allowlist", []))
        if findings:
            raise PublicationError("publication safety scan failed:\n" + "\n".join(findings))

        counts = verify_manifest(staging, manifest)
        replace_output(staging, output)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise

    return {"copied_files": len(copied), **counts}


def main() -> int:
    args = parse_args()
    try:
        summary = publish(args.vault, args.output, args.manifest)
    except PublicationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("Public publication completed")
    print(f"  output: {args.output.expanduser().resolve()}")
    print(f"  copied Markdown files: {summary['copied_files']}")
    print(f"  races: {summary['races']}")
    print(f"  entities: {summary['entities']}")
    print(f"  sources: {summary['sources']}")
    print(f"  meta pages: {summary['meta']}")
    print(f"  total Markdown files: {summary['total']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

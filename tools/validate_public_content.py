#!/usr/bin/env python3
"""Validate the reviewed Markdown exported into Quartz's public content tree.

This validator is intentionally independent of Quartz's renderer. It checks the
publication boundary, frontmatter, internal links, and election-specific
uncertainty markers before a build or deployment is allowed to proceed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from publish_public import SECRET_RULES, load_manifest


class ValidationError(RuntimeError):
    """Raised when public content violates a publication invariant."""


META_FILES = ("about.md", "changelog.md")
ROOT_FILES = ("index.md",)
GROUPS = ("races", "entities", "sources")

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$")
SOURCE_URL_RE = re.compile(r"^\s*-\s*[\"']?(https?://[^\"']+)[\"']?\s*$")

PUBLIC_CONTENT_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "excluded Obsidian/private file reference",
        re.compile(r"(?i)(?:^|[\s`/])(?:AGENTS\.md|log\.md|\.obsidian(?:[/`.)\s]|$)|raw/)", re.MULTILINE),
    ),
    ("skill-pruning marker", re.compile(r"\[SKILL_PRUNED\]")),
    (
        "tool transcript marker",
        re.compile(
            r"(?i)<untrusted_tool_result>|(?:browser_(?:navigate|snapshot|console|click|type)|tool_call\(|multi_tool_use\.)"
        ),
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content", type=Path, help="Quartz public content directory")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).resolve().with_name("publication-manifest.json"),
        help="Publication manifest JSON path",
    )
    return parser.parse_args()


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValidationError("frontmatter starts with '---' but has no closing delimiter")

    values: dict[str, str] = {}
    source_urls: list[str] = []
    for line in text[4:end].splitlines():
        match = FRONTMATTER_KEY_RE.match(line)
        if match:
            values[match.group(1)] = match.group(2).strip()
        source_match = SOURCE_URL_RE.match(line)
        if source_match:
            source_urls.append(source_match.group(1))
    return values, source_urls


def public_files(content_root: Path) -> list[Path]:
    if not content_root.is_dir():
        raise ValidationError(f"content directory not found: {content_root}")

    files = sorted(path for path in content_root.rglob("*") if path.is_file())
    errors: list[str] = []
    for path in files:
        if path.is_symlink():
            errors.append(f"symlink is not allowed: {path.relative_to(content_root)}")
        elif path.suffix.lower() != ".md":
            errors.append(f"unapproved public file type: {path.relative_to(content_root)}")
    if errors:
        raise ValidationError("\n".join(errors))
    return files


def scan_content(files: list[Path], content_root: Path) -> list[str]:
    findings: list[str] = []
    rules = SECRET_RULES + PUBLIC_CONTENT_RULES
    for path in files:
        relative = path.relative_to(content_root)
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError as exc:
            findings.append(f"{relative}: not valid UTF-8: {exc}")
            continue

        for line_number, line in enumerate(lines, start=1):
            for label, rule in rules:
                if rule.search(line):
                    findings.append(f"{relative}:{line_number}: {label}")
    return findings


def resolve_public_target(content_root: Path, source: Path, target: str) -> Path | None:
    target = target.strip()
    if not target or target.startswith(("#", "http://", "https://", "mailto:", "data:")):
        return None

    if target.startswith("/"):
        candidate = (content_root / target.lstrip("/")).resolve()
    else:
        candidate = (source.parent / target).resolve()

    if candidate.suffix != ".md":
        candidate = candidate.with_suffix(".md")
    return candidate


def check_links(files: list[Path], content_root: Path) -> tuple[int, int, list[str]]:
    wikilink_count = 0
    markdown_count = 0
    findings: list[str] = []

    for source in files:
        relative = source.relative_to(content_root)
        text = source.read_text(encoding="utf-8")

        for raw in WIKILINK_RE.findall(text):
            target = raw.split("|", 1)[0].split("#", 1)[0].strip()
            if not target:
                continue
            wikilink_count += 1
            candidate = (content_root / (target if target.endswith(".md") else f"{target}.md")).resolve()
            try:
                candidate.relative_to(content_root.resolve())
            except ValueError:
                findings.append(f"{relative}: wikilink escapes public content: {target}")
                continue
            if not candidate.is_file():
                findings.append(f"{relative}: broken wikilink target: {target}")

        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or target.startswith(("#", "http://", "https://", "mailto:", "data:")):
                continue
            markdown_count += 1
            candidate = resolve_public_target(content_root, source, target)
            if candidate is None:
                continue
            try:
                candidate.relative_to(content_root.resolve())
            except ValueError:
                findings.append(f"{relative}: Markdown link escapes public content: {target}")
                continue
            if not candidate.is_file():
                findings.append(f"{relative}: broken Markdown link target: {target}")

    return wikilink_count, markdown_count, findings


def check_frontmatter(files: list[Path], content_root: Path) -> list[str]:
    findings: list[str] = []
    for path in files:
        relative = path.relative_to(content_root)
        try:
            parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
        except ValidationError as exc:
            findings.append(f"{relative}: {exc}")
            continue
        if parsed is None:
            continue

        values, source_urls = parsed
        for required_key in ("last_updated", "confidence", "sources"):
            if required_key not in values:
                findings.append(f"{relative}: frontmatter missing {required_key}")
            elif required_key != "sources" and not values[required_key]:
                findings.append(f"{relative}: frontmatter has empty {required_key}")

        source_count = values.get("source_count")
        if source_count is not None:
            try:
                expected = int(source_count)
            except ValueError:
                findings.append(f"{relative}: source_count is not an integer: {source_count}")
            else:
                if expected != len(source_urls):
                    findings.append(
                        f"{relative}: source_count mismatch: declared {expected}, found {len(source_urls)} URLs"
                    )
    return findings


def check_manifest(files: list[Path], content_root: Path, manifest: dict) -> list[str]:
    counts = {
        "races": len(list((content_root / "pages" / "races").glob("*.md"))),
        "entities": len(list((content_root / "pages" / "entities").glob("*.md"))),
        "sources": len(list((content_root / "pages" / "sources").glob("*.md"))),
        "meta": sum((content_root / name).is_file() for name in META_FILES),
        "root": sum((content_root / name).is_file() for name in ROOT_FILES),
        "total": len(files),
    }
    findings: list[str] = []
    expected_groups = manifest.get("groups", {})
    for group in GROUPS:
        expected = expected_groups.get(group)
        if expected is not None and counts[group] != expected:
            findings.append(f"manifest mismatch for {group}: expected {expected}, got {counts[group]}")

    expected_meta = len(manifest.get("meta_files", META_FILES))
    if counts["meta"] != expected_meta:
        findings.append(f"manifest mismatch for meta files: expected {expected_meta}, got {counts['meta']}")

    expected_root = len(manifest.get("root_files", ROOT_FILES))
    if counts["root"] != expected_root:
        findings.append(f"manifest mismatch for root files: expected {expected_root}, got {counts['root']}")

    expected_total = manifest.get("total_markdown_files")
    if expected_total is not None and counts["total"] != expected_total:
        findings.append(f"manifest mismatch for total Markdown files: expected {expected_total}, got {counts['total']}")
    return findings


def check_governor_dispute(content_root: Path) -> list[str]:
    path = content_root / "pages" / "races" / "governor-2026.md"
    if not path.is_file():
        return ["required Governor page is missing"]
    if "[disputed]" not in path.read_text(encoding="utf-8"):
        return ["Governor result discrepancy lost its required [disputed] marker"]
    return []


def validate(content_root: Path, manifest_path: Path) -> dict[str, int]:
    try:
        manifest = load_manifest(manifest_path.resolve())
    except Exception as exc:  # argparse-facing error, not a library API
        raise ValidationError(str(exc)) from exc

    files = public_files(content_root)
    findings = []
    findings.extend(scan_content(files, content_root))
    findings.extend(check_frontmatter(files, content_root))
    findings.extend(check_manifest(files, content_root, manifest))
    findings.extend(check_governor_dispute(content_root))
    wikilinks, markdown_links, link_findings = check_links(files, content_root)
    findings.extend(link_findings)
    if findings:
        raise ValidationError("\n".join(findings))

    return {
        "markdown_files": len(files),
        "wikilinks": wikilinks,
        "markdown_internal_links": markdown_links,
    }


def main() -> int:
    args = parse_args()
    content_root = args.content.expanduser().resolve()
    try:
        summary = validate(content_root, args.manifest)
    except ValidationError as exc:
        print(f"ERROR: public content validation failed\n{exc}", file=sys.stderr)
        return 1

    print("Public content validation passed")
    print(f"  Markdown files: {summary['markdown_files']}")
    print(f"  Obsidian wikilinks: {summary['wikilinks']}")
    print(f"  Relative Markdown links: {summary['markdown_internal_links']}")
    print("  Broken internal links: 0")
    print("  Governor [disputed] marker: present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

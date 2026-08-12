"""Regression tests for the controlled public-content publisher."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_DIRECTORY = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS_DIRECTORY))

from publish_public import PublicationError, publish


class PublishPublicTests(unittest.TestCase):
    def create_vault(self, root: Path, index_text: str = "# Index\n") -> Path:
        vault = root / "vault"
        (vault / "pages" / "races").mkdir(parents=True)
        (vault / "pages" / "entities").mkdir(parents=True)
        (vault / "pages" / "sources").mkdir(parents=True)
        (vault / "publish").mkdir()
        (vault / "index.md").write_text(index_text, encoding="utf-8")
        (vault / "publish" / "about.md").write_text("# About\n", encoding="utf-8")
        (vault / "publish" / "changelog.md").write_text("# Changelog\n", encoding="utf-8")
        return vault

    def write_manifest(self, root: Path) -> Path:
        manifest = root / "manifest.json"
        manifest.write_text(
            json.dumps(
                {
                    "groups": {"races": 0, "entities": 0, "sources": 0},
                    "root_files": ["index.md"],
                    "meta_files": ["about.md", "changelog.md"],
                    "total_markdown_files": 3,
                    "secret_scan_allowlist": [],
                }
            ),
            encoding="utf-8",
        )
        return manifest

    def test_rejected_export_preserves_existing_public_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp_directory:
            root = Path(temp_directory)
            vault = self.create_vault(root, "# Unsafe\n/Users/example/private-note\n")
            manifest = self.write_manifest(root)
            output = root / "content"
            output.mkdir()
            existing = output / "last-known-good.md"
            existing.write_text("keep this public page", encoding="utf-8")

            with self.assertRaises(PublicationError):
                publish(vault, output, manifest)

            self.assertEqual(existing.read_text(encoding="utf-8"), "keep this public page")

    def test_verified_export_replaces_existing_public_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp_directory:
            root = Path(temp_directory)
            vault = self.create_vault(root, "---\nlast_updated: 2026-08-11\n---\n# New index\n")
            manifest = self.write_manifest(root)
            output = root / "content"
            output.mkdir()
            (output / "stale.md").write_text("remove me", encoding="utf-8")

            summary = publish(vault, output, manifest)

            self.assertEqual(summary["copied_files"], 3)
            self.assertFalse((output / "stale.md").exists())
            index = (output / "index.md").read_text(encoding="utf-8")
            self.assertIn("# New index", index)
            self.assertIn("modified: 2026-08-11", index)


if __name__ == "__main__":
    unittest.main()

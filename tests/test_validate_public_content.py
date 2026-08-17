"""Regression tests for the public-content validator's Quartz-aware link checks."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_DIRECTORY = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS_DIRECTORY))

from validate_public_content import check_links


def make_file(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class ValidatorLinkCheckTests(unittest.TestCase):
    def test_table_cell_parent_link_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_directory:
            root = Path(temp_directory)
            make_file(root, "pages/entities/collin-alexander.md", "# Target\n")
            race = make_file(
                root,
                "pages/races/county-council-2026.md",
                "| 7 | [Collin Alexander](../entities/collin-alexander) |\n",
            )

            _, _, findings = check_links([race], root)

            self.assertTrue(
                any("table-cell Markdown link must be content-root relative" in f for f in findings),
                findings,
            )

    def test_table_cell_content_root_link_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_directory:
            root = Path(temp_directory)
            make_file(root, "pages/entities/chris-sullivan.md", "# Target\n")
            race = make_file(
                root,
                "pages/races/county-council-2026.md",
                "| 1 | [Chris Sullivan](pages/entities/chris-sullivan) |\n",
            )

            _, _, findings = check_links([race], root)

            self.assertEqual([], findings)

    def test_table_cell_wikilink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_directory:
            root = Path(temp_directory)
            make_file(root, "pages/entities/darline-graham.md", "# Target\n")
            race = make_file(
                root,
                "pages/races/senate-2026.md",
                "| [[pages/entities/darline-graham|Darline Graham]] | 109,881 |\n",
            )

            _, _, findings = check_links([race], root)

            self.assertTrue(
                any("table-cell wikilink renders literally" in f for f in findings),
                findings,
            )

    def test_paragraph_parent_link_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_directory:
            root = Path(temp_directory)
            make_file(root, "pages/entities/collin-alexander.md", "# Target\n")
            race = make_file(
                root,
                "pages/races/county-council-2026.md",
                "See [Collin Alexander](../entities/collin-alexander) in the field.\n",
            )

            _, _, findings = check_links([race], root)

            self.assertEqual([], findings)

    def test_table_cell_broken_target_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as temp_directory:
            root = Path(temp_directory)
            race = make_file(
                root,
                "pages/races/county-council-2026.md",
                "| 1 | [Nobody](pages/entities/nobody) |\n",
            )

            _, _, findings = check_links([race], root)

            self.assertTrue(any("broken Markdown link target" in f for f in findings), findings)


if __name__ == "__main__":
    unittest.main()

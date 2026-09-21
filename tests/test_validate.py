"""Regression cases for installable metadata and self-contained references."""

import re
import tempfile
import unittest
from pathlib import Path

from scripts.validate import ROOT, SKILL, validate


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name) / "example-skill"
        self.skill.mkdir()
        (self.skill / "LICENSE").write_text("MIT license fixture\n", encoding="utf-8")

    def write_skill(self, name="example-skill", description="Review a change.", body="# Instructions\n"):
        (self.skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\nlicense: MIT\n---\n{body}",
            encoding="utf-8",
        )

    def test_complete_portable_package(self):
        self.write_skill(body="See [guide](references/guide.md).")
        (self.skill / "references").mkdir()
        (self.skill / "references" / "guide.md").write_text("# Guide\n", encoding="utf-8")
        self.assertEqual(validate(self.skill), [])

    def test_real_installable_folder_is_self_contained(self):
        self.assertEqual(validate(SKILL), [])
        for relative in (
            "SKILL.md",
            "LICENSE",
            "agents/openai.yaml",
            "scripts/review_evidence.py",
            "references/independent-review.md",
            "references/review-evidence.md",
            "assets/reviewer-prompt.md",
            "assets/review-report-template.json",
            "assets/pel-reviewer.toml",
        ):
            self.assertTrue((SKILL / relative).is_file(), relative)
        self.assertNotEqual(SKILL, ROOT)

    def test_installable_folder_contains_no_personal_home_paths(self):
        markers = ("/Users/", "C:\\Users\\")
        for path in SKILL.rglob("*"):
            if path.is_file():
                with self.subTest(path=path.relative_to(SKILL)):
                    text = path.read_text(encoding="utf-8")
                    self.assertFalse(any(marker in text for marker in markers))

    def test_ci_actions_use_immutable_revisions(self):
        workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
        action_uses = re.findall(r"uses:\s+([^\s#]+)", workflow)
        self.assertTrue(action_uses)
        for action in action_uses:
            with self.subTest(action=action):
                self.assertRegex(action, r"^[^@]+@[0-9a-f]{40}$")

    def test_missing_reference_is_rejected(self):
        self.write_skill(body="See [guide](references/missing.md).")
        self.assertTrue(any("missing linked file" in error for error in validate(self.skill)))

    def test_reference_outside_installable_package_is_rejected(self):
        (self.skill.parent / "private.md").write_text("Private", encoding="utf-8")
        self.write_skill(body="See [guide](../private.md).")
        self.assertTrue(any("escapes package" in error for error in validate(self.skill)))

    def test_invalid_names_are_rejected(self):
        for name in ["other-name", "Example", "bad--name", "''", "123"]:
            with self.subTest(name=name):
                self.write_skill(name=name)
                self.assertTrue(any("Name must" in error for error in validate(self.skill)))

    def test_empty_or_nontext_description_is_rejected(self):
        for description in ["''", "123", "[]", "x" * 1025]:
            with self.subTest(description=description[:30]):
                self.write_skill(description=description)
                self.assertTrue(any("Description must" in error for error in validate(self.skill)))

    def test_invalid_yaml_and_nonmapping_frontmatter_are_rejected(self):
        for frontmatter in ["name: [", "- name", "null"]:
            with self.subTest(frontmatter=frontmatter):
                (self.skill / "SKILL.md").write_text(f"---\n{frontmatter}\n---\nBody\n", encoding="utf-8")
                self.assertTrue(validate(self.skill))

    def test_missing_license_is_rejected(self):
        self.write_skill()
        (self.skill / "LICENSE").unlink()
        self.assertTrue(any("bundle LICENSE" in error for error in validate(self.skill)))

    def test_web_links_are_not_treated_as_files(self):
        self.write_skill(body="See [docs](https://example.com/docs) and [top](#instructions).")
        self.assertEqual(validate(self.skill), [])


if __name__ == "__main__":
    unittest.main()

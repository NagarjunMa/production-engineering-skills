#!/usr/bin/env python3
"""Check this repository's skill packaging, not agent behavior or code quality."""

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "production-engineering-loop"


def validate(skill: Path) -> list[str]:
    """Validate the metadata subset and inline file links used by this package."""
    errors = []
    skill = skill.resolve()
    try:
        content = (skill / "SKILL.md").read_text(encoding="utf-8")
    except OSError as exc:
        return [f"Cannot read SKILL.md: {exc}"]
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", content, re.DOTALL)
    if not match:
        return ["SKILL.md requires YAML frontmatter and a Markdown body"]
    try:
        metadata = yaml.safe_load(match[1])
    except yaml.YAMLError as exc:
        return [f"Invalid YAML: {exc}"]
    if not isinstance(metadata, dict):
        return ["Frontmatter must be a mapping"]
    name = metadata.get("name")
    if not isinstance(name, str) or not re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*", name
    ) or len(name) > 64 or name != skill.name:
        errors.append("Name must be lowercase hyphenated text matching its folder (1–64 characters)")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append("Description must be nonempty text, at most 1024 characters")
    compatibility = metadata.get("compatibility")
    if compatibility is not None and (
        not isinstance(compatibility, str)
        or not compatibility.strip()
        or len(compatibility) > 500
    ):
        errors.append("compatibility must be nonempty text, at most 500 characters")
    if not match[2].strip():
        errors.append("Skill body is empty")
    extra = metadata.get("metadata", {})
    if not isinstance(extra, dict) or any(
        not isinstance(key, str) or not isinstance(value, str)
        for key, value in extra.items()
    ):
        errors.append("metadata must map string keys to string values")
    if metadata.get("license") != "MIT" or not (skill / "LICENSE").is_file():
        errors.append("This package must declare MIT and bundle LICENSE")

    # This project uses simple inline Markdown links, not reference-style links.
    # Check that every linked local file travels with the installed package.
    for document in sorted(skill.rglob("*.md")):
        for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", document.read_text(encoding="utf-8")):
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            path = (document.parent / unquote(url.path)).resolve()
            if not path.is_relative_to(skill):
                errors.append(f"{document.relative_to(skill)}: link escapes package: {target}")
            elif not path.is_file():
                errors.append(f"{document.relative_to(skill)}: missing linked file: {target}")
    return errors


def main() -> int:
    errors = validate(SKILL)
    bundled_license = SKILL / "LICENSE"
    if bundled_license.is_file() and bundled_license.read_bytes() != (ROOT / "LICENSE").read_bytes():
        errors.append("Root and bundled licenses differ")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print("PASS: skill metadata, bundled links, and license consistency")
    print("Not evaluated: host runtime discovery, instruction following, or engineering outcomes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

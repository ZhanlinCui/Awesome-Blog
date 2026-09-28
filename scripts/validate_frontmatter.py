#!/usr/bin/env python3
"""Validate SKILL.md YAML frontmatter across the kit.

Offline, Python standard library only (PyYAML is used if available; a small
fallback parser handles the simple key/value + nested-mapping frontmatter used
by this kit so the check can run in minimal environments).

Usage:
    python3 validate_frontmatter.py [--root .]

Exit code: 0 if every SKILL.md passes, 1 otherwise.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_KEYS = ["name", "description", "license"]
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def extract_frontmatter(text: str):
    if not text.startswith("---"):
        return None
    parts = text.split("\n")
    end = None
    for i in range(1, len(parts)):
        if parts[i].strip() == "---":
            end = i
            break
    if end is None:
        return None
    return "\n".join(parts[1:end])


def parse_yaml(blob: str):
    try:
        import yaml  # type: ignore
        return yaml.safe_load(blob)
    except ImportError:
        return _mini_parse(blob)


def _mini_parse(blob: str):
    """Tiny parser for flat 'key: value' lines plus one-level 'metadata:' maps.

    Values are returned as strings; sufficient for presence/format checks.
    """
    data: dict = {}
    in_block = None
    for raw in blob.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        if re.match(r"^\S", raw) and ":" in raw:
            key, _, val = raw.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "":
                data[key] = {}
                in_block = key
            else:
                data[key] = _scalar(val)
                in_block = None
        elif raw.startswith("  ") and ":" in raw and in_block:
            k, _, v = raw.strip().partition(":")
            data[in_block][k.strip()] = _scalar(v.strip())
    return data


def _scalar(v: str):
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def validate(root: Path) -> int:
    skills = sorted(root.glob("skills/*/SKILL.md"))
    if not skills:
        print("ERROR: no skills/*/SKILL.md found under", root)
        return 1
    failures = 0
    for path in skills:
        rel = path.relative_to(root)
        fm_blob = extract_frontmatter(path.read_text(encoding="utf-8"))
        if fm_blob is None:
            print(f"FAIL {rel}: missing or unclosed YAML frontmatter")
            failures += 1
            continue
        try:
            fm = parse_yaml(fm_blob)
            assert isinstance(fm, dict)
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL {rel}: YAML parse error: {exc}")
            failures += 1
            continue
        problems = []
        for key in REQUIRED_KEYS:
            if not fm.get(key):
                problems.append(f"missing required key '{key}'")
        name = fm.get("name")
        if isinstance(name, str):
            if not SLUG_RE.match(name):
                problems.append(f"name '{name}' is not a lowercase kebab-case ASCII slug")
            if name != path.parent.name:
                problems.append(
                    f"name '{name}' does not match directory '{path.parent.name}'"
                )
        desc = fm.get("description")
        if isinstance(desc, str) and len(desc.strip()) < 20:
            problems.append("description is too short to be a useful trigger")
        meta = fm.get("metadata")
        if meta is not None and not isinstance(meta, dict):
            problems.append("metadata must be a mapping")
        if problems:
            failures += 1
            for p in problems:
                print(f"FAIL {rel}: {p}")
        else:
            print(f"PASS {rel} ({name})")
    print(f"\n{len(skills) - failures}/{len(skills)} skill files valid")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="kit root (contains skills/)")
    args = ap.parse_args()
    return validate(Path(args.root).resolve())


if __name__ == "__main__":
    sys.exit(main())

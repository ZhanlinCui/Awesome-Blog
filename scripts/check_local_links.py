#!/usr/bin/env python3
"""Check that every local relative link/image in Markdown files resolves.

Offline; Python standard library only. Remote links (http/https/mailto) and
pure anchor links are skipped.

Negative-test fixtures (directories named "fixtures") are skipped when
scanning a whole repository, since they intentionally reference missing
targets. Pointing --root directly at a fixtures directory still checks them.

Usage:
    python3 check_local_links.py [--root .] [--glob '**/*.md']
Exit code: 0 when all local targets exist, 1 otherwise.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

LINK_RE = re.compile(r"(!?\[[^\]]*\]\(([^)]+)\))")


def strip_anchor(target: str) -> str:
    return target.split("#", 1)[0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    failures = 0
    checked = 0
    for md in sorted(root.glob("**/*.md")):
        if ".git" in md.parts:
            continue
        # Skip negative-test fixtures (they reference missing targets on
        # purpose), unless the caller pointed --root straight at them.
        if "fixtures" in md.relative_to(root).parts:
            continue
        text = md.read_text(encoding="utf-8")
        for _, raw_target in LINK_RE.findall(text):
            target = raw_target.strip().split()[0] if raw_target.strip() else ""
            if target.startswith(("http://", "https://", "mailto:", "tel:")):
                continue
            if target.startswith("#") or not strip_anchor(target):
                continue
            local = unquote(strip_anchor(target))
            resolved = (md.parent / local).resolve()
            checked += 1
            if not resolved.exists():
                print(f"BROKEN  {md.relative_to(root)} -> {target}")
                failures += 1
    print(f"\n{checked} local links checked, {failures} broken")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

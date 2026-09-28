#!/usr/bin/env python3
"""Pre-delivery (preflight) checks for a local article draft.

Offline, Python standard library only. This gate never opens a browser, never
logs into a platform and never uploads anything. It validates a local
Markdown/HTML deliverable before the author publishes it manually.

Checks:
  - unresolved placeholders / TODO markers
  - research-trace leakage (internal S0xx/C0xx IDs, local absolute paths,
    names of the internal ledger files)
  - forbidden platform-automation vocabulary (login/cookie/credential/
    auto-publish instructions): must be absent from implementation content
  - figure placeholders [图X] and missing local image files
  - empty sections / heading level skips / multiple H1
  - over-the-top clickbait words for Chinese drafts (advisory count)

Usage:
    python3 preflight.py --draft deliverables/final.md
Exit code 0 = no blockers, 1 = blockers found.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

INTERNAL_ID_RE = re.compile(r"(?<![A-Za-z0-9])[SC]\d{3,}(?![0-9])")
PLACEHOLDER_RE = re.compile(
    r"(\[\s*CITATION\s+NEEDED\s*\]|\[\s*需补[^\]]*\]|\bTODO\b|\bFIXME\b|"
    r"\[图\s*\d+[^\]]*\]|\[示意图[^\]]*\])",
    re.IGNORECASE)
LEDGER_NAME_RE = re.compile(
    r"(source_registry|claims_registry|market_assumptions|task_spec)\.csv",
    re.IGNORECASE)
ABS_PATH_RE = re.compile(r"(?<![A-Za-z0-9_])/(?:home|Users|tmp)/\S+")
# implementation-flavored platform automation, not normal prose mentioning publishing
FORBIDDEN_RE = re.compile(
    r"(simulate\s*login|模拟登录|auto[- ]?publish|自动发布|自动上传|"
    r"cookie\s*[:=]|set-cookie|credentials?\s*[:=]\s*\S|"
    r"requests\.post\([^)]*(login|publish|upload)|"
    r"playwright\.|selenium\s|webdriver)",
    re.IGNORECASE)
H_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
IMG_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
CLICKBAIT = ["震惊", "必看", "万字干货", "不看后悔", "颠覆认知", "绝密"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", required=True)
    args = ap.parse_args()
    path = Path(args.draft)
    text = path.read_text(encoding="utf-8")
    blockers, warnings = [], []

    for rx, label in [
        (INTERNAL_ID_RE, "internal research ID leaked into deliverable"),
        (PLACEHOLDER_RE, "unresolved placeholder"),
        (LEDGER_NAME_RE, "internal ledger filename referenced"),
        (ABS_PATH_RE, "local absolute path leaked"),
        (FORBIDDEN_RE, "platform automation/login/credential content (forbidden)"),
    ]:
        for m in rx.finditer(text):
            line_no = text[: m.start()].count("\n") + 1
            snippet = m.group(0)[:60].replace("\n", " ")
            blockers.append(f"L{line_no}: {label}: {snippet!r}")

    # headings
    h1, prev_level = 0, 0
    for i, line in enumerate(text.splitlines(), 1):
        m = H_RE.match(line)
        if not m:
            continue
        level = len(m.group(1))
        if level == 1:
            h1 += 1
        if prev_level and level > prev_level + 1:
            warnings.append(f"L{i}: heading level skip H{prev_level}->H{level}")
        prev_level = level
    if h1 == 0:
        warnings.append("no H1 title found")
    elif h1 > 1:
        blockers.append(f"{h1} H1 headings; exactly one is required")

    # images and local links: local files must exist
    for m in IMG_RE.finditer(text):
        target = m.group(1).strip().split()[0]
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        local = unquote(target.split("#")[0])
        if not local:
            continue
        if not (path.parent / local).resolve().exists():
            blockers.append(f"missing local image/link target: {target}")

    # empty sections (heading immediately followed by heading/EOF)
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if H_RE.match(line):
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if not nxt.strip() or H_RE.match(nxt):
                warnings.append(f"L{i+1}: empty section")

    for word in CLICKBAIT:
        if word in text:
            warnings.append(f"clickbait word present: {word!r}")

    print(f"Preflight: {path}")
    for b in blockers:
        print("BLOCK", b)
    for w in warnings:
        print("WARN ", w)
    print(f"\n{len(blockers)} blocker(s), {len(warnings)} warning(s)")
    if not blockers:
        print("PASS — deliverable is a LOCAL file; the author performs any "
              "platform upload manually.")
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())

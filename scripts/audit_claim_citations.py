#!/usr/bin/env python3
"""Audit claim-to-source citations in a draft against the registries.

Offline, Python standard library only.

Two audit surfaces:
  1. Registry consistency (reuses validate_evidence_ledger rules).
  2. Draft hygiene:
       - internal IDs (S001/C012 style) must NOT appear in a final draft;
       - unfilled placeholders [CITATION NEEDED], [需补, TODO citations are blockers;
       - every inline citation marker like [S007] or (S007) is flagged (research leak);
       - numeric-looking sentences are reported as "manually verify" hints
         (deterministic heuristic, not an LLM judgement).

Usage:
    python3 audit_claim_citations.py --sources source_registry.csv \
        --claims claims_registry.csv --draft deliverables/final.md [--strict-draft]
Exit code 0 = clean, 1 = blockers.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_evidence_ledger import validate  # noqa: E402

INTERNAL_ID_RE = re.compile(r"(?<![A-Za-z0-9])([SC]\d{3,})(?![0-9])")
PLACEHOLDER_RE = re.compile(
    r"(\[\s*CITATION\s+NEEDED\s*\]|\[\s*需补[^\]]*\]|\bTODO\b|\bFIXME\b)",
    re.IGNORECASE)
NUMBER_RE = re.compile(r"[^。.\n]{0,40}\d[\d,\.%]*[^。.\n]{0,40}[。.]")


def audit_draft(path: str):
    text = Path(path).read_text(encoding="utf-8")
    blockers, notes = [], []
    for m in INTERNAL_ID_RE.finditer(text):
        line_no = text[: m.start()].count("\n") + 1
        blockers.append(
            f"draft L{line_no}: internal research ID '{m.group(1)}' must be "
            f"stripped from the deliverable")
    for m in PLACEHOLDER_RE.finditer(text):
        line_no = text[: m.start()].count("\n") + 1
        blockers.append(f"draft L{line_no}: unresolved placeholder {m.group(1)!r}")
    # numeric sentence hint (does not block by itself)
    hits = NUMBER_RE.findall(text)
    if hits:
        notes.append(
            f"draft contains {len(hits)} sentence(s) with numbers; confirm each "
            f"is present in claims_registry with a source (manual step).")
    return blockers, notes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", required=True)
    ap.add_argument("--claims", required=True)
    ap.add_argument("--draft")
    ap.add_argument("--key-claims", default="")
    args = ap.parse_args()

    keys = [x.strip() for x in args.key_claims.split(",") if x.strip()]
    errors, warnings = validate(args.sources, args.claims, keys)
    blockers = list(errors)
    if args.draft:
        d_block, d_notes = audit_draft(args.draft)
        blockers += d_block
        for n in d_notes:
            print("NOTE ", n)
    for w in warnings:
        print("WARN ", w)
    for b in blockers:
        print("BLOCK", b)
    print(f"\n{len(blockers)} blocker(s)")
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())

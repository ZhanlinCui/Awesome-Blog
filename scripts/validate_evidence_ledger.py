#!/usr/bin/env python3
"""Validate the completeness of an evidence ledger (source + claim registries).

Offline, Python standard library only; makes no network or LLM calls.

Inputs are CSV files following templates/source_registry.csv and
templates/claims_registry.csv (see references/evidence-ledger-spec.md).

Checks:
  S1 CSV parses and required columns exist.
  S2 source_id unique, well-formed (S + digits), required cells non-empty.
  S3 URL/retrieval date plausibility when present.
  S4 aggregator rows declare original_producer and reference an existing source.
  C1 claims reference existing sources; calculation refs keep CALC: prefix.
  C2 critical (key) claims have >=2 independent sources unless status allows
     single-source downgrade wording; never silently "verified" on one source.
  C3 status is an allowed value; placeholder claims must contain [需补] markers.

Usage:
    python3 validate_evidence_ledger.py --sources source_registry.csv \
        --claims claims_registry.csv
Exit code 0 = valid, 1 = errors found.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import date

SOURCE_COLS = [
    "source_id", "title", "publisher", "url", "source_type", "retrieval_date",
    "original_producer", "original_source_id", "method", "limitations",
    "accessed_lawfully",
]
CLAIM_COLS = [
    "claim_id", "statement", "claim_type", "source_ids", "independent_sources",
    "status", "disconfirmation", "final_wording",
]
ALLOWED_SOURCE_TYPES = {
    "official_stat", "regulator", "filing", "company_official", "academic",
    "media", "aggregator", "community", "other",
}
ALLOWED_CLAIM_TYPES = {
    "fact", "statistic", "estimate", "calculation", "forecast", "opinion",
    "recommendation",
}
ALLOWED_STATUS = {
    "verified", "contested", "single_source", "refuted", "placeholder",
}
SID_RE = re.compile(r"^S\d{3,}$")
CID_RE = re.compile(r"^C\d{3,}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED_SOURCE_CELLS = ["source_id", "title", "publisher", "source_type",
                         "retrieval_date", "limitations", "accessed_lawfully"]


def read_csv(path: str):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def check_columns(rows, cols, label, errors):
    if not rows:
        errors.append(f"{label}: file is empty")
        return
    missing = [c for c in cols if c not in rows[0]]
    if missing:
        errors.append(f"{label}: missing columns {missing}")


def validate(sources_path: str, claims_path: str, key_claim_ids=None):
    errors, warnings = [], []
    sources = read_csv(sources_path)
    claims = read_csv(claims_path)
    check_columns(sources, SOURCE_COLS, "sources", errors)
    check_columns(claims, CLAIM_COLS, "claims", errors)
    if errors:
        return errors, warnings
    source_ids = {}
    for raw_row in sources:
        row = {k: (v or "") for k, v in raw_row.items() if k is not None}
        sid = row["source_id"].strip()
        if not SID_RE.match(sid):
            errors.append(f"sources: bad source_id '{sid}' (want S + >=3 digits)")
        if sid in source_ids:
            errors.append(f"sources: duplicate source_id {sid}")
        source_ids[sid] = row
        for col in REQUIRED_SOURCE_CELLS:
            if not (row.get(col) or "").strip():
                errors.append(f"sources {sid}: empty required cell '{col}'")
        stype = (row.get("source_type") or "").strip()
        if stype not in ALLOWED_SOURCE_TYPES:
            errors.append(f"sources {sid}: source_type '{stype}' not allowed")
        rdate = (row.get("retrieval_date") or "").strip()
        if rdate and not DATE_RE.match(rdate):
            errors.append(f"sources {sid}: retrieval_date '{rdate}' not YYYY-MM-DD")
        elif rdate:
            try:
                date.fromisoformat(rdate)
            except ValueError:
                errors.append(f"sources {sid}: retrieval_date '{rdate}' not a real date")
        url = (row.get("url") or "").strip()
        if url and not (url.startswith("http://") or url.startswith("https://")
                        or url.lower().startswith(("doi:", "isbn:"))):
            warnings.append(f"sources {sid}: url is not http(s)/doi/isbn: {url}")
        law = (row.get("accessed_lawfully") or "").strip().lower()
        if law not in ("yes", "no"):
            errors.append(f"sources {sid}: accessed_lawfully must be yes/no")
        if stype == "aggregator":
            if not (row.get("original_producer") or "").strip():
                errors.append(
                    f"sources {sid}: aggregator must declare original_producer")
            ref = row.get("original_source_id", "").strip()
            if ref and ref not in source_ids and ref not in {
                    r["source_id"].strip() for r in sources}:
                errors.append(
                    f"sources {sid}: original_source_id '{ref}' not found")

    key_set = {c.strip() for c in (key_claim_ids or [])}
    claim_ids = set()
    for raw_row in claims:
        row = {k: (v or "") for k, v in raw_row.items() if k is not None}
        cid = row["claim_id"].strip()
        if not CID_RE.match(cid):
            errors.append(f"claims: bad claim_id '{cid}' (want C + >=3 digits)")
        if cid in claim_ids:
            errors.append(f"claims: duplicate claim_id {cid}")
        claim_ids.add(cid)
        ctype = (row.get("claim_type") or "").strip()
        if ctype not in ALLOWED_CLAIM_TYPES:
            errors.append(f"claims {cid}: claim_type '{ctype}' not allowed")
        status = (row.get("status") or "").strip()
        if status not in ALLOWED_STATUS:
            errors.append(f"claims {cid}: status '{status}' not allowed")
        refs = [x.strip() for x in row.get("source_ids", "").split(";") if x.strip()]
        if not refs and status != "placeholder":
            errors.append(f"claims {cid}: source_ids empty (only placeholder claims may omit refs)")
        for ref in refs:
            if ref.startswith("CALC:"):
                continue
            if ref not in source_ids:
                errors.append(f"claims {cid}: source ref '{ref}' not in registry")
        # independent_sources consistency
        try:
            indep = int(row.get("independent_sources", "0").strip() or 0)
        except ValueError:
            indep = -1
            errors.append(f"claims {cid}: independent_sources not an integer")
        real_refs = [r for r in refs if not r.startswith("CALC:")]
        if indep >= 0 and indep > len(real_refs):
            errors.append(
                f"claims {cid}: independent_sources={indep} but only "
                f"{len(real_refs)} refs listed")
        is_critical = cid in key_set or ctype in ("statistic", "forecast")
        if is_critical and status == "verified" and indep < 2 and indep >= 0:
            errors.append(
                f"claims {cid}: critical claim marked verified with "
                f"{indep} independent source; downgrade to single_source/"
                f"contested or add evidence")
        if status == "placeholder":
            if "需补" not in row.get("final_wording", ""):
                errors.append(
                    f"claims {cid}: placeholder claim final_wording must "
                    f"contain a [需补：…] marker")
        if status == "refuted" and not row.get("disconfirmation", "").strip():
            errors.append(f"claims {cid}: refuted claim needs disconfirmation note")

    return errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", required=True)
    ap.add_argument("--claims", required=True)
    ap.add_argument("--key-claims", default="",
                    help="comma-separated extra claim IDs treated as critical")
    args = ap.parse_args()
    keys = [x.strip() for x in args.key_claims.split(",") if x.strip()]
    errors, warnings = validate(args.sources, args.claims, keys)
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

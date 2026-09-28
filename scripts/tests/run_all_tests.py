#!/usr/bin/env python3
"""Minimal functional tests for the offline kit scripts.

Runs each CLI against good/bad fixtures and asserts exit codes plus key output.
Python standard library only. Run:

    python3 scripts/tests/run_all_tests.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
FIX = HERE / "fixtures"
REPO = SCRIPTS.parent

results = []


def run(name, args, expect_code, must_contain=()):
    proc = subprocess.run(
        [sys.executable, *args], cwd=REPO, capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    ok = proc.returncode == expect_code and all(s in out for s in must_contain)
    results.append((ok, name, proc.returncode, out))
    return ok


def main() -> int:
    # 1. frontmatter validation against the real kit
    run("frontmatter: real kit passes",
        [str(SCRIPTS / "validate_frontmatter.py"), "--root", str(REPO)], 0,
        must_contain=("skill files valid",))

    # 2. evidence ledger: good fixtures pass
    run("ledger: good fixtures pass",
        [str(SCRIPTS / "validate_evidence_ledger.py"),
         "--sources", str(FIX / "sources_good.csv"),
         "--claims", str(FIX / "claims_good.csv")], 0,
        must_contain=("0 error(s)",))

    # 3. evidence ledger: bad fixtures fail with the expected errors
    run("ledger: bad fixtures fail",
        [str(SCRIPTS / "validate_evidence_ledger.py"),
         "--sources", str(FIX / "sources_bad.csv"),
         "--claims", str(FIX / "claims_bad.csv")], 1,
        must_contain=("aggregator must declare original_producer",
                      "critical claim marked verified with 1 independent source",
                      "source ref 'S404' not in registry"))

    # 4. claim audit: clean draft passes
    run("audit: clean draft passes",
        [str(SCRIPTS / "audit_claim_citations.py"),
         "--sources", str(FIX / "sources_good.csv"),
         "--claims", str(FIX / "claims_good.csv"),
         "--draft", str(FIX / "draft_clean.md")], 0)

    # 5. claim audit: dirty draft blocked
    run("audit: dirty draft blocked",
        [str(SCRIPTS / "audit_claim_citations.py"),
         "--sources", str(FIX / "sources_good.csv"),
         "--claims", str(FIX / "claims_good.csv"),
         "--draft", str(FIX / "draft_dirty.md")], 1,
        must_contain=("internal research ID", "unresolved placeholder"))

    # 6. market sizing: reconciles
    run("market sizing: reconciles within tolerance",
        [str(SCRIPTS / "market_sizing.py"),
         "--assumptions", str(FIX / "assumptions_good.csv"),
         "--sensitivity", "GROWTH_base:0.06:0.12:0.18"], 0,
        must_contain=("Reconciliation passed", "DISCLAIMER"))

    # 7. preflight: clean passes, dirty blocked
    run("preflight: clean passes",
        [str(SCRIPTS / "preflight.py"),
         "--draft", str(FIX / "draft_clean.md")], 0,
        must_contain=("PASS",))
    run("preflight: dirty blocked",
        [str(SCRIPTS / "preflight.py"),
         "--draft", str(FIX / "draft_dirty.md")], 1,
        must_contain=("platform automation", "internal research ID",
                      "missing local image/link target"))

    # 8. local link checker on the fixtures dir (dirty draft references missing.png)
    run("link check: broken image detected",
        [str(SCRIPTS / "check_local_links.py"), "--root", str(FIX)], 1,
        must_contain=("missing.png",))

    failed = [r for r in results if not r[0]]
    for ok, name, code, _ in results:
        print(("PASS " if ok else "FAIL "), name, f"(exit={code})")
    print(f"\n{len(results) - len(failed)}/{len(results)} test groups passed")
    if failed:
        print("\n--- failure outputs ---")
        for ok, name, code, out in failed:
            print(f"\n### {name}\n{out[-1500:]}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

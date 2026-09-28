#!/usr/bin/env python3
"""Deterministic market-sizing arithmetic: TAM/SAM/SOM dual-path reconciliation,
bear/base/bull scenarios and single-variable sensitivity.

Offline, Python standard library only. The script performs arithmetic ON THE
USER'S ASSUMPTIONS; it produces no forecasts of its own and is not investment,
legal, tax or regulatory advice.

Assumptions CSV columns:
    assumption_id, description, value, unit, source_id, scenario, notes

Special rows (by assumption_id, order-independent):
    BASE_<scenario>   base-year market value, e.g. BASE_base
    GROWTH_<scenario> annual growth rate as decimal (0.12 = 12%)
    YEARS             forecast horizon (integer)
    SAM_RATE_<s>      SAM as fraction of TAM
    SOM_RATE_<s>      SOM as fraction of SAM
    Bottom-up path (per scenario):
      BOTTOMUP_UNITS_<s>  number of paying customers/units
      BOTTOMUP_ARPU_<s>   annual revenue per unit (same currency as BASE)
      BOTTOMUP_SAM_<s>    reachable units
      BOTTOMUP_SOM_<s>    obtainable units

Usage:
    python3 market_sizing.py --assumptions market_assumptions.csv \
        [--reconcile-tolerance 0.20] [--sensitivity GROWTH_base:0.08:0.10:0.12:0.15]
Exit code 0 = reconciled within tolerance on all scenarios, 1 otherwise.
"""
from __future__ import annotations

import argparse
import csv
import sys


def load(path: str):
    rows = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows[r["assumption_id"].strip()] = r
    return rows


def val(rows, key, default=None, cast=float):
    if key not in rows or rows[key]["value"].strip() == "":
        return default
    return cast(rows[key]["value"].strip())


def top_down(rows, scenario: str):
    base = val(rows, f"BASE_{scenario}")
    g = val(rows, f"GROWTH_{scenario}")
    years = val(rows, "YEARS", cast=int)
    if base is None or g is None or years is None:
        return None
    tam = base * (1 + g) ** years
    sam_rate = val(rows, f"SAM_RATE_{scenario}", 1.0)
    som_rate = val(rows, f"SOM_RATE_{scenario}", 1.0)
    sam = tam * sam_rate
    som = sam * som_rate
    return {"TAM": tam, "SAM": sam, "SOM": som,
            "base": base, "growth": g, "years": years}


def bottom_up(rows, scenario: str):
    units = val(rows, f"BOTTOMUP_UNITS_{scenario}")
    arpu = val(rows, f"BOTTOMUP_ARPU_{scenario}")
    sam_units = val(rows, f"BOTTOMUP_SAM_{scenario}", units)
    som_units = val(rows, f"BOTTOMUP_SOM_{scenario}",
                    val(rows, f"BOTTOMUP_SAM_{scenario}", units))
    if units is None or arpu is None:
        return None
    return {"TAM": units * arpu,
            "SAM": (sam_units or units) * arpu,
            "SOM": (som_units or 0) * arpu}


def diff_fraction(a: float, b: float) -> float:
    base = max(abs(a), abs(b))
    return abs(a - b) / base if base else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assumptions", required=True)
    ap.add_argument("--reconcile-tolerance", type=float, default=0.20)
    ap.add_argument("--sensitivity", default="",
                    help="KEY:v1:v2:... e.g. GROWTH_base:0.08:0.10:0.12:0.15")
    args = ap.parse_args()
    rows = load(args.assumptions)

    print("Market sizing — deterministic arithmetic on user assumptions\n")
    failures = []
    scenarios = ["bear", "base", "bull"]
    results = {}
    for sc in scenarios:
        td = top_down(rows, sc)
        bu = bottom_up(rows, sc)
        if td is None:
            print(f"[{sc}] top-down: assumptions missing, skipped")
            continue
        results[sc] = (td, bu)
        print(f"[{sc}] top-down : TAM={td['TAM']:.2f}  SAM={td['SAM']:.2f}  "
              f"SOM={td['SOM']:.2f}  (base={td['base']}, growth={td['growth']:.2%}, "
              f"years={td['years']})")
        if bu is not None:
            print(f"[{sc}] bottom-up: TAM={bu['TAM']:.2f}  SAM={bu['SAM']:.2f}  "
                  f"SOM={bu['SOM']:.2f}")
            for layer in ("TAM", "SAM", "SOM"):
                d = diff_fraction(td[layer], bu[layer])
                flag = "OK" if d <= args.reconcile_tolerance else "MISMATCH"
                print(f"[{sc}] reconcile {layer}: gap={d:.1%} [{flag}]")
                if flag == "MISMATCH":
                    failures.append(
                        f"{sc} {layer} dual-path gap {d:.1%} exceeds tolerance "
                        f"{args.reconcile_tolerance:.0%}")
        else:
            print(f"[{sc}] bottom-up: assumptions missing (only top-down shown)")
        print()

    if args.sensitivity:
        key, _, raw = args.sensitivity.partition(":")
        vals = [float(x) for x in raw.split(":") if x.strip()]
        print(f"Sensitivity on {key} (base scenario TAM):")
        original = rows.get(key, {}).get("value")
        for v in vals:
            rows.setdefault(key, {"assumption_id": key, "value": ""})
            rows[key]["value"] = str(v)
            td = top_down(rows, "base")
            if td:
                print(f"  {key}={v:.2%} -> TAM={td['TAM']:.2f}")
        if original is not None:
            rows[key]["value"] = original

    print("\nDISCLAIMER: internal deterministic check on supplied assumptions; "
          "not investment advice; no external-effect promise.")
    if failures:
        print("\nRECONCILE FAILURES:")
        for f in failures:
            print(" -", f)
        return 1
    print("\nReconciliation passed within tolerance.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

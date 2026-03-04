#!/usr/bin/env python3
"""
Readability‑statistics demo.

Given a plain‑text string (or a file), this script prints a selection of
commonly‑referenced readability scores:

1. Flesch‑Kincaid Grade Level
2. Flesch Reading Ease
3. Gunning Fog Index
4. SMOG Index
5. Coleman‑Liau Index
6. Automated Readability Index (ARI)
7. Dale‑Chall Readability Score
8. Linsear Write Formula
9. FORCAST Grade Level
10. New Dale‑Chall (if you have the word list)

Feel free to drop or add any of the calls below – they’re all simple
functions from the `textstat` module.
"""

import argparse
import sys
from pathlib import Path

import textstat


def read_input(source: str) -> str:
    """Read text from a file path or from stdin."""
    if source == "-":
        return sys.stdin.read()
    else:
        return Path(source).read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute a suite of readability statistics for a text."
    )
    parser.add_argument(
        "source",
        help="Path to a .txt file containing the text, or '-' to read from STDIN.",
    )
    args = parser.parse_args()

    text = read_input(args.source)

    # Basic sanity check
    if not text.strip():
        print("⚠️  Empty input – nothing to analyze.", file=sys.stderr)
        sys.exit(1)

    # ----------------------------------------------------------------------
    # 1️⃣  Classic formulas (the ones most people recognise)
    # ----------------------------------------------------------------------
    fk_grade = textstat.flesch_kincaid_grade(text)
    flesch_ease = textstat.flesch_reading_ease(text)
    gunning_fog = textstat.gunning_fog(text)
    smog = textstat.smog_index(text)
    coleman_liau = textstat.coleman_liau_index(text)
    ari = textstat.automated_readability_index(text)

    # ----------------------------------------------------------------------
    # 2️⃣  Additional useful metrics
    # ----------------------------------------------------------------------
    dale_chall = textstat.dale_chall_readability_score(text)
    linsear_write = textstat.linsear_write_formula(text)
    forcast = textstat.forcast_grade(text)

    # ----------------------------------------------------------------------
    # 3️⃣  Print results in a tidy table
    # ----------------------------------------------------------------------
    print("\nReadability statistics for:", args.source)
    print("-" * 50)
    print(f"{'Metric':30} {'Score'}")
    print("-" * 50)
    print(f"{'Flesch‑Kincaid Grade Level':30} {fk_grade:.2f}")
    print(f"{'Flesch Reading Ease':30} {flesch_ease:.2f}")
    print(f"{'Gunning Fog Index':30} {gunning_fog:.2f}")
    print(f"{'SMOG Index':30} {smog:.2f}")
    print(f"{'Coleman‑Liau Index':30} {coleman_liau:.2f}")
    print(f"{'Automated Readability Index (ARI)':30} {ari:.2f}")
    print(f"{'Dale‑Chall Readability Score':30} {dale_chall:.2f}")
    print(f"{'Linsear Write Formula':30} {linsear_write:.2f}")
    print(f"{'FORCAST Grade Level':30} {forcast:.2f}")
    print("-" * 50)


if __name__ == "__main__":
    main()

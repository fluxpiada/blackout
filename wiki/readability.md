# Readability analysis

Readability, pacing and vocabulary analysis lives in its own repository:

**<https://github.com/fluxpiada/readability-stats>**

It reads a folder of `.md` chapters — which is exactly what `manuscript/` is —
and writes a timestamped report snapshot you can diff against earlier drafts.

```bash
git clone https://github.com/fluxpiada/readability-stats.git
cd readability-stats
./run.sh 8   ~/Documents/Blackout/blackout/manuscript   # the full report
./run.sh all ~/Documents/Blackout/blackout/manuscript   # every analysis step
```

You do not need to install Python or any packages — the runner fetches
everything through [uv](https://docs.astral.sh/uv/) on first use.

Step 8 writes `reports/<timestamp>/` containing `report.md`, `report.pdf`, a
pacing curve, and a `summary.json`. `reports/index.md` tables every snapshot
with the change in word count and mean Flesch since the run before it, so the
trend across drafts is the thing you read rather than any single number.

> The scripts in that repository's root are calibrated for **English**. For a
> Dutch manuscript use its `nl/` implementation, which is built on
> Flesch-Douma and Brouwer's Leesindex A instead.

## Why this file no longer holds the numbers

It used to carry a hand-pasted table for v1.11.28. That table went stale
immediately — it was pinned to one version and listed only eleven of the twelve
chapters — and the local `analysis/readability.py` that notionally produced it
was never wired to anything and did not run. Both are gone. Generate the numbers
when you want them; don't copy them into the repo, where they can only rot.

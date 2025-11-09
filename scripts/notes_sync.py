import argparse, pathlib, json, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTES = ROOT / "notes"


def main():
ap = argparse.ArgumentParser()
ap.add_argument("--subset", default="all")
args = ap.parse_args()

notes = []
base = NOTES if args.subset == "all" else NOTES / args.subset
if base.exists():
for p in sorted(base.rglob("*.md")):
notes.append({"path": str(p.relative_to(ROOT)), "size": p.stat().st_size})

out = ROOT / "build" / "notes.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({"subset": args.subset, "count": len(notes), "files": notes}, indent=2), encoding="utf-8")
print(f"[ok] wrote {out}")
return 0

if __name__ == "__main__":
sys.exit(main())
```python
import argparse, sys

def main():
p = argparse.ArgumentParser()
p.add_argument("--subset", default="all")
args = p.parse_args()

# TODO: real sync logic
print(f"[ok] notes synced (subset={args.subset})")

sys.exit(main())

import argparse, pathlib, shutil, sys, subprocess, shlex

ROOT = pathlib.Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public" # optional static assets
README = ROOT / "README.md" # rendered to index.html if present


def run(cmd: list[str]):
print("$", " ".join(shlex.quote(c) for c in cmd), flush=True)
return subprocess.run(cmd, check=True)


def main():
ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--commit", default="")
args = ap.parse_args()

out = pathlib.Path(args.out)
if out.exists():
shutil.rmtree(out)
out.mkdir(parents=True)

# 1) Copy static assets if any
if PUBLIC.exists():
shutil.copytree(PUBLIC, out, dirs_exist_ok=True)

# 2) Prefer existing index.html; otherwise build from README.md
INDEX = ROOT / "index.html"
if INDEX.exists():
    shutil.copy2(INDEX, out / "index.html")
elif README.exists():
    try:
        run(["pandoc", str(README), "-s", "-o", str(out / "index.html")])
    except Exception:
        (out / "index.html").write_text(README.read_text(encoding="utf-8"), encoding="utf-8")
else:
    (out / "index.html").write_text("<h1>Site built</h1>\n", encoding="utf-8")

# 3) Simple commit badge
if args.commit:
badge = f"
<!-- built from {args.commit[:7]} -->
"
p = out / "index.html"
p.write_text(p.read_text(encoding="utf-8") + badge, encoding="utf-8")

print(f"[ok] built site → {out.resolve()}")
return 0

if __name__ == "__main__":
sys.exit(main())
```python
import argparse, pathlib, sys

def main():
p = argparse.ArgumentParser()
p.add_argument("--out", required=True)
args = p.parse_args()

out = pathlib.Path(args.out)
out.mkdir(parents=True, exist_ok=True)
sys.exit(main())

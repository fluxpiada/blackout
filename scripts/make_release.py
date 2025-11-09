import argparse, pathlib, sys, subprocess, shlex, hashlib, json, time
return 2

epub_path = out / EPUB_NAME

pandoc_cmd = [
"pandoc",
*sorted(str(p) for p in MANUSCRIPT.glob("*.md")),
"--resource-path=manuscript:images",
f"--epub-cover-image={COVER}",
f"--epub-metadata={METADATA}",
"--toc",
"-o", str(epub_path),
]

try:
run(pandoc_cmd)
except subprocess.CalledProcessError as e:
print("Pandoc failed", e, file=sys.stderr)
return e.returncode or 1

# Checksums + manifest
digest = sha256(epub_path)
(out / "SHA256SUMS").write_text(f"{digest} {epub_path.name}
", encoding="utf-8")

manifest = {
"tag": args.tag or "manual",
"built_at": int(time.time()),
"files": [epub_path.name, "SHA256SUMS"],
}
(out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

print(f"[ok] EPUB: {epub_path}")
print(f"[ok] SHA256: {digest}")
return 0

if __name__ == "__main__":
sys.exit(main())
```python
import argparse, pathlib, sys

def main():
p = argparse.ArgumentParser()
p.add_argument("--out", required=True)
p.add_argument("--tag", default="")
args = p.parse_args()

out = pathlib.Path(args.out)
out.mkdir(parents=True, exist_ok=True)

# TODO: build real release assets (e.g., EPUB, zips)
(out / "README.txt").write_text(f"Release for {args.tag or 'manual'}\n", encoding="utf-8")
print(f"[ok] assets in {out.resolve()}")

if __name__ == "__main__":
sys.exit(main())

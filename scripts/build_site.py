# scripts/build_site.py
import argparse, pathlib, sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--commit", default="")
    args = p.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # >>> Heavy lifting here (render, compile, etc.)
    # Write ONLY what you intend to publish:
    (out / "index.html").write_text("<h1>Site built</h1>", encoding="utf-8")

    print(f"[ok] built to {out.resolve()} @ {args.commit[:7]}")

if __name__ == "__main__":
    sys.exit(main())

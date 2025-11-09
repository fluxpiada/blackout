# scripts/build_site.py  — authoritative Pages builder
# Inputs:
#   --out dist            # output dir
#   --commit <sha>        # optional; adds build badge
#
# Looks for sources in this order:
#   1) site/index.md (preferred, rendered via pandoc)
#   2) README.md         (fallback, rendered via pandoc)
#   3) index.html        (last resort, copied as-is)
#
# Optional assets (copied if present): public/, styles/, templates/, images/

import argparse, pathlib, shutil, sys, subprocess, shlex

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DEFAULT = "dist"

# Preferred content sources
SITE_MD   = ROOT / "site" / "index.md"
README_MD = ROOT / "README.md"
RAW_HTML  = ROOT / "index.html"

# Optional extras
TEMPLATE  = ROOT / "templates" / "page.html"  # optional pandoc template
CSS       = ROOT / "styles" / "site.css"      # optional stylesheet

# Asset dirs to copy verbatim if present
ASSET_DIRS = [ROOT / "public", ROOT / "styles", ROOT / "templates", ROOT / "images"]

def run(cmd: list[str]):
    print("$", " ".join(shlex.quote(c) for c in cmd), flush=True)
    return subprocess.run(cmd, check=True)

def copy_assets(out: pathlib.Path):
    for d in ASSET_DIRS:
        if d.exists():
            shutil.copytree(d, out / d.name, dirs_exist_ok=True)

def build_from_markdown(src_md: pathlib.Path, out_html: pathlib.Path):
    cmd = ["pandoc", str(src_md), "-s", "-o", str(out_html)]
    if TEMPLATE.exists():
        cmd.extend(["--template", str(TEMPLATE)])
    if CSS.exists():
        # ensure CSS ends up alongside index.html
        shutil.copy2(CSS, out_html.parent / CSS.name)
        cmd.extend(["--css", CSS.name])
    # add more flags here if you need them, e.g. TOC depth:
    # cmd.extend(["--toc", "--toc-depth=2"])
    run(cmd)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT_DEFAULT)
    ap.add_argument("--commit", default="")
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    # 1) Copy assets first (so template/css are available for pandoc)
    copy_assets(out)

    # 2) Build index.html deterministically
    target = out / "index.html"
    if SITE_MD.exists():
        build_from_markdown(SITE_MD, target)
    elif README_MD.exists():
        build_from_markdown(README_MD, target)
    elif RAW_HTML.exists():
        shutil.copy2(RAW_HTML, target)
    else:
        # last-resort placeholder
        target.write_text("<h1>Site built</h1>\n", encoding="utf-8")

    # 3) Append build badge with short SHA (if provided)
    if args.commit and target.exists():
        badge = f"\n<!-- built from {args.commit[:7]} -->\n"
        target.write_text(target.read_text(encoding="utf-8") + badge, encoding="utf-8")

    print(f"[ok] built site → {out.resolve()}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

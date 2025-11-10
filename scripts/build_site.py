# scripts/build_site.py — authoritative Pages builder
# Inputs:
#   --out dist            # output dir
#   --commit <sha>        # optional; adds build badge
#
# Sources (first match wins):
#   1) site/index.md (preferred, rendered via pandoc)
#   2) README.md         (fallback, rendered via pandoc)
#   3) index.html        (last resort, copied as-is)
#
# Optional assets (copied if present): public/, styles/, templates/, images/
#
# Post-processing:
#   - Ensures the Download EPUB button points to the latest release asset:
#       https://github.com/fluxpiada/blackout/releases/latest/download/Blackout_Weak_Signals.epub
#   - If the HTML contains {{ DOWNLOAD_URL }} or [[DOWNLOAD_URL]], it is replaced.
#   - Otherwise, injects a button before </main> or </body>, only if not already present.

import argparse
import pathlib
import shutil
import sys
import subprocess
import shlex
import re

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

# Stable latest-release asset URL (single authoritative source of truth)
DOWNLOAD_URL = "https://github.com/fluxpiada/blackout/releases/latest/download/Blackout_Weak_Signals.epub"

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
    # Example for TOC (disabled by default):
    # cmd.extend(["--toc", "--toc-depth=2"])
    run(cmd)

def ensure_download_link(html: str) -> str:
    """
    - If a placeholder {{ DOWNLOAD_URL }} or [[DOWNLOAD_URL]] exists, replace it.
    - If there is already a link to an .epub (esp. our stable URL), leave as-is.
    - Otherwise, inject a minimal button before </main> or </body>.
    """
    # 1) Replace known placeholders
    replaced = html
    replaced = replaced.replace("{{ DOWNLOAD_URL }}", DOWNLOAD_URL)
    replaced = replaced.replace("[[DOWNLOAD_URL]]", DOWNLOAD_URL)

    if replaced != html:
        return replaced  # placeholder-driven site; done

    # 2) If any existing epub link is present, assume authoring handles it
    epub_link_re = re.compile(r'href=["\']([^"\']+\.epub[^"\']*)["\']', re.IGNORECASE)
    if epub_link_re.search(replaced):
        return replaced

    # 3) Inject a small download button (idempotent—avoid duplicates)
    if DOWNLOAD_URL in replaced or 'class="download-epub"' in replaced:
        return replaced

    button = (
        '\n<div class="download-epub" style="margin:1rem 0;">'
        f'<a class="btn" href="{DOWNLOAD_URL}" download>Download EPUB</a>'
        '</div>\n'
    )

    # Prefer before </main>, else before </body>, else append
    for tag in ("</main>", "</body>"):
        idx = replaced.lower().rfind(tag)
        if idx != -1:
            return replaced[:idx] + button + replaced[idx:]
    return replaced + button

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
        target.write_text("<!doctype html><meta charset='utf-8'><h1>Site built</h1>\n", encoding="utf-8")

    # 3) Post-process index.html: inject/replace the download URL
    if target.exists():
        html = target.read_text(encoding="utf-8")
        html = ensure_download_link(html)
        # 3b) Append build badge with short SHA (if provided)
        if args.commit:
            html += f"\n<!-- built from {args.commit[:7]} -->\n"
        target.write_text(html, encoding="utf-8")

    print(f"[ok] built site → {out.resolve()}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

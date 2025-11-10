# scripts/build_site.py — Pages builder (MD -> HTML, else copy root HTML)
# Sources:
#   1) site/index.md -> pandoc -> dist/index.html
#   2) else copy root index.html -> dist/index.html
# README.md is intentionally ignored.
#
# Assets copied verbatim if present: public/, styles/, templates/, images/
# Post-processing:
#   - Ensure Download button points to latest release asset URL (if none present).
#   - Append timestamp after "Latest build served via GitHub Pages — Version: vX.YY.ZZ".
#
# No CSS is generated or modified here.

import argparse
import pathlib
import shutil
import sys
import subprocess
import shlex
import re
import datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DEFAULT = "dist"

# Sources
SITE_MD   = ROOT / "site" / "index.md"
RAW_HTML  = ROOT / "index.html"

# Optional extras
TEMPLATE  = ROOT / "templates" / "page.html"
CSS_IN    = ROOT / "styles" / "site.css"   # if present, copied to dist/styles/site.css

ASSET_DIRS = [ROOT / "public", ROOT / "styles", ROOT / "templates", ROOT / "images"]

# Stable latest-release asset URL
DOWNLOAD_URL = "https://github.com/fluxpiada/blackout/releases/latest/download/Blackout_Weak_Signals.epub"

def run(cmd: list[str]):
    print("$", " ".join(shlex.quote(c) for c in cmd), flush=True)
    return subprocess.run(cmd, check=True)

def copy_assets(out: pathlib.Path):
    for d in ASSET_DIRS:
        if d.exists():
            shutil.copytree(d, out / d.name, dirs_exist_ok=True)

import subprocess, shutil, pathlib, sys

def _run_pandoc(cmd):
    log_file = ROOT / "pandoc.log"
    cmd = cmd + ["--verbose", f"--log={log_file}"]
    print("[build] running:", " ".join(str(x) for x in cmd))
    try:
        subprocess.run(cmd, check=True)
        print("[build] pandoc OK")
        return True
    except subprocess.CalledProcessError:
        print("\n[build] Pandoc exited non-zero. Tail of pandoc.log:\n")
        try:
            print("\n".join((log_file.read_text().splitlines())[-80:]))
        except Exception as e:
            print(f"[build] could not read pandoc.log: {e}")
        return False

def build_from_markdown(src_md: pathlib.Path, target: pathlib.Path):
    target.mkdir(parents=True, exist_ok=True)

    # Preflight: show what exists in CI
    print(f"[build] src_md exists: {src_md.exists()}  -> {src_md}")
    print(f"[build] template exists: {TEMPLATE.exists()}  -> {TEMPLATE}")
    print(f"[build] css exists: {CSS_IN.exists()}  -> {CSS_IN}")

    # Always start with a clean, minimal command
    base_cmd = [
        "pandoc", str(src_md), "-s",
        "-o", str(target / "index.html"),
        "--metadata", "pagetitle=The Blackout: Weak Signals",
    ]

    # Ensure CSS is present in dist and linked relatively if available
    with_css_cmd = list(base_cmd)
    if CSS_IN.exists():
        (target / "styles").mkdir(parents=True, exist_ok=True)
        shutil.copy2(CSS_IN, target / "styles" / "site.css")
        with_css_cmd += ["--css", "styles/site.css"]

    # 1) Try WITH template (if present)
    if TEMPLATE.exists():
        with_tpl_cmd = with_css_cmd + ["--template", str(TEMPLATE)]
        print("[build] Attempting build WITH template…")
        if _run_pandoc(with_tpl_cmd):
            return
        print("[build] Retrying WITHOUT template (temporary fallback)…")

    # 2) Fallback: WITHOUT template
    if _run_pandoc(with_css_cmd):
        return

    # 3) If we got here, even the fallback failed — exit hard with guidance
    sys.exit(
        "Build failed. See pandoc.log above. "
        "If step #2 failed, check site/index.md for stray `$…$` or broken code fences."
    )

def ensure_download_link(html: str) -> str:
    # Replace placeholders if present
    html = html.replace("{{ DOWNLOAD_URL }}", DOWNLOAD_URL)
    html = html.replace("[[DOWNLOAD_URL]]", DOWNLOAD_URL)

    # If an .epub href already exists, leave as-is (author controls it)
    if re.search(r'href=["\']([^"\']+\.epub[^"\']*)["\']', html, re.IGNORECASE):
        return html

    # Otherwise inject a minimal button before </main> or </body>
    if DOWNLOAD_URL in html or 'class="download-epub"' in html:
        return html

    button = (
        '\n<div class="download-epub" style="margin:1rem 0;">'
        f'<a class="btn" href="{DOWNLOAD_URL}" download>Download EPUB</a>'
        '</div>\n'
    )
    for tag in ("</main>", "</body>"):
        idx = html.lower().rfind(tag)
        if idx != -1:
            return html[:idx] + button + html[idx:]
    return html + button

def append_timestamp(html: str) -> str:
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    pattern = re.compile(
        r"(Latest\s+build\s+served\s+via\s+GitHub\s+Pages\s+—\s+Version:\s*v[\d\.]+)",
        re.IGNORECASE,
    )
    if pattern.search(html):
        html = pattern.sub(rf"\1 on {now}", html, count=1)
    return html

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT_DEFAULT)
    ap.add_argument("--commit", default="")
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    # Copy assets first
    copy_assets(out)

    # Build index.html
    target = out / "index.html"
    if SITE_MD.exists():
        build_from_markdown(SITE_MD, target)
    elif RAW_HTML.exists():
        shutil.copy2(RAW_HTML, target)
    else:
        target.write_text("<!doctype html><meta charset='utf-8'><h1>Site built</h1>\n", encoding="utf-8")

    # Post-process
    if target.exists():
        html = target.read_text(encoding="utf-8")
        html = ensure_download_link(html)
        html = append_timestamp(html)
        if args.commit:
            html += f"\n<!-- built from {args.commit[:7]} -->\n"
        target.write_text(html, encoding="utf-8")

    print(f"[ok] built site → {out.resolve()}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

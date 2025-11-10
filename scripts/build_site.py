# scripts/build_site.py — Pages builder (MD → HTML, else copy root HTML)
# Rule:
#   1) site/index.md -> pandoc -> dist/index.html
#   2) else copy root index.html -> dist/index.html
# README.md is intentionally ignored.
#
# Post-processing:
#   - If index.html contains <style>…</style>, extract to styles/site.css and inject
#     <link rel="stylesheet" href="styles/site.css"> into <head>.
#   - Ensure Download button points to latest release asset URL.
#   - Append timestamp after "Latest build served via GitHub Pages — Version: vX.YY.ZZ".
#
# Optional asset dirs copied verbatim: public/, styles/, templates/, images/

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
RAW_HTML  = ROOT / "index.html"  # root HTML

# Optional extras
TEMPLATE  = ROOT / "templates" / "page.html"
CSS_DIR   = ROOT / "styles"          # may exist already
CSS_FILE  = "site.css"               # target CSS filename under dist/styles/

ASSET_DIRS = [ROOT / "public", ROOT / "styles", ROOT / "templates", ROOT / "images"]

# Stable latest-release asset URL
DOWNLOAD_URL = "https://github.com/fluxpiada/blackout/releases/latest/download/Blackout_Weak_Signals.epub"

STYLE_TAG_RE = re.compile(r"(<style[^>]*>)(.*?)(</style>)", re.IGNORECASE | re.DOTALL)
HEAD_CLOSE_RE = re.compile(r"</head\s*>", re.IGNORECASE)

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
    # If a styles/ already exists, ensure the css is alongside index.html
    if (ROOT / "styles" / CSS_FILE).exists():
        shutil.copy2(ROOT / "styles" / CSS_FILE, out_html.parent / CSS_FILE)
        cmd.extend(["--css", CSS_FILE])
    run(cmd)

def ensure_download_link(html: str) -> str:
    # Replace placeholders if present
    html = html.replace("{{ DOWNLOAD_URL }}", DOWNLOAD_URL)
    html = html.replace("[[DOWNLOAD_URL]]", DOWNLOAD_URL)

    # If an .epub href already exists, don't touch (author controls it)
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

def externalize_inline_css(html: str, out_dir: pathlib.Path) -> str:
    """
    If there's an inline <style>…</style> (typically in <head>), write it to dist/styles/site.css,
    remove the style tag, and insert a <link rel="stylesheet" href="styles/site.css"> before </head>.
    Idempotent: if a link to styles/site.css already exists, do nothing.
    """
    # If link already present, skip
    if re.search(r'href=["\']styles\/site\.css["\']', html, re.IGNORECASE):
        return html

    m = STYLE_TAG_RE.search(html)
    if not m:
        return html  # no inline styles to extract

    css_payload = m.group(2).strip()
    if not css_payload:
        return html

    # Ensure dist/styles exists and write CSS
    styles_out_dir = out_dir / "styles"
    styles_out_dir.mkdir(parents=True, exist_ok=True)
    css_path = styles_out_dir / CSS_FILE
    css_path.write_text(css_payload + "\n", encoding="utf-8")

    # Remove the first <style>…</style>
    without_style = html[:m.start()] + html[m.end():]

    # Inject <link> before </head>
    link_tag = '<link rel="stylesheet" href="styles/site.css">\n'
    if HEAD_CLOSE_RE.search(without_style):
        return HEAD_CLOSE_RE.sub(link_tag + "</head>", without_style, count=1)
    # If no </head>, prepend at top as a fallback
    return link_tag + without_style

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT_DEFAULT)
    ap.add_argument("--commit", default="")
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    # Copy assets first (public/, styles/, templates/, images/)
    copy_assets(out)

    target = out / "index.html"

    # Builder rule: site/index.md → pandoc; else copy root index.html
    if SITE_MD.exists():
        build_from_markdown(SITE_MD, target)
    elif RAW_HTML.exists():
        shutil.copy2(RAW_HTML, target)
    else:
        target.write_text("<!doctype html><meta charset='utf-8'><h1>Site built</h1>\n", encoding="utf-8")

    # Post-process index.html
    if target.exists():
        html = target.read_text(encoding="utf-8")

        # If we used root index.html, externalize inline CSS (create styles/site.css)
        if not SITE_MD.exists():
            html = externalize_inline_css(html, out)

        html = ensure_download_link(html)
        html = append_timestamp(html)

        # Append build badge with short SHA (if provided)
        if args.commit:
            html += f"\n<!-- built from {args.commit[:7]} -->\n"

        target.write_text(html, encoding="utf-8")

    print(f"[ok] built site → {out.resolve()}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
import argparse
import pathlib
import shutil
import subprocess
import sys

# ---------- Paths (your originals kept) ----------
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DEFAULT = "dist"

# Sources
SITE_MD   = ROOT / "site" / "index.md"
RAW_HTML  = ROOT / "index.html"  # unused here but kept

# Optional extras
TEMPLATE  = ROOT / "templates" / "page.html"
CSS_IN    = ROOT / "styles" / "site.css"   # if present, copied to dist/styles/site.css

ASSET_DIRS = [ROOT / "public", ROOT / "styles", ROOT / "templates", ROOT / "images"]  # not used by the build, kept

LOG_FILE = ROOT / "pandoc.log"


def _run_pandoc(cmd: list[str]) -> bool:
    """Run pandoc with verbose logging; return True on success."""
    full = cmd + ["--verbose", f"--log={LOG_FILE}"]
    print("[build] running:", " ".join(str(x) for x in full))
    try:
        subprocess.run(full, check=True)
        print("[build] pandoc OK")
        return True
    except subprocess.CalledProcessError:
        if LOG_FILE.exists():
            print("\n[build] Pandoc failed. Tail of pandoc.log:\n")
            try:
                print("\n".join(LOG_FILE.read_text(errors="ignore").splitlines()[-80:]))
            except Exception as e:
                print(f"[build] could not read pandoc.log: {e}")
        else:
            print("[build] Pandoc failed early (no pandoc.log written).")
        return False


def build_from_markdown(src_md: pathlib.Path, out_dir: pathlib.Path) -> pathlib.Path:
    """
    Build site/index.md to out_dir/index.html.
    Try with template (if present); on failure, retry without template.
    Copy CSS into out_dir/styles/site.css and link it relatively.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "index.html"

    # Preflight visibility in CI
    print(f"[build] src_md exists: {src_md.exists()}  -> {src_md}")
    print(f"[build] template exists: {TEMPLATE.exists()}  -> {TEMPLATE}")
    print(f"[build] css exists: {CSS_IN.exists()}  -> {CSS_IN}")

    # Base command
    base_cmd = [
        "pandoc",
        str(src_md),
        "-s",
        "-o", str(out_file),
        "--metadata", "pagetitle=The Blackout: Weak Signals",
    ]

    # CSS (optional)
    cmd_with_css = list(base_cmd)
    if CSS_IN.exists():
        (out_dir / "styles").mkdir(parents=True, exist_ok=True)
        shutil.copy2(CSS_IN, out_dir / "styles" / "site.css")
        # Link relative to the output file location
        cmd_with_css += ["--css", "styles/site.css"]

    # 1) Try WITH template (if present)
    attempted_with_template = False
    if TEMPLATE.exists():
        attempted_with_template = True
        with_tpl = cmd_with_css + ["--template", str(TEMPLATE)]
        print("[build] Attempting build WITH template…")
        if _run_pandoc(with_tpl):
            return out_file
        print("[build] Retrying WITHOUT template (temporary fallback)…")

    # 2) Fallback: WITHOUT template
    if _run_pandoc(cmd_with_css):
        if attempted_with_template:
            print("[build] Built without template due to previous template error.")
        return out_file

    # 3) Hard stop
    sys.e

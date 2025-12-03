#!/usr/bin/env bash

# ============================================================
# Build script for The Blackout EPUB (with release history)
# ============================================================

set -euo pipefail

BOOK_TITLE="Blackout_Weak_Signals"
OUTDIR="versions"
META="epub/metadata.xml"
RELEASE_SCRIPT="epub/make_releases_md.js"
COVER="images/cover.png"
CSS="epub/style.css"   # optional; create only if needed

# ------------------------------------------------------------
# 🧭 Determine version number
# ------------------------------------------------------------
if [[ "${1-}" == "--auto" ]]; then
  VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0-auto")
  echo "🤖 Auto mode enabled. Using version: $VERSION"
else
  read -p "Enter version number (e.g. v1.10.25): " VERSION
  [[ -z "$VERSION" ]] && { echo "❌ No version entered. Aborting."; exit 1; }
fi

# ------------------------------------------------------------
# 📝 Generate GitHub release history
# ------------------------------------------------------------
if [[ -f "$RELEASE_SCRIPT" ]]; then
  echo "📜 Generating releases.md from GitHub API..."
  node "$RELEASE_SCRIPT"
else
  echo "⚠️ Release script not found at $RELEASE_SCRIPT — skipping."
fi

# ------------------------------------------------------------
# 📁 Ensure output directory exists
# ------------------------------------------------------------
mkdir -p "$OUTDIR"

# ------------------------------------------------------------
# ⚙️ Build EPUB
# ------------------------------------------------------------
echo "⚙️ Building EPUB version $VERSION..."

pandoc manuscript/*.md \
  --resource-path="manuscript:images" \
  --epub-cover-image="$COVER" \
  --epub-metadata="$META" \
  ${CSS:+ --css="$CSS"} \
  --toc \
  -o "$OUTDIR/${BOOK_TITLE}_${VERSION}.epub"

echo
echo "🎉 EPUB built successfully:"
echo "   → $OUTDIR/${BOOK_TITLE}_${VERSION}.epub"
echo

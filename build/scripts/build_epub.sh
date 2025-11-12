#!/usr/bin/env bash
# ============================================================
# Manual build script for The Blackout EPUB
# ============================================================

set -e
BOOK_TITLE="Blackout_Weak_Signals"
VERSION=$(grep '^version:' content/metadata.yaml | awk '{print $2}')
OUTDIR="build/output"
TEMPLATE="build/pandoc/template.html"
STYLE="build/pandoc/style.css"
COVER="build/pandoc/cover.png"

echo "🔧 Building EPUB version $VERSION..."
mkdir -p "$OUTDIR"

pandoc content/manuscript/*.md \
  --metadata-file=content/metadata.yaml \
  --template="$TEMPLATE" \
  --css="$STYLE" \
  --epub-cover-image="$COVER" \
  -o "$OUTDIR/${BOOK_TITLE}_${VERSION}.epub"

echo "✅ EPUB built: $OUTDIR/${BOOK_TITLE}_${VERSION}.epub"

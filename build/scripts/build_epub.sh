#!/usr/bin/env bash
# ============================================================
# Manual + Automated build script for The Blackout EPUB
# ============================================================

set -e

BOOK_TITLE="Blackout_Weak_Signals"
OUTDIR="build/output"
TEMPLATE="build/pandoc/template.html"
STYLE="build/pandoc/style.css"
COVER="build/pandoc/cover.png"
META="content/metadata.yaml"

# ------------------------------------------------------------
# 🧭 Determine version number
# ------------------------------------------------------------
if [[ "$1" == "--auto" ]]; then
  # Try to detect latest tag
  VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0-auto")
  echo "🤖 Auto mode enabled. Using version: $VERSION"
else
  read -p "Enter version number (e.g. v1.10.25): " VERSION
  if [[ -z "$VERSION" ]]; then
    echo "❌ No version entered. Aborting."
    exit 1
  fi
fi

# ------------------------------------------------------------
# 📝 Update metadata.yaml (if present)
# ------------------------------------------------------------
if [[ -f "$META" ]]; then
  if grep -q '^version:' "$META"; then
    sed -i.bak "s/^version:.*/version: \"$VERSION\"/" "$META"
  else
    echo "version: \"$VERSION\"" >> "$META"
  fi
else
  echo "⚠️  Metadata file not found, continuing without update."
fi

# ------------------------------------------------------------
# ⚙️ Build EPUB
# ------------------------------------------------------------
echo "🔧 Building EPUB version $VERSION..."
mkdir -p "$OUTDIR"

pandoc content/manuscript/*.md \
  --metadata-file="$META" \
  --resource-path=.:content:build/pandoc \
  --template="$TEMPLATE" \
  --css="$STYLE" \
  --epub-cover-image="$COVER" \
  -o "$OUTDIR/${BOOK_TITLE}_${VERSION}.epub"

echo "✅ EPUB built successfully:"
echo "   → $OUTDIR/${BOOK_TITLE}_${VERSION}.epub"

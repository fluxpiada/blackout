#!/usr/bin/env bash

# ============================================================
# Build script for The Blackout PDF in Shunn manuscript format
# https://www.shunn.net/format/story/
# ============================================================

set -euo pipefail

BOOK_TITLE="Blackout_Weak_Signals"
OUTDIR="versions"
META="pdf/manuscript.yaml"
TEMPLATE="pdf/shunn.latex"
FILTER="pdf/shunn.lua"

VERSION=""
CLASSIC=false
PAPERSIZE="letter"
TITLEPAGE=false
EXTRAS=false
FONT=""

usage() {
  cat <<'EOF'
Usage: pdf/bake_book_pdf.sh [options]

  --auto           Take the version from the latest git tag (for CI)
  --version=VER    Use VER as the version string
  --font=NAME      Typeset in NAME (e.g. --font="Georgia"). Overrides the
                   mainfont: key in pdf/manuscript.yaml
  --list-fonts     List font families installed on this machine, then exit
  --classic        Shunn Classic: monospace face, emphasis underlined
  --a4             A4 paper instead of the US Letter the spec assumes
  --title-page     Novel format: a separate title page, page 1 = first text page
  --with-extras    Append acknowledgments and appendix after the end marker
  -h, --help       Show this message

Font resolution order: --font=  >  mainfont: in pdf/manuscript.yaml  >  the
built-in fallback chain. An explicitly requested font that isn't installed is
an error, never a silent substitution.

With no --auto or --version, the script prompts for a version number.
EOF
}

list_fonts() {
  if command -v fc-list >/dev/null 2>&1; then
    fc-list : family | tr ',' '\n' | sort -u | sed '/^$/d'
  else
    echo "❌ fc-list not found. On macOS: brew install fontconfig" >&2
    exit 1
  fi
}

for arg in "$@"; do
  case "$arg" in
    --auto)         VERSION=$(git describe --tags --abbrev=0 --match='v*' 2>/dev/null || echo "v0.0.0-auto") ;;
    --version=*)    VERSION="${arg#*=}" ;;
    --font=*)       FONT="${arg#*=}" ;;
    --list-fonts)   list_fonts; exit 0 ;;
    --classic)      CLASSIC=true ;;
    --a4)           PAPERSIZE="a4" ;;
    --title-page)   TITLEPAGE=true ;;
    --with-extras)  EXTRAS=true ;;
    -h|--help)      usage; exit 0 ;;
    *)              echo "❌ Unknown option: $arg" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ -z "$VERSION" ]]; then
  read -r -p "Enter version number (e.g. v1.11.31): " VERSION
  [[ -z "$VERSION" ]] && { echo "❌ No version entered. Aborting."; exit 1; }
fi

for f in "$META" "$TEMPLATE" "$FILTER"; do
  [[ -f "$f" ]] || { echo "❌ Missing $f — run this from the repo root."; exit 1; }
done

TMPDIR_BUILD=$(mktemp -d)
trap 'rm -rf "$TMPDIR_BUILD"' EXIT

# ------------------------------------------------------------
# 🔤 Pick a font that actually exists on this machine
# ------------------------------------------------------------
font_available() {
  printf '\\documentclass{article}\\usepackage{fontspec}\\setmainfont{%s}\\begin{document}x\\end{document}\n' \
    "$1" > "$TMPDIR_BUILD/probe.tex"
  xelatex -halt-on-error -interaction=batchmode \
    -output-directory="$TMPDIR_BUILD" "$TMPDIR_BUILD/probe.tex" >/dev/null 2>&1
}

MAINFONT=""

# Read a scalar out of the metadata YAML using pandoc, so quoting is handled
# the same way pandoc itself would handle it.
read_meta() {
  printf '$%s$' "$1" > "$TMPDIR_BUILD/meta.tpl"
  pandoc /dev/null --metadata-file="$META" --template="$TMPDIR_BUILD/meta.tpl" \
    -t plain 2>/dev/null | head -1
}

# --font= beats mainfont: in the YAML, which beats the fallback chain below.
[[ -z "$FONT" ]] && FONT=$(read_meta mainfont)

if [[ -n "$FONT" ]]; then
  # An explicit choice is honoured or refused — never quietly swapped out.
  font_available "$FONT" || {
    echo "❌ Font not installed: $FONT"
    echo "   Run 'pdf/bake_book_pdf.sh --list-fonts' to see what's available."
    exit 1
  }
  MAINFONT="$FONT"
  echo "🔤 Using font: $MAINFONT (set explicitly)"
fi

if [[ -z "$MAINFONT" ]]; then
  # Nothing was asked for, so fall back. The chains exist so that a CI box
  # without the Microsoft fonts still produces near-identical pagination.
  if $CLASSIC; then
    # Shunn Classic asks for a monospace face.
    CANDIDATES=("Courier New" "Liberation Mono" "Nimbus Mono PS" "TeX Gyre Cursor" "DejaVu Sans Mono")
  else
    # Shunn Modern asks for a plain serif; Times New Roman is the named example.
    CANDIDATES=("Times New Roman" "Liberation Serif" "Nimbus Roman" "TeX Gyre Termes" "DejaVu Serif")
  fi

  for candidate in "${CANDIDATES[@]}"; do
    if font_available "$candidate"; then MAINFONT="$candidate"; break; fi
  done
  [[ -z "$MAINFONT" ]] && {
    echo "❌ None of these fonts are installed: ${CANDIDATES[*]}"
    echo "   Set one with --font=NAME or mainfont: in $META."
    exit 1
  }
  echo "🔤 Using font: $MAINFONT (fallback chain)"
fi

# ------------------------------------------------------------
# 📚 Assemble the manuscript
# ------------------------------------------------------------
# manuscript/??_*.md is exactly the twelve chapters — it skips the web
# frontmatter (00-), the release log (001_) and the back matter (998_, 999-).
shopt -s nullglob
CHAPTERS=(manuscript/??_*.md)
shopt -u nullglob
[[ ${#CHAPTERS[@]} -eq 0 ]] && { echo "❌ No chapter files found in manuscript/."; exit 1; }

INPUTS=("${CHAPTERS[@]}")
if $EXTRAS; then
  # The end marker closes the story; back matter follows it, as it should.
  printf '::: theend\n:::\n' > "$TMPDIR_BUILD/theend.md"
  INPUTS+=("$TMPDIR_BUILD/theend.md")
  for extra in manuscript/998_*.md manuscript/999-*.md; do
    [[ -f "$extra" ]] && INPUTS+=("$extra")
  done
fi

# ------------------------------------------------------------
# 🔢 Word count, rounded the way Shunn asks
# ------------------------------------------------------------
RAW_WORDS=$(pandoc "${CHAPTERS[@]}" -t plain --wrap=none | wc -w | tr -d ' ')

if   (( RAW_WORDS < 17500 )); then STEP=100     # short story: nearest hundred
elif (( RAW_WORDS < 40000 )); then STEP=500     # novella: nearest five hundred
else                               STEP=1000    # novel: nearest thousand
fi
ROUNDED=$(( (RAW_WORDS + STEP / 2) / STEP * STEP ))
GROUPED=$(printf '%d' "$ROUNDED" | sed -e :a -e 's/\(.*[0-9]\)\([0-9]\{3\}\)/\1,\2/;ta')
WORDCOUNT="about ${GROUPED} words"
echo "🔢 ${RAW_WORDS} words → ${WORDCOUNT}"

# ------------------------------------------------------------
# ⚙️ Build
# ------------------------------------------------------------
mkdir -p "$OUTDIR"

SUFFIX="manuscript"
$CLASSIC && SUFFIX="manuscript_classic"
OUTFILE="$OUTDIR/${BOOK_TITLE}_${VERSION}_${SUFFIX}.pdf"

echo "⚙️ Building Shunn-format PDF version $VERSION..."

PANDOC_ARGS=(
  "${INPUTS[@]}"
  --from=markdown
  --metadata-file="$META"
  --template="$TEMPLATE"
  --lua-filter="$FILTER"
  --resource-path="manuscript:images:."
  --pdf-engine=xelatex
  --variable=mainfont:"$MAINFONT"
  --variable=papersize:"$PAPERSIZE"
  --variable=wordcount:"$WORDCOUNT"
  --output="$OUTFILE"
)
$CLASSIC   && PANDOC_ARGS+=(--metadata=classic:true)
$TITLEPAGE && PANDOC_ARGS+=(--variable=titlepage:true)

pandoc "${PANDOC_ARGS[@]}"

echo
echo "🎉 PDF built successfully:"
echo "   → $OUTFILE"
echo

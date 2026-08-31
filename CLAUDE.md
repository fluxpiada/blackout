# The Blackout: Weak Signals

A dystopian SF novel by F. J. S. Remmelzwaal, written in Markdown and built to
EPUB and PDF with pandoc. The prose is the product; the tooling serves it.

## Layout

```text
manuscript/??_*.md    The twelve chapters — this glob is exactly the book
manuscript/draft/     Unfinished material, not built
epub/                 EPUB build script, metadata, CSS
pdf/                  Shunn manuscript-format PDF build
index.html            The live website — served raw from main (see below)
styles/site.css       Its stylesheet, shared with templates/page.html
versions/             Build output — GITIGNORED, never commit artifacts here
wiki/                 How-to docs
```

## Builds

```bash
epub/bake_book_epub.sh          # or --auto for the latest v* tag
pdf/bake_book_pdf.sh            # Shunn manuscript format; --font=, --a4, --classic
```

Both must be run **from the repo root** and both write to `versions/`.
Publishing is tag-driven: push a `v*.*.*` tag and CI attaches both files to the
GitHub Release. See `wiki/publish_workflow.md`.

## Things that will mislead you

**The website has no build step.** GitHub Pages is configured to serve the
`main` branch at `/` directly (`build_type: legacy`, `source: {branch: main,
path: /}`). Edit `index.html` and push — it is live. There is no `gh-pages`
deployment in play; a `pages.yml` workflow that built into that branch was
deleted because Pages never served it, and every Pages build in the API history
came from a `main` commit.

The page used to live at `/blackout/site/` with a redirect shim at the root.
That was flattened: `site/index.html` is now the root `index.html`, and
`/blackout/site/` no longer exists.

**The Download ePub button in `site/index.html` is hardcoded** to
`releases/download/v1.11.28/Blackout_Weak_Signals_v1.11.31.epub`. The version
mismatch is deliberate and correct — the v1.11.31 EPUB was attached to the
v1.11.28 release after the fact. It works today but will go stale on the next
release. Tracked as an issue; do not "fix" the mismatch as if it were a typo.

**`--auto` uses `git describe --match='v*'`, not a bare `git describe`.** Bare
describe returns the closest tag by commit distance, which picked up the
`backup/*` tags and — because of the slash — wrote output into a subdirectory.
Keep the match pattern.

**`versions/*` is gitignored.** Build artifacts live on GitHub Releases, not in
the repo. Never `git add` them.

## Manuscript conventions

* Chapters open with `# Chapter IX - The Fjord`
* Scene breaks are `## ~ * ~` or `## ~ *** ~` — `pdf/shunn.lua` normalises every
  variant to a centred `#`
* `03_The_Cove.md` writes its dividers as bare `~ * ~` without the `##`, which
  pandoc mis-parses as a definition list. The filter repairs it; the EPUB does
  not, so those two lines are still wrong in the EPUB
* `10_Phil.md` contains stray U+2028 separators from a word processor. The PDF
  filter converts them to spaces; the EPUB does not
* Notes-to-self go in `<!-- HTML comments -->` — pandoc drops these from every
  output format. Do not leave them as blockquotes or bare prose

## Working here

* Prose belongs to the author. Do not edit chapter text, fix her spelling, or
  "improve" her style unless explicitly asked. Formatting and build tooling are
  fair game
* Issues labelled **`author-only`** are hers. Do not analyse, plan, or act on
  them
* This repo is public. Never commit personal contact details — see
  `pdf/manuscript.yaml`, whose address and phone lines are deliberate
  placeholders

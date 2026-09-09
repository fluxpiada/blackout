# The Blackout: Weak Signals

A dystopian science-fiction novel by **F. J. S. Remmelzwaal** — man against
machine gone amok, set on a recognisable Earth.

The manuscript is written in Markdown, kept under version control, and built to
two outputs with [pandoc](https://pandoc.org): an **EPUB** for reading and a
**Shunn manuscript-format PDF** for submission.

## Read it

* **Download the ePub** — <https://fluxpiada.github.io/blackout/>
* **Every release** — [Releases](https://github.com/fluxpiada/blackout/releases)
* **Talk about it** — [Discussions](https://github.com/fluxpiada/blackout/discussions)

The download page is served straight from `main` by GitHub Pages. There is no
site build step: edit `index.html`, push, and it is live.

## Layout

```text
manuscript/??_*.md    The twelve chapters — this glob is exactly the book
manuscript/draft/     Unfinished material, not built
epub/                 EPUB build script, metadata, CSS
pdf/                  Shunn manuscript-format PDF build
images/               Cover art and in-text images
index.html            The live download page — served raw from main
styles/site.css       Its stylesheet
versions/             Build output — gitignored, never committed
wiki/                 How-to docs
LICENSE               GPL-3 — the tooling
LICENSE-BOOK          CC BY-NC-ND 4.0 — the book
```

Chapters open with `# Chapter IX - The Fjord`. Scene breaks are `## ~ * ~`,
normalised to a centred `#` by `pdf/shunn.lua`. Notes-to-self go in
`<!-- HTML comments -->`, which pandoc drops from every output format.

## Build it

Both scripts must be run **from the repo root**, and both write to `versions/`.

```bash
epub/bake_book_epub.sh          # prompts for a version, or --auto for the latest v* tag
pdf/bake_book_pdf.sh            # Shunn manuscript format
```

The PDF build takes `--font=`, `--a4`, `--classic`, `--title-page` and
`--with-extras`; run it with `--help` for the full list, or see
[`wiki/shunn_pdf_format.md`](wiki/shunn_pdf_format.md).

**Prerequisites:** pandoc, XeLaTeX (for the PDF), and Node 20 (the EPUB build
pulls the release history from the GitHub API).

You do not need to build anything by hand to publish — see below. Build locally
only when you want to check something before tagging.

## Publish

Publishing is **tag-driven**. Pushing a `v*.*.*` tag is what triggers everything:

```bash
git tag -a v1.MM.DD -m "Release v1.MM.DD"
git push origin v1.MM.DD
```

GitHub Actions then builds the EPUB and the PDF and attaches both to the
Release. Artifacts live on Releases, never in the repo.

Full details, including what each workflow does and where every setting lives:
[`wiki/publish_workflow.md`](wiki/publish_workflow.md).

## Analysing the prose

Readability, pacing and vocabulary analysis lives in a separate repository,
[readability-stats](https://github.com/fluxpiada/readability-stats), which reads
a folder of `.md` chapters directly. See [`wiki/readability.md`](wiki/readability.md).

## Licensing

**This repository contains two different works under two different licences.
Please read this before reusing anything.**

### The tooling is yours — GPL-3

The build and publishing machinery — `epub/`, `pdf/`, `styles/`, `wiki/`,
`.github/workflows/` and `index.html` — is licensed under the
[GNU General Public License v3](LICENSE).

Take it. It is a complete, working setup for writing a book in Markdown under
Git and publishing it: two pandoc pipelines, a Shunn-compliant LaTeX template
and filter, tag-triggered release automation, and a download page. If you want
to publish your own book this way, you are welcome to the whole thing.

> A generic, book-agnostic version of this tooling is being extracted into its
> own template repository so you can start from a clean slate rather than
> deleting someone else's novel. Until it lands, this repository is the source.

### The book is not — CC BY-NC-ND 4.0

The novel itself — everything in `manuscript/`, `images/`, `scans/` and
`research/`, and the EPUB and PDF built from them — is
© 2025 F. J. S. Remmelzwaal and licensed
[CC BY-NC-ND 4.0](LICENSE-BOOK).

You may read it and share it unchanged, with attribution, for non-commercial
purposes. You may not sell it, and you may not publish an altered version.

GitHub's sidebar can only display one licence for a repository, and it shows the
GPL. That badge describes the tooling, not the story.

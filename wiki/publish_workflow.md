# Publishing workflow

**Publishing is tag-driven.** You don't build release artifacts by hand and you
don't commit them — you push a tag, and GitHub Actions builds the EPUB and the
PDF and attaches both to the Release.

Build locally only when you want to *check* something before tagging.

---

## 1. Build locally (optional, for checking)

### EPUB

```bash
epub/bake_book_epub.sh            # prompts for a version number
epub/bake_book_epub.sh --auto     # uses the latest git tag
```

→ `versions/Blackout_Weak_Signals_<version>.epub`

### PDF (Shunn manuscript format)

```bash
pdf/bake_book_pdf.sh              # prompts for a version number
pdf/bake_book_pdf.sh --auto       # uses the latest git tag
```

→ `versions/Blackout_Weak_Signals_<version>_manuscript.pdf`

See [shunn_pdf_format.md](shunn_pdf_format.md) for the PDF options — font,
paper size, Shunn Classic, title page.

> `versions/` is in `.gitignore`. Built files stay local; the Release is the
> place artifacts live. Don't `git add` them.

---

## 2. Publish a release

Replace `1.MM.DD` with the actual version.

```bash
# 1. Commit your manuscript changes as normal
git add manuscript/
git commit -m "Chapter XII revisions"

# 2. Tag it — one tag per archived version
git tag -a v1.MM.DD -m "Release v1.MM.DD"

# 3. Push the commit and then the tag
git push origin HEAD
git push origin v1.MM.DD
```

Pushing the tag is what triggers everything. Watch it run:

```bash
gh run watch
gh release view v1.MM.DD      # once it finishes
```

---

## 3. What the automation does

| Workflow | Trigger | Result |
| --- | --- | --- |
| `bake_epub.yml` | `v*.*.*` tag, or manual | Builds the EPUB, attaches it to the Release |
| `bake_pdf.yml` | `v*.*.*` tag, or manual | Builds the Shunn PDF, attaches it to the Release |

Both bake workflows also accept `workflow_dispatch`, so you can run either from
the Actions tab without tagging. `bake_pdf.yml` exposes the paper size, title
page and Classic options as inputs there.

Before building the EPUB, CI generates two files that are **not** committed:

* `manuscript/001_releases.md` — release history, from the GitHub API
* `manuscript/build_info.md` — build timestamp and commit hash

See [baking_epub_process.md](baking_epub_process.md) for the EPUB pipeline in
detail.

### The website

There is no site build step. GitHub Pages is configured to serve the `main`
branch at `/` directly, so the site is just the raw files in the repo:

* `index.html` — the download page at <https://fluxpiada.github.io/blackout/>
* `styles/site.css` — its stylesheet (dark-mode aware; also used by
  `templates/page.html`)
* `images/` — the cover art the page and its share card reference

Edit those files and push to `main`; the change is live. (A `pages.yml` workflow
used to build into a `gh-pages` branch, but Pages never served that branch, so
the workflow was doing nothing and has been removed.)

---

## 4. Where the settings live

| File | Controls |
| --- | --- |
| `epub/metadata.xml` | EPUB title, author, rights, description |
| `epub/style.css` | EPUB styling |
| `images/cover.png` | EPUB cover |
| `pdf/manuscript.yaml` | PDF cover sheet: byline, running header, contact block, font |
| `pdf/shunn.latex` | The PDF page format itself |

---

## 5. Manual pandoc (reference only)

The bake scripts exist so you don't have to do this. Kept only for when you need
to debug a build:

```bash
pandoc manuscript/*.md \
  --resource-path="manuscript:images" \
  --epub-cover-image=images/cover.png \
  --epub-metadata=epub/metadata.xml \
  --toc --toc-depth=1 \
  -o versions/Blackout_Weak_Signals_manual.epub
```

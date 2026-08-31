# The Blackout — PDF Baking Process (Shunn Manuscript Format)

*How the submission-ready PDF is built, and what makes it "correct".*

The PDF for **The Blackout: Weak Signals** is generated in [Shunn Modern
Manuscript Format](https://www.shunn.net/format/story/) — the layout editors and
agents expect from a submission. This is deliberately *not* a typeset book: it is
a plain, double-spaced reading copy designed to be marked up.

---

## 1. Quick start

```bash
pdf/bake_book_pdf.sh                 # prompts for a version number
pdf/bake_book_pdf.sh --auto          # takes the version from the latest git tag
```

Output lands in `versions/Blackout_Weak_Signals_<version>_manuscript.pdf`.

### Options

| Flag | Effect |
| --- | --- |
| `--auto` | Version from the latest git tag (used by CI) |
| `--version=VER` | Use `VER` as the version string |
| `--font=NAME` | Typeset in `NAME` for this build |
| `--list-fonts` | List the font families installed on this machine |
| `--classic` | [Shunn Classic](https://www.shunn.net/format/classic/): monospace face, emphasis **underlined** instead of italic |
| `--a4` | A4 paper instead of the US Letter the spec assumes |
| `--title-page` | Novel format: a separate title page; page 1 becomes the first page of text |
| `--with-extras` | Append acknowledgments and appendix *after* the end marker |

---

## 2. What the format actually requires

Every rule below is enforced by `pdf/shunn.latex`:

* One-inch margins on all four sides
* 12pt Times New Roman (Shunn Classic: Courier New), black only
* Double-spaced throughout, with **no** extra space between paragraphs
* First line of every paragraph indented half an inch
* Left-aligned with a ragged right margin — never justified
* No hyphenation; one space between sentences
* Contact information in the upper-left of page one; word count, rounded, upper-right
* Title a third of the way down page one, byline double-spaced below it
* Running header `Surname / Keyword / Page` in the upper-right of every page
  **except** the first
* Scene breaks as a centred `#`
* End of manuscript as a centred `# # #`

Word count is measured from the chapter files at build time and rounded the way
Shunn asks — to the nearest 100 for a short story, 500 for a novella, 1,000 for a
novel — then printed as "about N words".

---

## 3. Setting the font

The font lives in `pdf/manuscript.yaml`:

```yaml
mainfont: "Times New Roman"
```

It ships commented out. Uncomment it and put any family installed on your
machine — the name must match **exactly** as the system reports it. To see what
you have:

```bash
pdf/bake_book_pdf.sh --list-fonts
```

To try one without editing the file:

```bash
pdf/bake_book_pdf.sh --font="Georgia"
```

Resolution order is `--font=` → `mainfont:` → the built-in fallback chain. A font
you asked for that isn't installed is a hard error, never a silent substitution —
so a typo can't quietly change how the manuscript paginates.

Leaving `mainfont:` commented out gives you the fallback chain: Times New Roman
where it exists, else Liberation Serif / Nimbus Roman / TeX Gyre Termes. That's
what lets a CI box without the Microsoft fonts paginate near-identically to your
Mac. `--classic` swaps the chain for monospace faces (Courier New first). Setting
a font explicitly overrides the chain in both modes, while `--classic` still
controls whether emphasis is underlined.

**Stay within the spec.** Shunn asks for a plain, readable 12pt serif in black
and explicitly warns off sans-serif and "anything flashy or unusual". Changing
`mainfont` to Helvetica will build fine and will read as a mistake to an editor.

Point size is not a setting: 12pt is fixed in `pdf/shunn.latex` because the
format requires it.

---

## 4. Your contact details

`pdf/manuscript.yaml` holds the cover-sheet data: title, byline, the surname and
keyword used in the running header, and the contact block.

**The address and phone lines ship as bracketed placeholders.** Fill them in
before sending the manuscript anywhere. Per Shunn, do not add a national
insurance or tax number.

---

## 5. Files

```text
pdf/bake_book_pdf.sh   # build script: font probe, word count, pandoc invocation
pdf/shunn.latex        # pandoc LaTeX template — the format itself
pdf/shunn.lua          # pandoc filter — normalises the manuscript's own conventions
pdf/manuscript.yaml    # contact block, byline, running-header text
```

### What the filter normalises

The manuscript uses a few conventions of its own that have to be translated into
manuscript furniture:

| In the Markdown | In the PDF |
| --- | --- |
| `# Chapter IX - The Fjord` | New page, title dropped a quarter down, centred |
| `## ~ * ~` / `## ~ *** ~` | A centred `#` scene break |
| bare `~ * ~` on its own line | Also a scene break — see below |
| a fenced code block | Centred screen text in the body font |
| `::: theend :::` | The centred `# # #` end marker |

Two source quirks the filter works around, so you don't have to edit the
manuscript:

* **`03_The_Cove.md` writes its dividers as bare `~ * ~` lines** without the `##`
  prefix. Pandoc reads those as a *definition list* hanging off the paragraph
  above, which mangles them — in the old EPUB they came out wrong. The filter
  detects that shape and restores both the paragraph and the scene break. If you
  ever want to fix it at source, prefix those lines with `##` to match the other
  chapters.
* **`10_Phil.md` contains four invisible U+2028 line separators**, pasted in from
  a word processor. No text font has a glyph for them, so they'd otherwise
  produce "Missing character" warnings and dropped spaces. The filter converts
  them to ordinary spaces. **This affects the EPUB too** — worth stripping from
  the source.

---

## 6. Which files go in

`manuscript/??_*.md` — exactly the twelve chapter files. The glob deliberately
skips:

* `00-frontmatter.md` — a web title page with an image and release links; the
  Shunn cover sheet replaces it
* `001_releases.md` — the release log
* `998_Acknowledgments.md`, `999-appendix.md` — back matter, added only with
  `--with-extras`, and then placed after the `# # #`

---

## 7. Automation

`.github/workflows/bake_pdf.yml` mirrors the EPUB workflow: it runs on a `v*.*.*`
tag push or on demand, installs Pandoc and XeLaTeX, bakes the PDF, sanity-checks
the output, uploads it as a build artifact, and attaches it to the GitHub Release
when triggered by a tag.

CI runs on Ubuntu, where Times New Roman and Courier New don't exist. The build
script probes for a font it can actually use — falling back to Liberation Serif
and Liberation Mono, which are metrically compatible with Times and Courier — so
local and CI builds paginate near-identically.

---

## 8. Notes-to-self in the manuscript

Wrap anything meant for your eyes only in an HTML comment. Pandoc drops these
from **every** output format — PDF, EPUB and the web build alike:

```markdown
<!-- write up that Phil is gone -->
```

Chapter XI already uses this, including for a multi-paragraph passage parked for
later (`11_Zoning_For_Success.md:62`). Two notes in Chapter XII used to render as
story text and have been converted:

* `12_VisaPass.md:5` — was `> [!] TIP` / `- Rando busker`, rendering as a
  blockquote mid-scene
* `12_VisaPass.md:52` — was `*** rando busker punk exits before them`, rendering
  as ordinary prose

Both are now comments, so the reminders survive in the source while staying out
of the built manuscript. Note that "a rando busker or two" in `09_The_Fjord.md`
is real prose, not a note — leave it be.

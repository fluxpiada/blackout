# The Blackout — EPUB Baking Process

*A technical overview of how the automated EPUB build system works.*

This document explains how the EPUB for **The Blackout: Weak Signals** is automatically generated using GitHub Actions and a custom build script. It covers directory structure, release-history generation, build metadata stamping, and the final EPUB output workflow.

---

## 1. Repository Structure (Relevant Parts)

The EPUB build process relies on the following directories:

```
manuscript/       # All chapter .md files + auto-generated build_info.md
images/           # Cover + illustrations
epub/             # Build metadata, scripts, and template files
versions/         # Final output: versioned EPUB files
```

Two key scripts live in `epub/`:

* `make_releases_md.js` — generates a release history file from GitHub Releases API
* `bake_book_epub.sh` — the main build script invoked by GitHub Actions

---

## 2. Automated Workflow Overview

GitHub Actions handles the complete EPUB build pipeline:

1. Checkout repository
2. Install Node.js (for release-history script)
3. Install Pandoc
4. Generate GitHub release history
5. Generate build metadata (timestamp + commit hash)
6. Run the EPUB baking script
7. Upload EPUB to GitHub Release (only when triggered by a tag)

This ensures reproducible builds and guarantees that every EPUB contains information about *when* and *from which commit* it was created.

---

## 3. Release History Generation

Before building, the workflow executes:

```
node epub/make_releases_md.js
```

This script queries the GitHub API and writes:

```
manuscript/001_releases.md
```

The file contains entries like:

```
- v1.4.0 — 2025-01-18
- v1.3.0 — 2024-12-10
```

Because Pandoc ingests all `.md` files in `manuscript/`, this history automatically appears in the final EPUB.

---

## 4. Build Metadata Injection

The workflow generates an additional transient file:

```
manuscript/build_info.md
```

Its contents are created dynamically:

* Build timestamp (UTC)
* Commit hash (short form)

Example:

```
# Build Information

- Build timestamp: 2025-02-16 21:42 UTC
- Commit: 9275486
```

This improves traceability and helps you identify exactly which version of the repo an EPUB came from.

The file is **not committed**; it’s created only during the workflow run.
You can ignore it by adding:

```
manuscript/build_info.md
```

to `.gitignore`.

---

## 5. Main EPUB Build Script

The workflow runs:

```
epub/bake_book_epub.sh --auto
```

This script:

1. Determines the version (from the tag or via `--auto`)
2. Prepares the output directory `versions/`
3. Calls Pandoc with correct resource paths
4. Produces an EPUB named:

```
versions/Blackout_Weak_Signals_<version>.epub
```

Pandoc pulls content from:

* `manuscript/*.md`
* `images/`
* `epub/metadata.xml`

Including the dynamically generated files.

---

## 6. Publishing (When Triggered by a Tag)

If the workflow was triggered by pushing a tag shaped like `v1.4.0`, GitHub Actions:

* Creates a GitHub Release (if one doesn’t exist)
* Uploads the generated EPUB from `versions/`

This automates your full release pipeline.

---

## 7. Summary

The EPUB baking system is designed to be:

* **Deterministic** — Each EPUB is linked to a specific commit and timestamp
* **Automated** — Manual work reduced to pushing a tag
* **Modular** — Scripts cleanly separated from manuscript
* **Traceable** — Each release notes what source it was built from

The output EPUB always includes:

* Release history (`001_releases.md`)
* Build metadata (`build_info.md`)
* All manuscript chapters
* Correct metadata + cover

This ensures a reproducible, transparent, and well-documented build process.

---

# TD;LR — EPUB Baking Process

- GitHub Actions builds your EPUB automatically.
- It pulls all chapters from `manuscript/` and assets from `images/`.
- Before building, it generates:
  - `001_releases.md` → full GitHub release history  
  - `build_info.md` → timestamp + commit hash  
- Both files are injected into the EPUB without being committed.
- `bake_book_epub.sh` runs Pandoc and outputs to `versions/`.
- Tagging a commit (`v1.4.0`) auto-creates a GitHub Release and uploads the EPUB.
- Result: fully automated, traceable, reproducible EPUB builds.

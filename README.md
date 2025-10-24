
# The Git–Pandoc Book Workflow

## Structure & Write (in Markdown)
Each chapter lives as a .md file in a GitHub repository. Markdown keeps it clean, portable, and diff-friendly — no proprietary clutter, just text and meaning.
## Version Control with Git
Every edit is a commit — you can branch off to test a rewrite, compare drafts, and roll back anytime. GitHub hosts the repo, synchronizing versions and providing Issues for notes, Pull Requests for collaborative edits, and Actions for automation.
## Build with Pandoc
When the manuscript’s ready for output, Pandoc becomes the compiler. It reads the Markdown and converts it into your chosen formats — EPUB for e-readers, PDF for layout proofs, DOCX for editors, even HTML for web previews.
You can define a YAML metadata file for title, author, cover, and styling.
A Makefile or GitHub Action can automate builds — so each push can regenerate the latest version of the book.
## Polish & Publish
GitHub Pages (or any CI/CD pipeline) can automatically host preview builds. The repository itself doubles as your creative archive — every word, every version, traceable forever.

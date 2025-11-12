# The Blackout – Rebuild Branch

This branch restructures the repository into three clear areas:

1. **content/** – manuscript and archival materials  
2. **build/** – scripts, templates, and EPUB output (manual build only)  
3. **.github/workflows/** – automated release and site updates  

Build manually:
```bash
chmod +x build/scripts/build_epub.sh
./build/scripts/build_epub.sh
```

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

# GIT for Creative Writing
## A. The Core Stack
* Git — the version control engine under GitHub. It tracks every change to your text, line by line, with commit history so you can roll back or compare versions anytime.
* GitHub — the remote host that syncs your local repo, lets you collaborate (or work across devices), and gives you features like Issues (to track edits or research), Pull Requests (to test rewrites), and Wikis (for notes or lore).
* Markdown — lightweight, plain-text formatting that plays beautifully with Git. You can write chapters in .md files, easily diff them, and export to EPUB or PDF later with tools like Pandoc or Jekyll.
Git LFS (Large File Storage) — optional, if your book has big assets (images, audio snippets, etc.), keeping the repo lean while storing media efficiently.
## B. The Workflow Magic
I'm essentially treating my book like software:
* Each chapter is a file (or branch).
* Each edit is a commit — timestamped and reversible.
* You can branch a new idea (say, an alternate ending), test it, and merge if it works.
* Issues act as a kind of personal editorial to-do list.
* Readers or beta editors could even submit Pull Requests later, suggesting changes.

Let me know what you think!

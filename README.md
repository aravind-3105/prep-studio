# Prep Studio

A personal Python and DSA interview revision workspace. Built with plain HTML, CSS, and JavaScript, with no runtime dependencies or external services.

## Use it

Open `dist/Prep Studio.html` directly in your browser for the single-file edition, or serve the site from this repository:

```sh
python3 -m http.server 8000 --directory dist
```

Then open http://localhost:8000.

## Features

- 13 searchable Python fundamentals sections, 10 Python-for-interviews sections, and 35 algorithms/data-structures sections (full NeetCode beginners course), with worked examples and interview traps.
- A cheat sheet tab with one compact Need/Remember card per topic, plus a jump list and a link from each lesson.
- Revision progress, saved topics, and personal notes per topic.
- A six-week roadmap with session checkboxes.
- Optional reveal-and-explain recall cards.
- JSON progress backup and restore, Markdown downloads, and print/PDF support.
- Responsive layouts, keyboard accessible controls, and a light/dark theme toggle.

Progress and the theme choice stay in localStorage in your browser. Local and hosted copies have separate progress. Export a backup from the header; import it on the roadmap page. If browser storage is blocked, progress lasts for the session and can still be exported. Progress backups and personal notes are not part of the repository.

## Edit and rebuild

Edit lesson content in `content/python-notes.md`, `content/interview-notes.md`, and `content/dsa-notes.md`, the cheat sheet in `content/cheatsheet.md`, and the schedule in `content/schedule.md`. Edit the interface in `dist/index.html`, `dist/style.css`, and `dist/app.js`. Cheat sheet headings use `## Title {lesson-id}` so each card links back to its lesson.

```sh
python3 build.py
node --check dist/app.js
node checks/verify.cjs
```

Python 3 and Node.js are only needed to rebuild and run the checks. The Markdown renderer uses the Python standard library and supports the constructs used by these notes.

`build.py` regenerates lesson data, downloadable Markdown, and the single-file HTML. Generated files are included so the site works immediately after cloning.

## Scope

Python fundamentals, Python-for-interviews tools, and the full NeetCode beginners DSA notes (arrays through DP and bits) are available now. Problem practice, coding exercises, and a code runner are still to come.

## Repository privacy

The intended repository is private and personal. Site hosting metadata, environment files, and progress exports are excluded by `.gitignore`. GitHub Pages deployment is defined in `.github/workflows/pages.yml`. Once Pages is enabled with GitHub Actions as its source, pushes to `main` rebuild, check, and publish `dist/`. The published study content is accessible to site visitors; personal progress and notes remain in each visitor's browser.

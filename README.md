# Muruga Sharanam — Thiruppugazh Song Catalog

A dependency-free static site for browsing the Thiruppugazh song catalog and creating shareable "bhajan lists". No build step, no framework, no package.json — plain HTML, CSS, and JavaScript.

## Pages

- **`index.html`** — the song catalog. Live search across titles/ragam/thalam/lyrics/YouTube links, a song detail overlay with lyrics, and URL deep-link filtering (`?tivs=…&name=…`).
- **`bhajan-lists.html`** — saved bhajan lists. Render list cards with visit counts, remove individual lists, or clear all. "+ Create Bhajan List" opens a selection modal in place (no navigation) and generates a full shareable link (`origin/?tivs=…&name=…`).

## Run the dev server

The site is fully client-side; serve the repo directory over HTTP:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/> (or <http://localhost:8000/bhajan-lists.html>).

## Project layout

| Path | Purpose |
| --- | --- |
| `index.html` | Song catalog, search, song overlay (served at `/` and `/index.html`) |
| `bhajan-lists.html` | Saved bhajan lists + create-list selection modal |
| `common.js` | Shared `BhajanLists` helpers (`get`/`save`/`clear`/`catalogUrl`/`recordVisit`) |
| `data/thiruppugazh.js` | `Thiruppugazh.load()` — fetches and parses the song database |
| `data/thiruppugazh.jsonl` | Song database (see `data/README.md` for the record schema) |
| `data/README.md` | Song database schema and conventions |

## Deployment

GitHub Pages (this repo) serves the `main` branch directly; push to deploy. Shared pages/scripts must stay relative-root-safe since there is no bundler.

## Making changes

- Shared logic belongs in `common.js` or `data/thiruppugazh.js`, not duplicated per page.
- Keep generated share URLs absolute (`origin/?…`) — no `index.html`, no `create=true`.
- After changes, run the full agent-browser test suite described in `AGENTS.md` and keep docs (`AGENTS.md`, `README.md`, `data/README.md`) in sync.
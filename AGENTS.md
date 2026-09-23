# AGENTS.md

## Project

Static site with no build step, framework, or package.json. Two pages, all client-side:

- `index.html` — song catalog table. Search box, song detail overlay, and URL deep-link filtering (`?tivs=…&name=…`). Served at both `/` and `/index.html`.
- `bhajan-lists.html` — saved lists (render cards, visit counts, remove, clear all) plus the "create bhajan list" selection modal (opens in place via `#open-selection`).

Shared JS loaded via `<script>` tags (classic scripts, globals only, no modules):

- `data/thiruppugazh.js` — `Thiruppugazh.load()` fetches + parses `data/thiruppugazh.jsonl`, returns `{ songs, byTiv }`.
- `common.js` — `BhajanLists` namespace wrapping `localStorage["bhajan_lists"]`: `get()`, `save(lists)`, `clear()`, `catalogUrl(search)`, `recordVisit(url, name)`. `catalogUrl()` builds the canonical absolute list URL (`origin/?…`, no `index.html`).

There is no lint/typecheck/test script. The only way to verify changes is in the browser (below).

## Testing with agent-browser

A dev server serves the repo at `http://localhost:8000`. Drive it with agent-browser:

```bash
# Use a worktree-scoped session so you don't hijack the shared browser
export AGENT_BROWSER_SESSION="$(agent-browser session id --scope worktree --prefix site-test)"

# Core loop
agent-browser open http://localhost:8000/<page>      # navigate
agent-browser wait --load networkidle                 # wait for page/lazy load of songs
agent-browser snapshot -i -c                          # interactive elements (fresh @eN refs each snapshot)
agent-browser click @eN     # or: agent-browser find text "..." click
agent-browser eval "document.getElementById('status').textContent"   # assert inline
agent-browser console                                 # MUST be empty after each case (uncaught js errors fail cases silently)
```

Notes:

- Songs are loaded async from `data/thiruppugazh.jsonl` (448 total). Always `wait --load networkidle` and assert `#status` shows `448 song(s)` before trusting a passed load.
- Sync waits: `agent-browser wait --fn "!document.getElementById('selection-overlay').classList.contains('hidden')"`.
- `confirm` dialogs (Clear All) block the page — resolve with `agent-browser dialog accept`.
- Reset saved data between runs: `agent-browser eval "localStorage.removeItem('bhajan_lists')"`.
- Elements are built dynamically by JS; use CSS selectors / `find text` rather than snapshot refs when asserting.

### Test cases

#### index.html — catalog

1. **Load**: status is `448 song(s)`, table has 448 `<tbody>#songs tr`, console empty.
2. **Search**: type "muruga" in `#search` → status drops (e.g. `3 of 448 song(s)`); clear → back to `448 song(s)`.
3. **Song overlay**: click any `.title` in the table → `#overlay` loses `hidden`, `#overlay-title` is non-empty; press `Escape` → `#overlay` gains `hidden`.
4. **Deep-link filter**: open `/?tivs=001,005&name=RefactorTest` → status `2 of 448 song(s)`, `#list-name-display` shows the name, `#overlay` stays hidden.
5. **Clear filter**: with a deep-link filter active, click `#clear-filter` badge → status back to `448 song(s)`.

#### bhajan-lists.html — create bhajan list modal

6. **Open modal**: on bhajan-lists.html click `#open-selection` (+ Create Bhajan List) → `#selection-overlay` loses `hidden`, `#selection-list` has 448 rows, URL unchanged (no navigation).
7. **Selection + count**: click first two `.song-check-row input` → `#selection-count` shows `2 song(s) selected`; `#select-all` → `#selection-count` shows `446` (unique TIVs; the data contains duplicate TIV rows, e.g. 398 and 399) while `#selection-meta` shows `448 of 448 song(s) selected`; `#deselect-all` → `0 song(s) selected`.
8. **Generate Link**: select 2 songs, set `#list-name-input` = "Test List", click `#selection-generate` → `#share-url` is the full **absolute** URL (e.g. `http://localhost:8000/?tivs=…&name=…`) with no `index.html` and no `create=true`; `localStorage.bhajan_lists` contains one entry `{name:"Test List", count:1}` with the same absolute `url`.
9. **Go to list**: click `#go-list` → lands on the generated `/?…` URL, status `2 of 448 song(s)`, `#list-name-display` = "Test List", and the stored entry count incremented.
10. **Copy**: click `#copy-link` → clipboard value equals `#share-url` value.
11. **Cancel/close**: `#selection-cancel` (or `Escape`) hides the overlay and restores scroll.

#### bhajan-lists.html

12. **Empty state**: with no saved lists, page shows `0 list(s)` and `.empty-state` "No bhajan lists yet…".
13. **Create button**: click `+ Create Bhajan List` → the selection modal opens in place; the URL stays `bhajan-lists.html` (→ case 6).
14. **Render**: with ≥1 saved list, a `.list-card` shows the name and "Visited N time(s)".
15. **Visit bump**: clicking a `.list-card-title` increments the stored count (it also navigates; click bumps +1, landing on the list page bumps +1, like production behavior).
16. **Remove**: `.btn-delete` deletes that entry; empty state returns after the last one.
17. **Clear All**: `#clear-all` shows a `confirm` dialog → `dialog accept` → storage emptied, page shows `0 list(s)`.

#### shared JS

18. **recordVisit create-branch**: open a deep link whose absolute `catalogUrl()` (e.g. `/?tivs=…&name=NewName`) is NOT yet stored → storage gains a `{name:"NewName", count:1}` entry with that absolute `url`.
19. **No leakage**: after every case, `agent-browser console` must be empty, and clean up with `localStorage.removeItem('bhajan_lists')`.

## Conventions

- Inline page scripts are IIFEs that reference the shared globals (`Thiruppugazh`, `BhajanLists`) — keep shared logic in `common.js` / `data/thiruppugazh.js`, not duplicated per page.
- URL generation (`generateLink`, in `bhajan-lists.html`) must emit an absolute, shareable link (`origin/?…` via `BhajanLists.catalogUrl`) — never reference `index.html` or emit a `create=true` param.
- Do not add a build step; the site is plain static HTML+JS.
- **Run the full test suite** (all cases in this file) with agent-browser after any JS/HTML change; also check `agent-browser console` stays empty.
- **Keep docs in sync**: update `README.md` (overview/layout), `data/README.md` (schema), and this file (tests/conventions) when a change affects them.
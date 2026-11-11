# App standards

What "done" means for an app on corey.sciu.to. New apps from this template start with the mechanical parts
in place; the rest is judgment. Each app's CLAUDE.md links here.

## Built into the template

- **Tests gate the deploy.** `.github/workflows/deploy.yml` runs the unit tests and the browser tests on every
  push to `main` and publishes to Pages only if they pass. Pages' source is "GitHub Actions", not the branch.
- **One shared workflow.** Each app's `deploy.yml` only calls `.github/workflows/app.yml@v1` here, with inputs
  for what differs (`site`, `stamp`, `python-test`, `after-build`). Change the steps in `app.yml`; for a
  breaking change, tag `v2` and move apps over one at a time. After a compatible change, move the `v1` tag.
- **Version stamp.** The workflow replaces `dev` in every `<span class="version" title="Version">` on the pages
  listed in `stamp` with `v1.<number of commits>` and writes `version.json`. Add the span to each page.
- **A reload gets the new version.** GitHub Pages lets browsers keep files for ten minutes, so the workflow
  (`.github/scripts/stamp.py`, tested by `test_stamp.py` beside it) adds `?v=<version>` to every reference from
  one file of the site to another: scripts, styles, images and data named in the stamped pages, and every
  relative `import`, `import()` and `new URL('./x.js', import.meta.url)` in the site's scripts. Data a script
  fetches by a built-up address can't be found that way: add the version yourself, from the page's version
  span, as `sounds/a.ogg?v=` + `document.querySelector('[title="Version"]').textContent`.
- **Desktop and phone.** Every browser test runs at both sizes. Tag a desktop-only test `@desktop`.
- **Accessibility.** `e2e/a11y.spec.js` runs axe on each page. Add new pages to its list.
- **Footer** with a contact address (`corey.sciuto+<app>@gmail.com`), a "More projects" link to
  https://corey.sciu.to/projects/, and the version. Every page shows them or links to a help page that does.
- **Link previews.** `og:` tags and `preview.png` (`npm run screenshot`), also used on the projects page.

## Judgment

- **Static site.** No build step and no framework unless there's a real need. Load libraries from a CDN,
  pinned to an exact version.
- **Logic in plain files** (math, parsing, data shaping) with no DOM, exported for Node with
  `if (typeof module !== 'undefined') module.exports = {...}` and unit-tested in `tests/*.test.js`.
- **Browser tests cover the main flows**, not just "it loads".
- **Everything worth sharing is in the URL.**
- **Visible text: labels, not sentences.** A note is one short line. Explanations go in a help page or the
  README.
- **American spelling** (center, color, kilometer) in text, code and docs. Keep proper names and quoted titles
  as written (Centre County, a source titled "The centre wheel").
- **AI disclosure:** one line under the README's Live link, `Built with [Claude Code](https://claude.com/claude-code).`
  (name the other tools too if others were used). The projects page footer says the same. Not in the app UI.
- **A short help page** once an app has more than a few controls, linked from the footer.
- **`ARCHITECTURE.md`: how it's built**, for an engineer reading the repo: what it runs on (browser APIs,
  libraries with versions, dev tools), the file layout with one line per file, how the pieces fit (a mermaid
  diagram), the core techniques and data formats, how it's tested and deployed, and known limits. Link it from
  the README's top and the help page footer ("How it's built"); the projects page links it automatically.
  Update it when the structure changes. [meowpiano's](https://github.com/csciuto/meowpiano/blob/main/ARCHITECTURE.md)
  is the model.
- **Fair use and data.** Credit data sources in the footer or help page; prefer public-domain or openly
  licensed data, and keep images small.
- **Every control answers a question.** Add features when there's a concrete question behind them; don't
  remove controls without asking.

## Working on these repos

- Commit and push freely once tests pass. Ask before deleting repos, force-pushing or rewriting history.
- Extend, don't rewrite. Ask before redesigning an app.
- After visible UI changes, run `npm run screenshot` and commit `preview.png`.
- After structural changes (new files, libraries, formats), update `ARCHITECTURE.md`.

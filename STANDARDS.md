# App standards

What "done" means for an app on corey.sciu.to. New apps from this template start with the mechanical parts
in place; the rest is judgment. Each app's CLAUDE.md links here.

## Built into the template

- **Tests gate the deploy.** `.github/workflows/deploy.yml` runs the unit tests and the browser tests on every
  push to `main` and publishes to Pages only if they pass. Pages' source is "GitHub Actions", not the branch.
- **Version stamp.** The workflow replaces `dev` in every `<span class="version" title="Version">` with
  `v1.<number of commits>`. Add the span to each page.
- **Desktop and phone.** Every browser test runs at both sizes. Tag a desktop-only test `@desktop`.
- **Accessibility.** `e2e/a11y.spec.js` runs axe on each page. Add new pages to its list.
- **Footer** with a contact address (`corey.sciuto+<app>@gmail.com`) and the version.
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
- **A short help page** once an app has more than a few controls, linked from the footer.
- **Fair use and data.** Credit data sources in the footer or help page; prefer public-domain or openly
  licensed data, and keep images small.
- **Every control answers a question.** Add features when there's a concrete question behind them; don't
  remove controls without asking.

## Working on these repos

- Commit and push freely once tests pass. Ask before deleting repos, force-pushing or rewriting history.
- Extend, don't rewrite. Ask before redesigning an app.
- After visible UI changes, run `npm run screenshot` and commit `preview.png`.

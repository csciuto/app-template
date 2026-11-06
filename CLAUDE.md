# __TITLE__

__DESCRIPTION__

Follow the app standards in [csciuto/app-template STANDARDS.md](https://github.com/csciuto/app-template/blob/main/STANDARDS.md).
In short: tests gate the deploy; logic in plain, unit-tested files; browser tests at desktop and phone size with
accessibility checks; footer with contact and version; labels, not sentences. Commit and push freely once
tests pass.

## This app

- Lives at https://corey.sciu.to/__NAME__/. `.github/workflows/deploy.yml` tests, stamps the version and
  publishes on every push to `main`.
- Keep `index.html` at the repo root. If the app moves (e.g. into `docs/`), update the repo's homepage URL, the
  `og:` tags, the workflow's version-stamp file list, and `APP`/`PREVIEW` in `e2e/smoke.spec.js`.
- `READY` in `e2e/smoke.spec.js` should be an element that only appears once the app has rendered.
- The repo's description, homepage URL and `corey-app` topic list it on https://corey.sciu.to/projects/. Keep
  the description to one plain sentence.

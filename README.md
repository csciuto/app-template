# __TITLE__

**Live:** [corey.sciu.to/__NAME__](https://corey.sciu.to/__NAME__/)

__DESCRIPTION__

## Development

No build step: plain HTML, CSS and JavaScript. Each push to `main` runs the tests in GitHub Actions and, if they
pass, publishes to GitHub Pages with a version stamp.

```bash
npm run serve                                     # http://localhost:8090
npm install && npx playwright install chromium   # first time only
npm test                                          # unit tests (node --test)
npm run test:e2e                                  # browser tests, desktop and phone, with accessibility checks
npm run screenshot                                # refreshes preview.png, used for link previews
```

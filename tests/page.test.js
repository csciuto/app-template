// Checks on the page itself: run with `node --test`. Put the app's logic in plain files and test it here too.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');

const html = fs.readFileSync(require.resolve('../index.html'), 'utf8');
// The template repo itself still has its placeholders; new-app deletes .template-README.md when it fills them.
const isTemplate = fs.existsSync(require('node:path').join(__dirname, '..', '.template-README.md'));

test('the template placeholders are all filled in', { skip: isTemplate }, () => {
  assert.doesNotMatch(html, /__[A-Z]+__/);
});

test('the page has a version stamp for the deploy to fill in', () => {
  assert.match(html, /<span class="version" title="Version">dev<\/span>/);
});

test('link-preview tags point at this app', { skip: isTemplate }, () => {
  assert.match(html, /<meta property="og:image" content="https:\/\/corey\.sciu\.to\/[^"]+\/preview\.png">/);
});

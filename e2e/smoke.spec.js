const { test, expect } = require('@playwright/test');

// Smoke test: the app loads and renders without JavaScript errors.
// `npm run screenshot` also saves preview.png, used for link previews
// and on https://corey.sciu.to/projects/.
const APP = '/';
const PREVIEW = 'preview.png';
const READY = '#app';

test('app loads without errors @desktop', async ({ page }) => {
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  await page.setViewportSize({ width: 1200, height: 630 });
  await page.goto(APP);
  await expect(page.locator(READY).first()).toBeVisible();
  expect(errors).toEqual([]);
  if (process.env.UPDATE_PREVIEW) {
    await page.waitForTimeout(750);
    await page.screenshot({ path: PREVIEW });
  }
});

test('footer shows a contact and the version', async ({ page }) => {
  await page.goto(APP);
  await expect(page.locator('footer')).toContainText('@gmail.com');
  await expect(page.locator('.version')).toHaveText(/^(dev|v1\.\d+)$/);
});

test('contact and a link back to the projects page', async ({ page }) => {
  for (const p of [APP]) {
    await page.goto(p);
    await expect(page.getByText(/corey\.sciuto\+\w+@gmail\.com/).first()).toBeAttached();
    await expect(page.locator('a[href="https://corey.sciu.to/projects/"]').first()).toBeAttached();
  }
});

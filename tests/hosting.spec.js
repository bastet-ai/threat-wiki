const { test, expect } = require('@playwright/test');

test('Workers preserves pages, directory URLs, search, feed, assets and 404s', async ({ request }) => {
  const home = await request.get('/');
  expect(home.status()).toBe(200);
  const html = await home.text();
  expect(html).toContain('threat.wiki');
  for (const match of html.matchAll(/(?:src|href)="([^"]+\.(?:css|js)(?:\?[^"]*)?)"/g)) {
    if (/^https?:/.test(match[1])) continue;
    expect((await request.get(match[1])).status(), match[1]).toBe(200);
  }
  const group = await request.get('/actors/teampcp/');
  expect(group.status()).toBe(200);
  expect(await group.text()).toContain('TeamPCP');
  const redirect = await request.get('/actors/teampcp', { maxRedirects: 0 });
  expect(redirect.status()).toBe(307);
  expect(redirect.headers().location).toBe('/actors/teampcp/');
  const search = await request.get('/search/search_index.json');
  expect(search.status()).toBe(200);
  const index = await search.json();
  expect(index.docs.length).toBeGreaterThan(100);
  expect(index.docs.some(doc => doc.location.startsWith('actors/teampcp/'))).toBe(true);
  const feed = await request.get('/feed.xml');
  expect(feed.status()).toBe(200);
  expect(await feed.text()).toContain('https://threat.wiki/');
  for (const path of ['/missing-migration-test/', '/AGENTS.md', '/TODO.md', '/.env', '/drafts/']) {
    expect((await request.get(path)).status(), path).toBe(404);
  }
});

const { test, expect, request } = require('@playwright/test');

const PAGE_PATH = '/ops/oracle-weblogic-cve-2024-21182-exploitation/';
const EXPECTED_SOURCE_URLS = [
  'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json',
  'https://www.oracle.com/security-alerts/cpujul2024.html#AppendixFMW',
  'https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-21182',
  'https://cveawg.mitre.org/api/cve/CVE-2024-21182'
];

function canonicalize(url) {
  const parsed = new URL(url);
  parsed.hash = '';
  return parsed.toString();
}

test.describe('WebLogic source links', () => {
  test('source URLs are rendered as clickable links and point to precise records', async ({ page }) => {
    await page.goto(PAGE_PATH);

    const sources = page.locator('article h2#sources').locator('xpath=following-sibling::*[preceding-sibling::h2[1][@id="sources"]]');
    await expect(page.locator('article h2#sources')).toBeVisible();

    const bareUrls = await sources.evaluateAll((nodes) => {
      const matches = [];
      const urlRe = /https?:\/\/[^\s<>)]+/g;
      for (const node of nodes) {
        const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, {
          acceptNode(textNode) {
            return textNode.parentElement?.closest('a') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
          }
        });
        while (walker.nextNode()) {
          const text = walker.currentNode.textContent || '';
          for (const match of text.matchAll(urlRe)) matches.push(match[0]);
        }
      }
      return matches;
    });
    expect(bareUrls, `bare, non-clickable source URLs: ${bareUrls.join(', ')}`).toEqual([]);

    const hrefs = await sources.locator('a[href^="http"]').evaluateAll((links) => links.map((link) => link.href));
    for (const expectedUrl of EXPECTED_SOURCE_URLS) {
      expect(hrefs.map(canonicalize)).toContain(canonicalize(expectedUrl));
    }
  });

  test('external source links resolve and contain CVE-2024-21182', async () => {
    const api = await request.newContext({ extraHTTPHeaders: { 'user-agent': 'threat-wiki-source-link-test/1.0' } });
    for (const sourceUrl of EXPECTED_SOURCE_URLS) {
      const response = await api.get(sourceUrl);
      expect(response.status(), `${sourceUrl} should return HTTP 200`).toBe(200);
      const body = await response.text();
      expect(body, `${sourceUrl} should contain CVE-2024-21182`).toContain('CVE-2024-21182');
    }
    await api.dispose();
  });
});

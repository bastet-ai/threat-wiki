const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 120_000,
  expect: { timeout: 10_000 },
  use: {
    baseURL: 'http://127.0.0.1:4174',
    browserName: 'chromium'
  },
  webServer: {
    command: 'uvx --from mkdocs-material mkdocs build --strict && python3 -m http.server 4174 -d site',
    url: 'http://127.0.0.1:4174',
    reuseExistingServer: !process.env.CI,
    timeout: 180_000
  }
});

# Publishing notes

## 2026-10-09

- Preparing the Cloudflare Git connection exposed an existing strict-build failure on `c6d23b804fe617007275791809a1a590194fafd9`. GitHub validation failed at https://github.com/bastet-ai/threat-wiki/actions/runs/37977902444.
- Removed the navigation reference to `ops/ghostaction-github-actions-workflow-injection-git-history-credential-mining-stepsecurity-october-2026.md`, which has no tracked source file. No article source was removed; the original navigation entry remains in Git history.
- Cloudflare serves the existing `threat-wiki` Static Assets Worker at `threat.wiki`; Git connection and final deployment verification are in progress.

Validation: `npm run build`, `npm run deploy:check`, and `npm run test:hosting` passed. The hosting check covers pages, directory URLs, search, feed, assets, and 404 handling.

# Publishing notes

## 2026-10-09

- Preparing the Cloudflare Git connection exposed an existing strict-build failure on `c6d23b804fe617007275791809a1a590194fafd9`. GitHub validation failed at https://github.com/bastet-ai/threat-wiki/actions/runs/37977902444.
- Removed the navigation reference to `ops/ghostaction-github-actions-workflow-injection-git-history-credential-mining-stepsecurity-october-2026.md`, which had no tracked source file at that commit. No article source was removed; the original navigation entry remains in Git history. The repair is commit `042ac53bc6d52196a95a3651de4f3266d0743e35`; [GitHub validation passed](https://github.com/bastet-ai/threat-wiki/actions/runs/37982785940).
- Synced the later content update `7b1564c94df0759d6cdab602bc6c57a03fd031e2`, which adds the GhostAction article source. This publishing documentation update preserves that content and its generated tag index.
- Confirmed Cloudflare Workers Builds is enabled for `bastet-ai/threat-wiki`, production branch `main`, Worker `threat-wiki`, root `/`, included paths `*`, and preview builds disabled.
- The build command is `npm run build`; the deploy command is `npx wrangler deploy`. Checked-in `.node-version` and `.python-version` select the build runtimes.
- Cloudflare fetches and deploys repository commits using its GitHub app. The deployment credential stays in Cloudflare; no Cloudflare secrets were added to GitHub. No build variables or secrets were configured.
- GitHub Actions remains validation-only. Manual recovery must pause automatic builds and wait for running builds to finish before deploying; verify the site before re-enabling builds.
- Existing custom-domain configuration, DNS, and the previous GitHub Pages deployment remain available for recovery.

Local validation for the navigation repair: `npm run build`, `npm run deploy:check`, and `npm run test:hosting` passed. The hosting check covers pages, directory URLs, search, feed, assets, and 404 handling.

### First Git-triggered deployment verified

- Pushing commit [`2eea99b5947e1ed6574b1279e5ec2bef7c6feb9a`](https://github.com/bastet-ai/threat-wiki/commit/2eea99b5947e1ed6574b1279e5ec2bef7c6feb9a) triggered Cloudflare build `0207f721-6871-416d-bdbe-0aa7ae914b5d`, which succeeded and published Worker version `9a7f56de-77ad-43b2-b5a7-94285a3627a6`. GitHub validation for that commit also succeeded. Exact commit identity comes from Cloudflare build/version evidence, not from the HTTP checks alone.
- All nine public HTTPS checks passed against `https://threat.wiki/` at 20:13 UTC: homepage, `/actors/teampcp/`, both canonical URLs, a 307 trailing-slash redirect, linked CSS, a valid search index with 13,310 entries including the article, a valid RSS feed, and a real 404 for a missing page. Certificate verification remained enabled.

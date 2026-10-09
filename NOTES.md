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

Verification pending: a push-triggered Cloudflare build for the documentation commit, its deployed commit/build identifier, and public HTTPS checks after that deployment. Connection settings alone do not prove the complete deployment path.

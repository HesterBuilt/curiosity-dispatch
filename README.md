# The Curiosity Dispatch

A personal news and road-adventure dashboard, separate from HFM Industry Intelligence. Static GitHub Pages website with a six-hour GitHub Actions RSS refresh, topic filters, local browser bookmarks, and a curated Explorer's Atlas.

## Publish

1. Create a **new public** repository named `curiosity-dispatch` in your GitHub account. Do not upload personal secrets.
2. Upload `index.html`, `news.json`, `update_feeds.py`, and `.github/workflows/update-news.yml`, preserving the folder path. GitHub Desktop or Git works best for hidden `.github` folders.
3. In the new repository, choose **Actions > Update Curiosity Dispatch > Run workflow**. It fetches public RSS results and commits `news.json`.
4. Choose **Settings > Pages > Deploy from a branch > main > /(root) > Save**.
5. Your published site should be `https://YOUR-USERNAME.github.io/curiosity-dispatch/`.
6. Optionally paste the published URL into Notion using `/embed`.

## Important

- GitHub Actions schedules are approximate and can be delayed or disabled by GitHub inactivity policies.
- News results use Google News RSS search queries and may be incomplete, duplicated across topics, stale or blocked. Sources and article claims must be checked independently.
- Atlas entries are **curated starting points**, not a verified current-access directory. Travel tiers are rough planning categories based on the Gainesville, Georgia area, not calculated routes. Check directions, opening status, permits and road conditions before visiting.
- Saved articles are stored in each browser's localStorage, not synced between devices.
- Change news topics by editing `QUERIES` in `update_feeds.py`; change places in the `places` array in `index.html`.
- The dashboard has no paid dependencies or credentials. The new repository is separate from `hfm-industry-intelligence`.

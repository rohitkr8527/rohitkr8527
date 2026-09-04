# Unified GitHub Profile + Engineering Activity Design

## Goal
Create a recruiter-friendly GitHub profile for Rohit Kumar focused on AI/ML Engineering, Data Science, and Applied AI, with a single merged GitHub + GitLab engineering activity visualization.

## Visual direction
- Dark, GitHub-compatible visual system.
- No emoji section headings.
- Use real technology logos and compact badges.
- Prioritize About, core focus, tech stack, and selected work before activity metrics.
- One section called `Engineering Activity`; never split GitHub and GitLab activity into separate sections.

## Activity architecture
- Fetch GitHub contribution-calendar counts by date through GitHub GraphQL.
- Fetch GitLab user events using a read-only personal access token stored as `GITLAB_TOKEN` in GitHub Actions.
- Private GitLab activity may contribute to aggregate daily counts, but project names, URLs, titles, commit messages, and other private metadata must never be written to generated public files.
- Normalize both sources into date -> integer-count maps.
- Merge source counts per day and publish only aggregate date/count data.
- Generate a custom activity heatmap SVG and a custom animated snake SVG from the same merged dataset.
- Run generation daily via GitHub Actions and commit only generated public assets.

## Privacy rules
Public generated JSON contains only:
- date
- github count
- gitlab count
- total count

It must never contain:
- private GitLab project names
- project IDs or URLs
- commit messages
- issue/MR titles
- author metadata
- access tokens

## Repository files
- `README.md` — final profile README.
- `scripts/activity.py` — fetch, normalize, merge, stats, and public serialization.
- `scripts/render.py` — custom SVG heatmap and animated snake rendering.
- `scripts/update_profile.py` — orchestration entrypoint.
- `tests/test_activity.py` — deterministic unit tests.
- `.github/workflows/update-profile.yml` — scheduled generation workflow.
- `assets/hero.svg` — profile hero artwork.
- `assets/engineering-activity.svg` — generated merged heatmap.
- `assets/engineering-snake.svg` — generated merged animated snake.
- `assets/unified-activity.json` — privacy-safe merged data.

## Data semantics
GitHub uses GitHub's contribution-calendar daily counts. GitLab uses available user Events API activity; push events count their reported `commit_count` when present, otherwise each event contributes one activity unit. The resulting visualization is named `Engineering Activity`, not an exact cross-platform contribution ledger.

## Failure behavior
- Missing `GITLAB_TOKEN`: GitLab fetch fails with a clear error in CI; the user must configure the secret.
- Temporary GitHub/GitLab API error: the workflow fails rather than silently publishing misleading zero activity.
- Missing dates: represented as zero.
- Any event parsing anomaly: ignore unknown metadata and retain only the date/count needed for aggregation.

## Verification
- Unit tests cover GitLab privacy normalization, push-event counting, date merging, streak statistics, and SVG rendering.
- A local sample generation run must produce parseable JSON and SVG assets.

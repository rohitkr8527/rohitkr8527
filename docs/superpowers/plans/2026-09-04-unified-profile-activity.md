# Unified Profile Activity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a premium GitHub profile package with one privacy-safe GitHub + GitLab engineering activity graph and matching snake animation.

**Architecture:** Python standard-library scripts fetch GitHub GraphQL contribution counts and GitLab Events API activity, normalize both into daily counts, merge them, and generate custom SVG assets. A scheduled GitHub Action regenerates assets daily; the README consumes only repository-local generated files plus selected public badge/logo services.

**Tech Stack:** Python 3.12 standard library, GitHub GraphQL API, GitLab REST Events API, SVG, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-04-unified-profile-activity-design.md`

## Global Constraints
- Do not expose private GitLab project names or metadata.
- Keep GitHub and GitLab activity visually merged into one `Engineering Activity` section.
- No emoji headings.
- Use generated repository-local activity assets.
- Environment/secrets contain only secrets; usernames and visual configuration stay in code/workflow arguments.

---

### Task 1: Activity normalization and merge
**Files:**
- Create: `tests/test_activity.py`
- Create: `scripts/activity.py`

**Interfaces:**
- Produces: `normalize_gitlab_events(events) -> dict[str, int]`
- Produces: `merge_activity(github, gitlab, start, end) -> list[dict]`
- Produces: `compute_stats(rows) -> dict[str, int]`

- [ ] Write tests for GitLab push counting, privacy-safe normalization, daily merging, and streak calculations.
- [ ] Run tests and confirm they fail because implementation is missing.
- [ ] Implement minimal activity helpers.
- [ ] Run tests and confirm they pass.

### Task 2: SVG rendering
**Files:**
- Modify: `tests/test_activity.py`
- Create: `scripts/render.py`

**Interfaces:**
- Consumes merged rows from Task 1.
- Produces: `render_heatmap(rows, stats) -> str`
- Produces: `render_snake(rows) -> str`

- [ ] Add tests that require valid SVG structure and expected labels.
- [ ] Run tests and confirm rendering tests fail.
- [ ] Implement heatmap and animated snake SVG generation.
- [ ] Run tests and confirm they pass.

### Task 3: API fetch and orchestration
**Files:**
- Modify: `scripts/activity.py`
- Create: `scripts/update_profile.py`
- Create: `.github/workflows/update-profile.yml`

**Interfaces:**
- `fetch_github_activity(username, token, start, end) -> dict[str, int]`
- `fetch_gitlab_activity(username, token, start, end) -> dict[str, int]`

- [ ] Add deterministic tests for API response parsers.
- [ ] Run tests and confirm parser tests fail.
- [ ] Implement fetchers and parsers using Python standard library HTTP clients.
- [ ] Implement orchestrator and workflow.
- [ ] Run all tests.

### Task 4: README and visual assets
**Files:**
- Create: `README.md`
- Create: `assets/hero.svg`
- Generate: `assets/engineering-activity.svg`
- Generate: `assets/engineering-snake.svg`
- Generate: `assets/unified-activity.json`

- [ ] Create premium recruiter-oriented README with a single Engineering Activity section.
- [ ] Generate sample assets using deterministic sample data for package preview only.
- [ ] Verify README references existing paths and contains no private-source placeholders or separate GitLab activity section.

### Task 5: Final verification
- [ ] Run `python -m unittest discover -s tests -v`.
- [ ] Run `python scripts/update_profile.py --sample`.
- [ ] Parse generated JSON and both SVG files.
- [ ] Zip the package.

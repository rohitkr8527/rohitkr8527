from __future__ import annotations

import argparse
import json
import os
from datetime import date, timedelta
from pathlib import Path

from activity import compute_stats, fetch_github_activity, fetch_gitlab_activity, merge_activity
from render import render_heatmap, render_snake


def sample_counts(start: date, end: date) -> tuple[dict[str, int], dict[str, int]]:
    """Create deterministic preview-only data. Never used by the scheduled workflow."""
    github: dict[str, int] = {}
    gitlab: dict[str, int] = {}
    current = start
    i = 0
    while current <= end:
        if current.weekday() < 5:
            github[current.isoformat()] = (i * 3) % 5
            gitlab[current.isoformat()] = (i * 7) % 8
        elif i % 4 == 0:
            gitlab[current.isoformat()] = 1
        current += timedelta(days=1)
        i += 1
    return github, gitlab


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate unified GitHub + GitLab profile activity assets.")
    parser.add_argument("--github-user", default="rohitkr8527")
    parser.add_argument("--gitlab-user", default="rohitkr8527")
    parser.add_argument("--days", type=int, default=364)
    parser.add_argument("--sample", action="store_true", help="Generate deterministic preview data without network access.")
    parser.add_argument("--output", default="assets")
    args = parser.parse_args()

    end = date.today()
    start = end - timedelta(days=max(1, args.days))

    if args.sample:
        github, gitlab = sample_counts(start, end)
        data_mode = "preview"
    else:
        github_token = os.environ.get("GITHUB_TOKEN", "")
        gitlab_token = os.environ.get("GITLAB_TOKEN", "")
        if not github_token:
            raise SystemExit("GITHUB_TOKEN is required. GitHub Actions provides it automatically.")
        if not gitlab_token:
            raise SystemExit("GITLAB_TOKEN is required. Add it as a repository Actions secret.")
        github = fetch_github_activity(args.github_user, github_token, start, end)
        gitlab = fetch_gitlab_activity(args.gitlab_user, gitlab_token, start, end)
        data_mode = "live"

    rows = merge_activity(github, gitlab, start, end)
    stats = compute_stats(rows)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    public_payload = {
        "mode": data_mode,
        "range": {"from": start.isoformat(), "to": end.isoformat()},
        "stats": stats,
        "days": rows,
    }
    (output / "unified-activity.json").write_text(
        json.dumps(public_payload, indent=2) + "\n", encoding="utf-8"
    )
    (output / "engineering-activity.svg").write_text(render_heatmap(rows, stats), encoding="utf-8")
    (output / "engineering-snake.svg").write_text(render_snake(rows), encoding="utf-8")


if __name__ == "__main__":
    main()

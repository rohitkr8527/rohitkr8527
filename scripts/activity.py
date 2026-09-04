from __future__ import annotations

import json
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Any


def normalize_gitlab_events(events: list[dict[str, Any]]) -> dict[str, int]:
    """Reduce GitLab events to privacy-safe daily activity counts."""
    counts: dict[str, int] = defaultdict(int)
    for event in events:
        created_at = event.get("created_at")
        if not created_at:
            continue
        day = str(created_at)[:10]
        push_data = event.get("push_data") or {}
        commit_count = push_data.get("commit_count")
        if isinstance(commit_count, int) and commit_count > 0:
            counts[day] += commit_count
        else:
            counts[day] += 1
    return dict(sorted(counts.items()))


def merge_activity(
    github: dict[str, int],
    gitlab: dict[str, int],
    start: date,
    end: date,
) -> list[dict[str, int | str]]:
    """Merge GitHub and GitLab daily counts across an inclusive date range."""
    if end < start:
        raise ValueError("end must be on or after start")
    rows: list[dict[str, int | str]] = []
    current = start
    while current <= end:
        day = current.isoformat()
        gh = max(0, int(github.get(day, 0)))
        gl = max(0, int(gitlab.get(day, 0)))
        rows.append({"date": day, "github": gh, "gitlab": gl, "total": gh + gl})
        current += timedelta(days=1)
    return rows


def compute_stats(rows: list[dict[str, int | str]]) -> dict[str, int]:
    """Return aggregate contribution and streak statistics for merged rows."""
    total = sum(int(row["total"]) for row in rows)
    active_days = sum(1 for row in rows if int(row["total"]) > 0)
    longest = 0
    running = 0
    for row in rows:
        if int(row["total"]) > 0:
            running += 1
            longest = max(longest, running)
        else:
            running = 0
    current = 0
    for row in reversed(rows):
        if int(row["total"]) > 0:
            current += 1
        else:
            break
    return {
        "total": total,
        "active_days": active_days,
        "current_streak": current,
        "longest_streak": longest,
    }


def parse_github_graphql(payload: dict[str, Any]) -> dict[str, int]:
    """Extract contribution-calendar daily counts from GitHub GraphQL JSON."""
    if payload.get("errors"):
        raise RuntimeError(f"GitHub GraphQL error: {payload['errors']}")
    try:
        weeks = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    except (KeyError, TypeError) as exc:
        raise RuntimeError("GitHub GraphQL response did not contain a contribution calendar") from exc
    counts: dict[str, int] = {}
    for week in weeks:
        for item in week.get("contributionDays", []):
            counts[str(item["date"])] = int(item.get("contributionCount", 0))
    return counts


def _request_json(request: urllib.request.Request) -> Any:
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_github_activity(username: str, token: str, start: date, end: date) -> dict[str, int]:
    """Fetch GitHub contribution calendar data for a user using GraphQL."""
    if not token:
        raise ValueError("GitHub token is required")
    query = """
    query($login:String!, $from:DateTime!, $to:DateTime!) {
      user(login:$login) {
        contributionsCollection(from:$from, to:$to) {
          contributionCalendar {
            weeks { contributionDays { date contributionCount } }
          }
        }
      }
    }
    """
    body = json.dumps(
        {
            "query": query,
            "variables": {
                "login": username,
                "from": f"{start.isoformat()}T00:00:00Z",
                "to": f"{end.isoformat()}T23:59:59Z",
            },
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "rohitkr8527-profile-activity",
        },
    )
    return parse_github_graphql(_request_json(request))


def fetch_gitlab_activity(username: str, token: str, start: date, end: date) -> dict[str, int]:
    """Fetch GitLab user events and reduce them to daily activity counts.

    The function intentionally discards project metadata before returning.
    """
    if not token:
        raise ValueError("GITLAB_TOKEN is required")
    encoded_user = urllib.parse.quote(username, safe="")
    events: list[dict[str, Any]] = []
    page = 1
    while True:
        params = urllib.parse.urlencode(
            {
                "after": start.isoformat(),
                "before": end.isoformat(),
                "per_page": 100,
                "page": page,
            }
        )
        url = f"https://gitlab.com/api/v4/users/{encoded_user}/events?{params}"
        request = urllib.request.Request(
            url,
            headers={
                "PRIVATE-TOKEN": token,
                "User-Agent": "rohitkr8527-profile-activity",
            },
        )
        batch = _request_json(request)
        if not isinstance(batch, list):
            raise RuntimeError("GitLab Events API returned an unexpected response")
        events.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        if page > 100:
            raise RuntimeError("GitLab pagination exceeded safety limit")
    return normalize_gitlab_events(events)

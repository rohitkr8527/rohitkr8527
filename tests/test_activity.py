import json
import os
import sys
import unittest
from datetime import date
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from activity import (  # type: ignore
    compute_stats,
    fetch_gitlab_activity,
    merge_activity,
    normalize_gitlab_events,
    parse_github_contributions_html,
    parse_github_graphql,
)
from render import render_heatmap, render_snake  # type: ignore


class ActivityTests(unittest.TestCase):
    def test_gitlab_push_event_uses_commit_count_without_project_metadata(self):
        events = [
            {
                "action_name": "pushed to",
                "created_at": "2026-09-01T12:00:00.000+05:30",
                "project_id": 999,
                "push_data": {"commit_count": 4, "ref": "main"},
                "target_title": "private title",
            },
            {
                "action_name": "commented on",
                "created_at": "2026-09-01T14:00:00.000+05:30",
                "project_id": 999,
            },
        ]
        result = normalize_gitlab_events(events)
        self.assertEqual(result, {"2026-09-01": 5})
        self.assertNotIn("private", json.dumps(result))
        self.assertNotIn("999", json.dumps(result))

    def test_merge_activity_has_only_date_counts_and_total(self):
        rows = merge_activity(
            {"2026-09-01": 2, "2026-09-02": 1},
            {"2026-09-01": 3},
            date(2026, 9, 1),
            date(2026, 9, 3),
        )
        self.assertEqual(rows[0], {"date": "2026-09-01", "github": 2, "gitlab": 3, "total": 5})
        self.assertEqual(rows[2]["total"], 0)
        self.assertEqual(set(rows[0]), {"date", "github", "gitlab", "total"})

    def test_compute_stats_tracks_total_active_days_and_streaks(self):
        rows = [
            {"date": "2026-09-01", "github": 1, "gitlab": 0, "total": 1},
            {"date": "2026-09-02", "github": 0, "gitlab": 2, "total": 2},
            {"date": "2026-09-03", "github": 0, "gitlab": 0, "total": 0},
            {"date": "2026-09-04", "github": 1, "gitlab": 1, "total": 2},
        ]
        self.assertEqual(
            compute_stats(rows),
            {"total": 5, "active_days": 3, "current_streak": 1, "longest_streak": 2},
        )

    def test_parse_github_graphql_extracts_calendar_days(self):
        payload = {
            "data": {
                "user": {
                    "contributionsCollection": {
                        "contributionCalendar": {
                            "weeks": [
                                {
                                    "contributionDays": [
                                        {"date": "2026-09-01", "contributionCount": 3},
                                        {"date": "2026-09-02", "contributionCount": 0},
                                    ]
                                }
                            ]
                        }
                    }
                }
            }
        }
        self.assertEqual(parse_github_graphql(payload), {"2026-09-01": 3, "2026-09-02": 0})

    def test_parse_github_contributions_html_extracts_counts(self):
        html = """
        <table>
          <tr>
            <td id="contribution-day-component-0-0" data-date="2026-09-01" data-level="1"></td>
            <td id="contribution-day-component-0-1" data-date="2026-09-02" data-level="0"></td>
          </tr>
        </table>
        <tool-tip for="contribution-day-component-0-0">3 contributions on September 1st.</tool-tip>
        <tool-tip for="contribution-day-component-0-1">No contributions on September 2nd.</tool-tip>
        """
        counts = parse_github_contributions_html(html)
        self.assertEqual(counts.get("2026-09-01"), 3)
        self.assertEqual(counts.get("2026-09-02"), 0)

    def test_fetch_gitlab_activity_returns_empty_when_no_token(self):
        res = fetch_gitlab_activity("rohitkr8527", None, date(2026, 9, 1), date(2026, 9, 2))
        self.assertEqual(res, {})

    def test_heatmap_is_valid_svg_and_mentions_combined_activity(self):
        rows = merge_activity({"2026-09-01": 2}, {"2026-09-01": 4}, date(2026, 9, 1), date(2026, 9, 7))
        svg = render_heatmap(rows, compute_stats(rows))
        ET.fromstring(svg)
        self.assertIn("Engineering Activity", svg)
        self.assertIn("GitHub + GitLab", svg)

    def test_heatmap_mentions_github_only_when_no_gitlab(self):
        rows = merge_activity({"2026-09-01": 2}, {}, date(2026, 9, 1), date(2026, 9, 7))
        svg = render_heatmap(rows, compute_stats(rows))
        ET.fromstring(svg)
        self.assertIn("Engineering Activity", svg)
        self.assertIn("GitHub ·", svg)

    def test_snake_is_valid_animated_svg(self):
        rows = merge_activity({"2026-09-01": 2}, {"2026-09-02": 4}, date(2026, 9, 1), date(2026, 9, 14))
        svg = render_snake(rows)
        ET.fromstring(svg)
        self.assertIn("animateMotion", svg)
        self.assertIn("Combined engineering activity", svg)


if __name__ == "__main__":
    unittest.main()

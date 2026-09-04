from __future__ import annotations

from datetime import date, datetime, timedelta
from html import escape
from typing import Iterable

BG = "#0d1117"
CARD = "#161b22"
BORDER = "#30363d"
TEXT = "#f0f6fc"
MUTED = "#8b949e"
BLUE = "#58a6ff"
LEVELS = ["#21262d", "#0e4429", "#006d32", "#26a641", "#39d353"]


def _level(value: int, max_value: int) -> int:
    if value <= 0 or max_value <= 0:
        return 0
    ratio = value / max_value
    if ratio <= 0.25:
        return 1
    if ratio <= 0.5:
        return 2
    if ratio <= 0.75:
        return 3
    return 4


def _week_layout(rows: list[dict]) -> tuple[list[dict], date]:
    if not rows:
        return [], date.today()
    first = datetime.fromisoformat(str(rows[0]["date"])).date()
    aligned = first - timedelta(days=(first.weekday() + 1) % 7)  # Sunday start
    return rows, aligned


def render_heatmap(rows: list[dict], stats: dict[str, int]) -> str:
    rows, aligned = _week_layout(rows)
    cell = 11
    gap = 3
    left = 54
    top = 92
    width = 920
    height = 250
    max_value = max((int(r["total"]) for r in rows), default=0)
    row_by_date = {str(r["date"]): r for r in rows}

    rects: list[str] = []
    labels: list[str] = []
    month_seen: set[tuple[int, int]] = set()
    current = aligned
    last = datetime.fromisoformat(str(rows[-1]["date"])).date() if rows else aligned
    week = 0
    while current <= last:
        for dow in range(7):
            day = current + timedelta(days=dow)
            row = row_by_date.get(day.isoformat())
            value = int(row["total"]) if row else 0
            x = left + week * (cell + gap)
            y = top + dow * (cell + gap)
            fill = LEVELS[_level(value, max_value)]
            rects.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{fill}"><title>{day.isoformat()}: {value} activity</title></rect>'
            )
            key = (day.year, day.month)
            if day.day <= 7 and key not in month_seen:
                month_seen.add(key)
                labels.append(f'<text x="{x}" y="78" class="month">{day.strftime("%b")}</text>')
        current += timedelta(days=7)
        week += 1

    day_labels = [
        f'<text x="8" y="{top + idx * (cell + gap) + 9}" class="day">{name}</text>'
        for idx, name in [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    ]
    legend_x = width - 173
    legend = [f'<text x="{legend_x - 42}" y="224" class="muted">Less</text>']
    for i, color in enumerate(LEVELS):
        legend.append(f'<rect x="{legend_x + i * 16}" y="214" width="11" height="11" rx="2" fill="{color}"/>')
    legend.append(f'<text x="{legend_x + 88}" y="224" class="muted">More</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Combined GitHub and GitLab engineering activity">
<style>
.title{{font:700 21px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;fill:{TEXT}}}
.subtitle{{font:500 12px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;fill:{MUTED}}}
.stat{{font:700 17px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;fill:{TEXT}}}
.statlabel,.month,.day,.muted{{font:500 10px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;fill:{MUTED}}}
</style>
<rect width="100%" height="100%" rx="14" fill="{CARD}" stroke="{BORDER}"/>
<text x="24" y="34" class="title">Engineering Activity</text>
<text x="24" y="54" class="subtitle">GitHub + GitLab · combined daily activity</text>
<text x="620" y="34" class="stat">{stats.get('total',0):,}</text><text x="620" y="51" class="statlabel">activity</text>
<text x="705" y="34" class="stat">{stats.get('active_days',0):,}</text><text x="705" y="51" class="statlabel">active days</text>
<text x="805" y="34" class="stat">{stats.get('longest_streak',0):,}</text><text x="805" y="51" class="statlabel">best streak</text>
{''.join(labels)}{''.join(day_labels)}{''.join(rects)}{''.join(legend)}
</svg>'''


def render_snake(rows: list[dict]) -> str:
    rows, aligned = _week_layout(rows)
    width = 920
    height = 190
    cell = 10
    gap = 3
    left = 52
    top = 60
    row_by_date = {str(r["date"]): r for r in rows}
    max_value = max((int(r["total"]) for r in rows), default=0)
    last = datetime.fromisoformat(str(rows[-1]["date"])).date() if rows else aligned
    rects: list[str] = []
    points: list[tuple[float, float]] = []
    current = aligned
    week = 0
    while current <= last:
        dows = range(7) if week % 2 == 0 else range(6, -1, -1)
        for dow in dows:
            day = current + timedelta(days=dow)
            value = int(row_by_date.get(day.isoformat(), {}).get("total", 0))
            x = left + week * (cell + gap)
            y = top + dow * (cell + gap)
            rects.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{LEVELS[_level(value,max_value)]}" opacity="0.72"/>')
            points.append((x + cell / 2, y + cell / 2))
        current += timedelta(days=7)
        week += 1
    if not points:
        points = [(left, top), (left + 1, top)]
    path_d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Combined engineering activity snake animation">
<style>.title{{font:700 15px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;fill:{TEXT}}}.sub{{font:500 11px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;fill:{MUTED}}}</style>
<rect width="100%" height="100%" rx="14" fill="{CARD}" stroke="{BORDER}"/>
<text x="24" y="30" class="title">Activity Flow</text><text x="24" y="46" class="sub">Combined engineering activity · animated daily traversal</text>
{''.join(rects)}
<path d="{path_d}" fill="none" stroke="none" id="snakePath"/>
<g>
  <circle cx="0" cy="0" r="6" fill="{BLUE}" opacity="0.28"/>
  <circle cx="0" cy="0" r="3.2" fill="#79c0ff"/>
  <animateMotion dur="16s" repeatCount="indefinite" rotate="auto" path="{path_d}"/>
</g>
</svg>'''

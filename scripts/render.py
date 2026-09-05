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
    if max_value <= 4:
        return min(4, value)
    t1 = max(1, int(max_value * 0.20))
    t2 = max(2, int(max_value * 0.45))
    t3 = max(3, int(max_value * 0.70))
    if value <= t1:
        return 1
    if value <= t2:
        return 2
    if value <= t3:
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
    height = 252
    max_value = max((int(r["total"]) for r in rows), default=0)
    has_gitlab = any(int(r.get("gitlab", 0)) > 0 for r in rows)
    subtitle = "GitHub + GitLab · combined daily activity" if has_gitlab else "GitHub · daily activity and engineering momentum"
    row_by_date = {str(r["date"]): r for r in rows}

    rects: list[str] = []
    labels: list[str] = []
    month_seen: set[tuple[int, int]] = set()
    current = aligned
    last = datetime.fromisoformat(str(rows[-1]["date"])).date() if rows else aligned
    week = 0
    active_points: list[tuple[int, int, int]] = []
    while current <= last:
        for dow in range(7):
            day = current + timedelta(days=dow)
            row = row_by_date.get(day.isoformat())
            value = int(row["total"]) if row else 0
            x = left + week * (cell + gap)
            y = top + dow * (cell + gap)
            level = _level(value, max_value)
            fill = LEVELS[level]
            active_class = ' class="active-cell"' if value > 0 else ""
            rects.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{fill}"{active_class}><title>{day.isoformat()}: {value} activity</title></rect>'
            )
            if level >= 3:
                active_points.append((x + 5, y + 5, value))
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
    legend = [f'<text x="{legend_x - 42}" y="226" class="muted">Less</text>']
    for i, color in enumerate(LEVELS):
        legend.append(f'<rect x="{legend_x + i * 16}" y="216" width="11" height="11" rx="2" fill="{color}"/>')
    legend.append(f'<text x="{legend_x + 88}" y="226" class="muted">More</text>')

    # Subtle halos on the most active nodes
    halos: list[str] = []
    for hx, hy, val in active_points[-8:]:
        halos.append(
            f'<circle cx="{hx}" cy="{hy}" r="6" fill="#39d353" opacity="0.22" pointer-events="none">'
            f'<animate attributeName="r" values="4;7.5;4" dur="3.6s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.22;0.05;0.22" dur="3.6s" repeatCount="indefinite"/>'
            f'</circle>'
        )

    grid_width = week * (cell + gap)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Combined GitHub and GitLab engineering activity">
<defs>
  <linearGradient id="topAccent" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#58a6ff" stop-opacity="0.15"/>
    <stop offset="50%" stop-color="#39d353" stop-opacity="0.95"/>
    <stop offset="100%" stop-color="#a371f7" stop-opacity="0.25"/>
    <animate attributeName="x1" values="-100%;100%;-100%" dur="12s" repeatCount="indefinite"/>
    <animate attributeName="x2" values="0%;200%;0%" dur="12s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="energyWave" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#39d353" stop-opacity="0"/>
    <stop offset="42%" stop-color="#39d353" stop-opacity="0.02"/>
    <stop offset="50%" stop-color="#58a6ff" stop-opacity="0.22"/>
    <stop offset="58%" stop-color="#39d353" stop-opacity="0.08"/>
    <stop offset="100%" stop-color="#39d353" stop-opacity="0"/>
    <animate attributeName="x1" values="-150%;150%" dur="7s" repeatCount="indefinite"/>
    <animate attributeName="x2" values="-50%;250%" dur="7s" repeatCount="indefinite"/>
  </linearGradient>
</defs>
<style>
.title{{font:700 20px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;fill:{TEXT}}}
.subtitle{{font:500 12px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;fill:{MUTED}}}
.stat{{font:700 16px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif}}
.statlabel,.month,.day,.muted{{font:500 10px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;fill:{MUTED}}}
.active-cell{{transition:opacity 0.2s}}
.active-cell:hover{{stroke:#79c0ff;stroke-width:1px}}
</style>
<rect width="100%" height="100%" rx="14" fill="{CARD}" stroke="{BORDER}"/>
<rect x="14" y="0" width="892" height="2.5" rx="1" fill="url(#topAccent)"/>

<text x="24" y="34" class="title">Engineering Activity</text>
<g transform="translate(230, 27)">
  <circle cx="0" cy="0" r="3.5" fill="#39d353"/>
  <circle cx="0" cy="0" r="7.5" fill="none" stroke="#39d353" stroke-width="1.2" opacity="0.6">
    <animate attributeName="r" values="3.5;9;3.5" dur="2.4s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.75;0;0.75" dur="2.4s" repeatCount="indefinite"/>
  </circle>
</g>
<text x="24" y="55" class="subtitle">{subtitle}</text>

<!-- Stat Dashboard Pills -->
<g transform="translate(488, 14)">
  <rect width="94" height="46" rx="8" fill="#1b212a" stroke="{BORDER}"/>
  <text x="47" y="22" text-anchor="middle" class="stat" fill="#39d353">{stats.get('total',0):,}</text>
  <text x="47" y="37" text-anchor="middle" class="statlabel">activity</text>
</g>
<g transform="translate(592, 14)">
  <rect width="94" height="46" rx="8" fill="#1b212a" stroke="{BORDER}"/>
  <text x="47" y="22" text-anchor="middle" class="stat" fill="{TEXT}">{stats.get('active_days',0):,}</text>
  <text x="47" y="37" text-anchor="middle" class="statlabel">active days</text>
</g>
<g transform="translate(696, 14)">
  <rect width="98" height="46" rx="8" fill="#1b212a" stroke="{BORDER}"/>
  <text x="49" y="22" text-anchor="middle" class="stat" fill="{BLUE}">{stats.get('current_streak',0):,}</text>
  <text x="49" y="37" text-anchor="middle" class="statlabel">current streak</text>
</g>
<g transform="translate(804, 14)">
  <rect width="92" height="46" rx="8" fill="#1b212a" stroke="{BORDER}"/>
  <text x="46" y="22" text-anchor="middle" class="stat" fill="#d2a8ff">{stats.get('longest_streak',0):,}</text>
  <text x="46" y="37" text-anchor="middle" class="statlabel">best streak</text>
</g>

<!-- Heatmap Grid -->
{''.join(labels)}{''.join(day_labels)}{''.join(rects)}{''.join(halos)}

<!-- Shimmer Light Sweep -->
<rect x="52" y="90" width="{grid_width + 4}" height="100" rx="4" fill="url(#energyWave)" pointer-events="none"/>

{''.join(legend)}
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
    has_gitlab = any(int(r.get("gitlab", 0)) > 0 for r in rows)
    sub = "Combined engineering activity · animated daily traversal" if has_gitlab else "Engineering activity · animated daily traversal"
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
<text x="24" y="30" class="title">Activity Flow</text><text x="24" y="46" class="sub">{sub}</text>
{''.join(rects)}
<path d="{path_d}" fill="none" stroke="none" id="snakePath"/>
<g>
  <circle cx="0" cy="0" r="6" fill="{BLUE}" opacity="0.28"/>
  <circle cx="0" cy="0" r="3.2" fill="#79c0ff"/>
  <animateMotion dur="16s" repeatCount="indefinite" rotate="auto" path="{path_d}"/>
</g>
</svg>'''

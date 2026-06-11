#!/usr/bin/env python3
"""Génère un résumé GitHub Actions avec les technologies en hausse et en baisse."""

import json
import os
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "data.json"


def main() -> None:
    if not DATA_FILE.exists():
        return

    with DATA_FILE.open(encoding="utf-8") as f:
        data = json.load(f)

    technologies = data.get("technologies", [])
    rising = [t for t in technologies if t.get("trajectory") == "rising"]
    declining = [t for t in technologies if t.get("trajectory") == "declining"]

    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")

    if not summary_file:
        if rising:
            print(f"📈 En hausse ({len(rising)}) : {', '.join(t['name'] for t in rising)}")
        if declining:
            print(f"📉 En baisse ({len(declining)}) : {', '.join(t['name'] for t in declining)}")
        if not rising and not declining:
            print("→ Toutes les technologies sont stables.")
        return

    lines = [
        "# 📊 Résumé de la collecte\n",
        f"**Date :** {data.get('generated_at', '—')}  ",
        f"**Technologies suivies :** {len(technologies)}\n",
    ]

    if rising:
        lines.append(f"## 📈 En hausse — {len(rising)} technologie{'s' if len(rising) > 1 else ''}\n")
        lines.append("| Technologie | Catégorie | Position | ⭐ Stars |")
        lines.append("|------------|-----------|----------|---------|")
        for t in rising:
            stars = t.get("metrics", {}).get("github", {}).get("stars", "—")
            stars_fmt = f"{stars:,}".replace(",", " ") if isinstance(stars, int) else str(stars)
            lines.append(f"| **{t['name']}** | {t['category']} | `{t['position'].upper()}` | {stars_fmt} |")
        lines.append("")

    if declining:
        lines.append(f"## 📉 En baisse — {len(declining)} technologie{'s' if len(declining) > 1 else ''}\n")
        lines.append("| Technologie | Catégorie | Position |")
        lines.append("|------------|-----------|----------|")
        for t in declining:
            lines.append(f"| **{t['name']}** | {t['category']} | `{t['position'].upper()}` |")
        lines.append("")

    if not rising and not declining:
        lines.append("## → Toutes les technologies sont stables\n")

    with open(summary_file, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

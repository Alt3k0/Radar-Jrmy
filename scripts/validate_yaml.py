#!/usr/bin/env python3
"""Valide le schéma de technologies.yaml."""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
TECH_FILE = ROOT / "technologies.yaml"

VALID_POSITIONS = {"adopt", "trial", "assess", "hold"}
VALID_CATEGORIES = {
    "languages",
    "frameworks_front",
    "frameworks_back",
    "mobile",
    "databases",
    "devops",
    "observability",
    "security",
    "messaging",
    "ai",
}
VALID_SWITCHING_COSTS = {"low", "medium", "high"}
REQUIRED_FIELDS = {"id", "name", "category", "position"}


def validate() -> list[str]:
    with TECH_FILE.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    errors = []
    technologies = data.get("technologies", [])
    ids_seen = set()

    for i, tech in enumerate(technologies):
        prefix = f"[{i}] {tech.get('name', '???')}"

        for field in REQUIRED_FIELDS:
            if field not in tech:
                errors.append(f"{prefix}: champ requis manquant '{field}'")

        tech_id = tech.get("id")
        if tech_id:
            if tech_id in ids_seen:
                errors.append(f"{prefix}: id dupliqué '{tech_id}'")
            ids_seen.add(tech_id)

        if tech.get("position") and tech["position"] not in VALID_POSITIONS:
            errors.append(
                f"{prefix}: position invalide '{tech['position']}' (valeurs: {VALID_POSITIONS})"
            )

        if tech.get("category") and tech["category"] not in VALID_CATEGORIES:
            errors.append(
                f"{prefix}: catégorie invalide '{tech['category']}' (valeurs: {VALID_CATEGORIES})"
            )

        if tech.get("switching_cost") and tech["switching_cost"] not in VALID_SWITCHING_COSTS:
            errors.append(f"{prefix}: switching_cost invalide '{tech['switching_cost']}'")

    return errors


if __name__ == "__main__":
    errors = validate()
    if errors:
        print("Erreurs de validation YAML :")
        for error in errors:
            print(f"  ✗ {error}")
        sys.exit(1)
    print(f"technologies.yaml valide ({TECH_FILE})")

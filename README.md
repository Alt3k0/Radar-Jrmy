# ⬡ Tech Radar

![CI](https://github.com/Alt3k0/Radar-Jrmy/actions/workflows/ci.yml/badge.svg)
![Dernière collecte](https://github.com/Alt3k0/Radar-Jrmy/actions/workflows/collect.yml/badge.svg)

Radar technologique personnel — 50 technologies réparties sur 4 anneaux (Adopt / Trial / Assess / Hold) dans 10 catégories. Les métriques sont collectées automatiquement toutes les 6 h via GitHub Actions et publiées sur GitHub Pages.

**→ [Voir le radar en ligne](https://alt3k0.github.io/Radar-Jrmy/)**

---

## Fonctionnalités

| Page | Description |
|------|-------------|
| **Radar** | SVG interactif D3.js — survol pour tooltip, clic pour détail, filtres par catégorie |
| **Tableau** | Liste triable et filtrable avec pros/cons/cas d'usage en dépliable |
| **Éditeur** | Outil local pour changer la position d'une techno et exporter le YAML modifié |

Trajectoires calculées automatiquement (`↑` hausse / `→` stable / `↓` baisse) à partir de la variation des stars GitHub et des téléchargements npm/PyPI entre deux collectes.

---

## Architecture

```
technologies.yaml          ← source de vérité (édition manuelle)
        │
        ▼
scripts/collect.py         ← collecte async (httpx) toutes les 6 h
  ├── sources/github_source.py   GitHub API (stars, delta 30 j)
  ├── sources/npm_source.py      npm registry (DL/semaine, delta %)
  ├── sources/pypi_source.py     PyPI stats
  └── sources/cncf_source.py     CNCF membership
        │
        ▼
data/data.json             ← committé par radar-bot [skip ci]
        │
        ▼
src/ (GitHub Pages)        ← deploy.yml copie data.json dans src/
  ├── index.html           ← radar D3.js
  ├── table.html           ← tableau
  └── editor.html          ← éditeur YAML
```

Zéro serveur, zéro base de données — l'historique des métriques vit dans Git.

---

## Développement local

**Prérequis :** Python 3.12+, Node 20+

```bash
# 1. Dépendances Python
pip install -r requirements.txt        # production
pip install -r requirements-dev.txt    # + outils de dev (ruff, pytest)

# 2. Token GitHub (optionnel, évite la limite de taux API)
echo "GITHUB_TOKEN=ghp_xxxx" > .env

# 3. Collecter les métriques
python scripts/collect.py              # génère data/data.json

# 4. Lancer le site
npm run dev                            # copie data.json dans src/
python -m http.server 8080 --directory src
# → http://localhost:8080
```

---

## Ajouter ou modifier une technologie

Éditer [`technologies.yaml`](technologies.yaml) :

```yaml
- id: mon-outil
  name: Mon Outil
  category: devops          # languages | frameworks_front | frameworks_back
                            # mobile | databases | devops | observability
                            # security | messaging | ai
  position: trial           # adopt | trial | assess | hold
  since: "2025-01"
  switching_cost: medium    # low | medium | high
  notes: "Courte description."
  pros:
    - Avantage 1
  cons:
    - Inconvénient 1
  use_cases:
    - Cas d'usage 1
  sources:
    github: owner/repo      # optionnel
    npm_package: nom-pkg    # optionnel
    pypi_package: nom-pkg   # optionnel
```

Valider le schéma :

```bash
python scripts/validate_yaml.py
```

---

## CI/CD

| Workflow | Déclencheur | Action |
|----------|-------------|--------|
| `ci.yml` | Push / PR | ruff, pytest, htmlhint, eslint, validate_yaml |
| `collect.yml` | Cron 6 h + manuel | Collecte les métriques, commit `data/data.json` |
| `deploy.yml` | Push main + fin de collect | Déploie `src/` sur GitHub Pages |

**Secret requis :** `RADAR_GITHUB_TOKEN` — PAT GitHub avec scope `public_repo` (pour appeler l'API GitHub sans rate-limit dans `collect.py`).

---

## Stack technique

| Couche | Technologie |
|--------|-------------|
| Visualisation | D3.js v7, JS ES modules vanilla |
| Build frontend | Aucun — HTML/CSS/JS statique |
| Collecte | Python 3.12, httpx (async), PyYAML |
| Linting Python | ruff |
| Tests Python | pytest, pytest-asyncio, pytest-httpx |
| Linting JS/HTML | ESLint 8, HTMLHint |
| Hébergement | GitHub Pages (`src/`) |

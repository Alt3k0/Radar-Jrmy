# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Format : [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)
Versionnement : [Semantic Versioning](https://semver.org/lang/fr/)

---

## [Unreleased]

## [0.1.0] — 2026-06-11

### Added
- Structure initiale du projet (Python 3.12, D3.js v7, GitHub Actions)
- 20 technologies pré-configurées dans `technologies.yaml`
- Scripts de collecte : GitHub REST API, npm downloads, PyPI stats, CNCF Landscape
- Client HTTP réutilisable avec retry/backoff exponentiel (3 tentatives)
- Calcul automatique de trajectoire (`rising` / `stable` / `declining`)
- Vue radar D3.js interactive (4 anneaux ADOPT/TRIAL/ASSESS/HOLD)
- Vue tableau filtrable et triable avec accessibilité clavier
- Éditeur de positions avec export YAML
- Workflow CI : lint ruff + tests pytest + validation YAML + htmlhint + eslint
- Workflow collect : cron toutes les 6h, commit automatique `data.json`
- Workflow deploy : déploiement GitHub Pages après collecte ou push sur main
- Templates GitHub : PR, issues "add technology" et "bug report"
- Gestion sécurisée des secrets via GitHub Actions Secrets + `.env` local

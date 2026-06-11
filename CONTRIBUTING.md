# Contribuer au Tech Radar

## Ajouter une technologie

1. Éditer `technologies.yaml` — ajouter une entrée en suivant ce modèle :

```yaml
- id: nom-kebab-case          # identifiant unique, minuscules, tirets
  name: Nom Affiché
  category: devops            # voir catégories valides ci-dessous
  position: assess            # adopt | trial | assess | hold
  since: "2026-01"            # YYYY-MM
  switching_cost: medium      # low | medium | high
  notes: "Justification en une phrase"
  sources:
    github: owner/repo        # optionnel
    npm_package: package-name # optionnel
    pypi_package: package     # optionnel
    cncf: true                # optionnel
```

**Catégories valides :** `languages`, `frameworks_front`, `frameworks_back`,
`mobile`, `databases`, `devops`, `observability`, `security`, `messaging`, `ai`

2. Valider le schéma :
```bash
python scripts/validate_yaml.py
```

3. Ouvrir une Pull Request avec le template "Ajouter une technologie".

---

## Développement local

```bash
# Installer les dépendances Python
pip install -r requirements-dev.txt

# Copier et remplir les variables d'environnement
cp .env.example .env
# Ajouter votre GITHUB_TOKEN dans .env (optionnel, limite à 60 req/h sans)

# Lancer la collecte
python scripts/collect.py

# Ouvrir le site (serveur local requis pour les modules ES)
python -m http.server 8080 --directory src
# Puis ouvrir http://localhost:8080
```

## Tests et linting

```bash
# Lint Python
ruff check scripts/ tests/
ruff format --check scripts/ tests/

# Tests
pytest tests/ -v

# Validation YAML
python scripts/validate_yaml.py
```

## Conventional Commits

| Prefix | Usage |
|--------|-------|
| `feat:` | Nouvelle technologie ou fonctionnalité |
| `fix:` | Correction de bug |
| `chore:` | Maintenance (deps, config, données auto) |
| `docs:` | Documentation uniquement |
| `test:` | Ajout/modification de tests |
| `ci:` | Modification des workflows CI/CD |

## Définitions des positions

| Position | Signification |
|----------|---------------|
| **ADOPT** | Confiance totale. Utiliser en production sans hésitation. |
| **TRIAL** | Mérite d'être expérimenté sur des projets réels. |
| **ASSESS** | À explorer pour comprendre l'impact potentiel. |
| **HOLD** | Approcher avec précaution. Éviter pour les nouveaux projets. |

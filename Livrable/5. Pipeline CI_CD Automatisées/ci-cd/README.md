# Pipeline CI/CD — FutureKawa

---

|              |                                     |
|---|---|
| **Projet**   | FutureKawa |
| **Document** | Documentation du pipeline CI/CD      |
| **Version**  | 1.0                                   |
| **Date**     | 02/07/2026                            |
| **Équipe**   | Rudy · Florian · Noé · Josselin       |

---

## Vue d'ensemble

Le pipeline CI/CD est défini dans `.gitlab-ci.yml` à la racine du dépôt. Il utilise **GitLab CI** avec des runners Docker.

### Stages

```
lint  →  test  →  build  →  staging  →  security  →  deploy
```

| Stage | Rôle | Déclenchement |
|---|---|---|
| `lint` | Vérification syntaxique et style | MR + push sur toute branche |
| `test` | Tests unitaires et intégration | MR + push sur toute branche |
| `build` | Build et push des images Docker | `dev` et `main` uniquement |
| `staging` | Smoke test avec les images buildées | `dev` et `main` uniquement |
| `security` | SAST + détection de secrets | Toutes branches |
| `deploy` | Validation Terraform + gate manuel | `main` uniquement |

---

## Navigation

| # | Document | Contenu |
|---|---|---|
| 1 | [Lint](01-lint.md) | Vérifications ESLint, Ruff, ShellCheck |
| 2 | [Tests](02-tests.md) | Jobs de test par service, couverture, artifacts |
| 3 | [Build](03-build.md) | Construction des images Docker, registry, tags |
| 4 | [Staging](04-staging.md) | Smoke test de la stack CI |
| 5 | [Sécurité](05-securite.md) | SAST GitLab, détection de secrets |
| 6 | [Deploy](06-deploy.md) | Gate manuel, Terraform validate |

---

## Règles de déclenchement

Les jobs CI sont **conditionnels** : ils ne tournent que si des fichiers du service concerné ont changé. Cela évite de lancer les tests de l'API siège quand seul le frontend exploitation a été modifié.

```yaml
rules:
  - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    changes:
      - API-siege/**/*
  - if: '$CI_PIPELINE_SOURCE == "push"'
    changes:
      - API-siege/**/*
```

---

## Résumé des jobs

| Job | Stage | Service | Image |
|---|---|---|---|
| `lint_simu_sensor` | lint | simu-sensor | node:20 |
| `lint_front_siege` | lint | front-siege | node:20 |
| `lint_front_exploitation` | lint | front-exploitation | node:20 |
| `lint_api_siege` | lint | API Siège | python:3.12-slim |
| `lint_api_exploitation` | lint | API Exploitation | python:3.12-slim |
| `lint_broker` | lint | broker | shellcheck-alpine |
| `simu_sensor_test` | test | simu-sensor | node:20 |
| `api_siege_test` | test | API Siège | python:3.11-alpine |
| `api_exploitation_test` | test | API Exploitation | python:3.11-alpine |
| `front_siege_test` | test | front-siege | node:20 |
| `front_exploitation_test` | test | front-exploitation | node:20 |
| `broker_acl_test` | test | broker | docker:24 |
| `build_api_siege` | build | API Siège | docker:24 |
| `build_api_exploitation` | build | API Exploitation | docker:24 |
| `build_front_siege` | build | front-siege | docker:24 |
| `build_front_exploitation` | build | front-exploitation | docker:24 |
| `build_broker` | build | broker | docker:24 |
| `smoke_test` | staging | toute la stack | docker:24 |
| `semgrep-sast` | security | tout le code | GitLab template |
| `secret_detection` | security | tout le code | GitLab template |
| `deploy_prod` | deploy | infra/ | hashicorp/terraform:1.9 |

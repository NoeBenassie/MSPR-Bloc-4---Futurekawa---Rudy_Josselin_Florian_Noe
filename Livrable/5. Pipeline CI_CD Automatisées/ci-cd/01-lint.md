# 01 — Stage Lint

[← Retour à l'index](README.md) | [Suivant : Tests →](02-tests.md)

---

## Rôle

Le stage `lint` vérifie la **qualité syntaxique et stylistique** du code avant de lancer les tests. Un job échoué ici bloque la suite du pipeline.

---

## Jobs

### `lint_simu_sensor` — ESLint (Node 20)

Vérifie le code TypeScript/Vue du simulateur de capteur.

```yaml
image: node:20
script:
  - cd simu-sensor
  - npm ci
  - npx eslint .
```

**Déclenché si :** fichiers `simu-sensor/**/*` modifiés.

---

### `lint_front_siege` — ESLint (Node 20)

Vérifie le code TypeScript/Vue du frontend siège.

```yaml
image: node:20
script:
  - cd front-siege
  - npm ci
  - npx eslint .
```

**Déclenché si :** fichiers `front-siege/**/*` modifiés.

---

### `lint_front_exploitation` — ESLint (Node 20)

Vérifie le code TypeScript/Vue du frontend exploitation.

```yaml
image: node:20
script:
  - cd front-exploitation
  - npm ci
  - npx eslint .
```

**Déclenché si :** fichiers `front-exploitation/**/*` modifiés.

---

### `lint_api_siege` — Ruff (Python 3.12)

Vérifie le code Python de l'API siège avec Ruff (linter + formateur Python ultra-rapide).

```yaml
image: python:3.12-slim
script:
  - pip install -q ruff
  - cd API-siege
  - ruff check .
```

**Déclenché si :** fichiers `API-siege/**/*` modifiés.

---

### `lint_api_exploitation` — Ruff (Python 3.12)

Même chose pour l'API exploitation.

```yaml
image: python:3.12-slim
script:
  - pip install -q ruff
  - cd API-exploitation
  - ruff check .
```

**Déclenché si :** fichiers `API-exploitation/**/*` modifiés.

---

### `lint_broker` — ShellCheck

Vérifie les scripts shell du broker MQTT (`entrypoint.sh`, `tests/test_acl.sh`) avec ShellCheck, le linter shell de référence.

```yaml
image: koalaman/shellcheck-alpine:stable
script:
  - shellcheck broker/entrypoint.sh broker/tests/test_acl.sh
```

**Déclenché si :** fichiers `broker/**/*` modifiés.

---

## En cas d'échec

| Outil | Commande locale équivalente |
|---|---|
| ESLint | `cd <service> && npx eslint .` |
| Ruff | `cd API-<service> && ruff check . --fix` |
| ShellCheck | `shellcheck broker/entrypoint.sh` |

---

[← Retour à l'index](README.md) | [Suivant : Tests →](02-tests.md)

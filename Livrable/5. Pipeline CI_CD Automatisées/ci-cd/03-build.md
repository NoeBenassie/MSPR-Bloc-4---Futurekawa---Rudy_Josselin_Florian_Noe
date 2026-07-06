# 03 — Stage Build

[← Tests](02-tests.md) | [Suivant : Staging →](04-staging.md)

---

## Rôle

Le stage `build` construit les images Docker de chaque service et les pousse dans le **registry GitLab**. Il ne se déclenche que sur les branches `dev` et `main`.

---

## Template commun

Tous les jobs de build partagent un template YAML (`&build_template`) :

```yaml
stage: build
image: docker:24
services:
  - docker:24-dind
before_script:
  - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" "$CI_REGISTRY"
  - |
    if [ "$CI_COMMIT_BRANCH" = "main" ]; then
      export TAG_MOVING="latest"
      export TAG_SHA="main-$CI_COMMIT_SHORT_SHA"
    else
      export TAG_MOVING="dev-latest"
      export TAG_SHA="dev-$CI_COMMIT_SHORT_SHA"
    fi
rules:
  - if: '$CI_COMMIT_BRANCH == "dev"'
  - if: '$CI_COMMIT_BRANCH == "main"'
```

---

## Jobs

### `build_api_siege`

```bash
docker build -t "$REGISTRY/futurekawa-api-siege:$TAG_SHA" API-siege/
docker tag ... :$TAG_MOVING
docker push ... :$TAG_SHA
docker push ... :$TAG_MOVING
```

### `build_api_exploitation`

Idem pour `API-exploitation/`.

### `build_front_siege`

Idem pour `front-siege/`.

### `build_front_exploitation`

Idem pour `front-exploitation/`.

### `build_broker`

Idem pour `broker/`.

---

## Stratégie de tags

| Branche | Tag mobile | Tag SHA (immuable) |
|---|---|---|
| `dev` | `dev-latest` | `dev-<sha court>` |
| `main` | `latest` | `main-<sha court>` |

Le tag SHA est utilisé par le job `smoke_test` pour tester exactement les images qui viennent d'être buildées.

---

## Images buildées

| Image | Registry |
|---|---|
| `futurekawa-api-siege` | `registry.gitlab.com/<groupe>/futurekawa/` |
| `futurekawa-api-exploitation` | idem |
| `futurekawa-front-siege` | idem |
| `futurekawa-front-exploitation` | idem |
| `futurekawa-broker` | idem |

---

[← Tests](02-tests.md) | [Suivant : Staging →](04-staging.md)

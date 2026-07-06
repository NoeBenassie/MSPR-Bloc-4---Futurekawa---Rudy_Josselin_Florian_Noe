# 04 — Stage Staging (Smoke Test)

[← Build](03-build.md) | [Suivant : Sécurité →](05-securite.md)

---

## Rôle

Le stage `staging` lève la stack backend complète à partir des images **tout juste buildées** et vérifie que les deux APIs répondent sur `/api/health/`. Si ce test échoue, le pipeline s'arrête avant le deploy.

---

## Job : `smoke_test`

### Principe

Le smoke test utilise `docker-compose.ci.yml`, une version allégée de la stack (pas de frontends, pas de simu-sensor). Les images viennent du registry GitLab, pas d'un bind-mount du code source.

```yaml
stage: staging
image: docker:24
services:
  - docker:24-dind
```

### Script

```bash
# 1. Récupère les images buildées à ce SHA
docker compose -f docker-compose.ci.yml pull

# 2. Lève la stack
docker compose -f docker-compose.ci.yml up -d

# 3. Attend que l'API siège réponde (30 tentatives × 2 s)
until docker compose exec -T api-siege wget -q --spider -T 3 http://127.0.0.1:5000/api/health/
do sleep 2; done

# 4. Assert API siège
docker compose exec -T api-siege wget -q --spider http://127.0.0.1:5000/api/health/

# 5. Même séquence pour api-exploitation
# ...

# 6. État final
docker compose -f docker-compose.ci.yml ps
```

### Nettoyage (after_script)

```bash
docker compose -f docker-compose.ci.yml logs --tail=100
docker compose -f docker-compose.ci.yml down -v
```

---

## Pourquoi `127.0.0.1` et pas `localhost` ?

Dans ces containers CI, `localhost` résout en IPv6 (`::1`) en premier, mais les serveurs Django n'écoutent qu'en IPv4. Utiliser `127.0.0.1` force l'IPv4 et évite un faux négatif de healthcheck.

---

## Déclenchement

Uniquement sur les branches `dev` et `main`, après le stage `build`.

---

[← Build](03-build.md) | [Suivant : Sécurité →](05-securite.md)

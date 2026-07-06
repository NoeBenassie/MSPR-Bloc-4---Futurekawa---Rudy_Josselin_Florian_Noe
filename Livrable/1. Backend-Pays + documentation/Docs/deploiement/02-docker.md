# 02 — Docker et images

[← Architecture](01-architecture.md) | [Suivant : Terraform →](03-terraform.md)

---

## Dockerfiles

Chaque service buildable dispose de son propre `Dockerfile` à la racine de son dossier :

| Service | Dockerfile |
|---|---|
| API Siège | `API-siege/Dockerfile` |
| API Exploitation | `API-exploitation/Dockerfile` |
| Front Siège | `front-siege/Dockerfile` |
| Front Exploitation | `front-exploitation/Dockerfile` |
| Broker MQTT | `broker/Dockerfile` |

Le simulateur (`simu-sensor`) utilise aussi un Dockerfile mais ne tourne qu'en développement (profil `demo` du Compose).

---

## Registry GitLab

Les images buildées en CI sont poussées dans le **registry GitLab du projet** :

```
registry.gitlab.com/<groupe>/futurekawa/futurekawa-<service>:<tag>
```

| Image | Exemple de tag |
|---|---|
| `futurekawa-api-siege` | `dev-a1b2c3d` / `latest` |
| `futurekawa-api-exploitation` | `dev-a1b2c3d` / `latest` |
| `futurekawa-front-siege` | `dev-a1b2c3d` / `latest` |
| `futurekawa-front-exploitation` | `dev-a1b2c3d` / `latest` |
| `futurekawa-broker` | `dev-a1b2c3d` / `latest` |

---

## Stratégie de tags

| Branche | Tag mobile | Tag SHA |
|---|---|---|
| `dev` | `dev-latest` | `dev-<sha court>` |
| `main` | `latest` | `main-<sha court>` |

Le tag SHA est immuable et permet de retrouver exactement quelle version est déployée. Le tag mobile (`latest`, `dev-latest`) est écrasé à chaque build.

---

## Build local

```bash
# Rebuild toutes les images sans cache
make rebuild

# Build + démarrage avec rebuild
make dev

# Build d'un service spécifique
docker compose -f docker-compose.siege.yml build api-siege
```

---

## Commandes Docker utiles

```bash
# Voir les images construites
docker images | grep futurekawa

# Logs d'un service
docker compose -f docker-compose.siege.yml logs -f api-siege

# Shell dans un container
docker compose -f docker-compose.exploit.yml exec api-exploitation bash

# Lancer une migration Django manuellement
docker compose -f docker-compose.exploit.yml exec api-exploitation python manage.py migrate
```

---

[← Architecture](01-architecture.md) | [Suivant : Terraform →](03-terraform.md)

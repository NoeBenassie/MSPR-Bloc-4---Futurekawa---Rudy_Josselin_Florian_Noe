# 04 — Variables d'environnement

[← Terraform](03-terraform.md) | [← Retour à l'index](README.md)

---

## Présentation

Les variables d'environnement sont centralisées dans un fichier `.env` à la racine du projet (non versionné). Le `Makefile` l'inclut automatiquement avec `include .env`.

```bash
cp .env.example .env
# Éditer .env avec les valeurs réelles
```

---

## Variables globales (toutes stacks)

| Variable | Description | Exemple |
|---|---|---|
| `COMPOSE_PROJECT_NAME` | Préfixe des containers Docker | `futurekawa` |

---

## Application Siège — API Django

| Variable | Description | Requis |
|---|---|---|
| `SECRET_KEY` | Clé secrète Django (siège) | Oui |
| `DEBUG` | Mode debug (`True` / `False`) | Oui |
| `ALLOWED_HOSTS` | Hôtes autorisés | Oui |
| `DB_NAME` | Nom de la base PostgreSQL siège | Oui |
| `DB_USER` | Utilisateur PostgreSQL | Oui |
| `DB_PASSWORD` | Mot de passe PostgreSQL | Oui |
| `DB_HOST` | Hôte PostgreSQL (nom du container) | Oui |
| `DB_PORT` | Port PostgreSQL | `5432` |
| `EMAIL_HOST` | Serveur SMTP pour les invitations | Oui |
| `EMAIL_PORT` | Port SMTP | `587` |
| `EMAIL_HOST_USER` | Adresse e-mail expéditeur | Oui |
| `EMAIL_HOST_PASSWORD` | Mot de passe SMTP | Oui |
| `FRONTEND_URL` | URL du frontend siège (liens e-mail) | Oui |

---

## Application Exploitation — API Django

| Variable | Description | Requis |
|---|---|---|
| `SECRET_KEY_EXPLOITATION` | Clé secrète Django (exploitation) | Oui |
| `DEBUG_EXPLOITATION` | Mode debug | Oui |
| `ALLOWED_HOSTS_EXPLOITATION` | Hôtes autorisés | Oui |
| `DB_NAME_EXPLOITATION` | Nom de la base PostgreSQL exploitation | Oui |
| `DB_USER_EXPLOITATION` | Utilisateur PostgreSQL | Oui |
| `DB_PASSWORD_EXPLOITATION` | Mot de passe PostgreSQL | Oui |
| `DB_HOST_EXPLOITATION` | Hôte PostgreSQL | Oui |
| `DB_PORT_EXPLOITATION` | Port PostgreSQL | `5432` |
| `REDIS_URL` | URL Redis (Celery broker) | `redis://redis:6379/0` |
| `EMAIL_HOST` | SMTP (invitations exploitation) | Oui |
| `FRONTEND_URL_EXPLOITATION` | URL du frontend exploitation | Oui |

---

## Broker MQTT

| Variable | Description | Requis |
|---|---|---|
| `MQTT_USER` | Nom d'utilisateur MQTT | Oui |
| `MQTT_PASSWORD` | Mot de passe MQTT | Oui |

---

## Simu-sensor (dev uniquement)

| Variable | Description | Défaut |
|---|---|---|
| `VITE_MQTT_BROKER_URL` | URL WebSocket du broker MQTT | `ws://localhost:9001` |
| `VITE_MQTT_USER` | Utilisateur MQTT | `admin` |
| `VITE_MQTT_PASSWORD` | Mot de passe MQTT | — |
| `VUE_APP_API_PAYS_URL` | URL de l'API exploitation | — |

---

## Synchronisation siège → exploitation

| Variable | Description | Requis |
|---|---|---|
| `EXPLOITATION_API_URL` | URL de base de l'API exploitation | Oui |
| `EXPLOITATION_API_TOKEN` | Master token pour `/api/all-data/` | Oui |

Le master token est généré via la commande Django :
```bash
docker compose exec api-exploitation python manage.py create_master_token <nom>
```

---

[← Terraform](03-terraform.md) | [← Retour à l'index](README.md)

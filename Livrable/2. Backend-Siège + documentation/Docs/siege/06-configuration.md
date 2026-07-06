# 06 — Configuration & déploiement

[← Précédent : Sécurité & chiffrement](05-securite-chiffrement.md) | [Retour à l'index](README.md) | [Suivant : Tests →](07-tests.md)

---

## Les conteneurs du service

Le backend siège est bien plus simple à déployer que l'exploitation : **pas de Redis, pas de worker, pas de broker** (`docker-compose.siege.yml`).

| Conteneur | Image | Rôle |
|---|---|---|
| `bdd-siege` | `postgres:16-alpine` | Base de données centrale |
| `api-siege` | Django | Migrations + serveur API |
| `front-siege` | `node:20-alpine` | Interface Vue.js |

```
        ┌──────── network-siege ────────┐
        │                                │
   bdd-siege ──── api-siege ──── front-siege
   (PostgreSQL)   (Django)       (Vue.js)
        └────────────────────────────────┘
                     │
                     ▼  requests (réseaux exploitation)
            [ Exploitations distantes ]
```

> Le siège est raccordé aux réseaux des exploitations (`network-exploitation`, `network-exploit-1`) pour pouvoir les appeler.

---

## L'entrypoint

```sh
# API-siege/entrypoint.sh
1. makemigrations + migrate         # met la base à jour
2. create_default_users             # crée les comptes par défaut
3. runserver 0.0.0.0:5000           # serveur Django
```

Un seul processus, au premier plan — contrairement à l'exploitation qui jongle avec le subscriber MQTT.

---

## Variables d'environnement clés

| Variable | Rôle |
|---|---|
| `DJANGO_SETTINGS_MODULE` | `core.settings.local` / `production` |
| `DJANGO_SECRET_KEY` | Clé secrète Django |
| `SITE_TOKEN_ENCRYPTION_KEY` | **Clé Fernet** pour chiffrer les tokens des sites |
| `POSTGRES_*` | Connexion base centrale |
| `CORS_ALLOWED_ORIGINS` | Origines front autorisées (prod) |
| `EMAIL_HOST_*` | SMTP pour les emails d'invitation |
| `FRONTEND_URL` | Base des liens d'invitation (`/set-password?token=...`) |

> `SITE_TOKEN_ENCRYPTION_KEY` est **critique** : la perdre rend tous les tokens de sites illisibles. À générer avec `Fernet.generate_key()` et à conserver en secret.

---

## Environnements de settings

```
core/settings/
├── base.py         # commun — INSTALLED_APPS, DRF, chiffrement
├── local.py        # dev — DEBUG=True, CORS ouvert
├── production.py   # prod — DEBUG=False, CORS_ALLOWED_ORIGINS explicite
└── test.py         # CI — base isolée
```

---

## Démarrage local

```bash
docker compose -f docker-compose.siege.yml up

# ou à la main
cd API-siege
python manage.py migrate
python manage.py create_default_users
python manage.py runserver 0.0.0.0:5000
```

---

[← Précédent : Sécurité & chiffrement](05-securite-chiffrement.md) | [Retour à l'index](README.md) | [Suivant : Tests →](07-tests.md)

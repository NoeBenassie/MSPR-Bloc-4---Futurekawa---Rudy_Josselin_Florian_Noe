# 01 — Vue d'ensemble

[← Retour à l'index](README.md) | [Suivant : Django & DRF →](02-django-drf.md)

---

## Rôle du backend siège

Le backend siège est la **tour de contrôle multi-plantations**. Il ne collecte pas lui-même de mesures : il **interroge** chaque exploitation, en cache les données, et offre une vue consolidée au frontend siège.

Ses missions :

1. **Référencer** les sites d'exploitation (nom, pays, URL d'API, token d'accès chiffré).
2. **Synchroniser** : appeler l'endpoint `/api/all-data/` de chaque exploitation.
3. **Cacher** la dernière réponse de chaque site (`last_data`, `last_sync`).
4. **Gérer** les utilisateurs du siège (admin / lecteur) et leur authentification.

---

## Architecture réseau

```
                    ┌──────────────── Frontend Siège (Vue.js) ────────────────┐
                    │        consulte les sites, les cartes, les graphiques    │
                    └───────────────────────────┬──────────────────────────────┘
                                                 │ REST
                                                 ▼
                                        [ API Siège (Django) ]
                                        ├── SiegeUser (comptes)
                                        ├── ExploitationSite (sites + token chiffré)
                                        └── action « sync »
                                                 │
                    ┌────────────────────────────┼────────────────────────────┐
                    │ GET /api/all-data/          │ GET /api/all-data/          │ ...
                    ▼ (Token chiffré)             ▼                             ▼
          [ Exploitation A ]            [ Exploitation B ]            [ Exploitation C ]
```

> Le siège est **client** des exploitations. Il n'accède jamais à leurs bases de données : il passe par leur API, authentifié avec un token propre à chaque site.

---

## Stack technique

| Élément | Choix | Rôle |
|---|---|---|
| Framework web | Django 4.2 | Structure, ORM, admin |
| API | Django REST Framework | Sérialisation, ViewSets |
| Base de données | PostgreSQL 15 | Sites + utilisateurs |
| Client HTTP | `requests` | Appels vers les exploitations |
| Chiffrement | `cryptography` (Fernet) | Tokens API des sites |
| Filtres | `django-filter` | Filtrage des listes API |
| Doc API | drf-spectacular | Swagger / OpenAPI |

---

## Dépendances (`requirements.txt`)

```
Django>=4.2,<5.0
djangorestframework>=3.14
psycopg2-binary>=2.9
django-cors-headers>=4.0
python-dotenv>=1.0.0
django-filter>=23.5        # filtrage des listes
drf-spectacular>=0.26.0    # documentation OpenAPI
requests>=2.31.0           # appels HTTP vers les exploitations
cryptography>=42.0         # chiffrement Fernet des tokens
```

> Différence marquante avec l'exploitation : **pas de Celery, pas de Redis, pas de paho-mqtt**. En revanche, `requests` et `cryptography` sont propres au siège.

---

## Les trois modèles

| Modèle | Rôle |
|---|---|
| `SiegeUser` | Utilisateur du siège (`AbstractUser`), rôle `admin` ou `viewer` |
| `ExploitationSite` | Un site distant : URL d'API + token chiffré + cache des données |
| `InvitationToken` | Token UUID à usage unique pour définir un mot de passe (24 h) |

---

[← Retour à l'index](README.md) | [Suivant : Django & DRF →](02-django-drf.md)

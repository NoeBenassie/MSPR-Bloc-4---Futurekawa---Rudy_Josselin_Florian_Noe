# Backend Siège — FutureKawa

---

|              |                                          |
|---|---|
| **Projet**   | FutureKawa |
| **Livrable** | Documentation Backend Siège |
| **Périmètre** | API Django centrale qui agrège les plantations |
| **Framework** | Django 4.2 + Django REST Framework |
| **Communication** | Client HTTP (`requests`) vers les exploitations |
| **Sécurité** | Tokens API chiffrés (Fernet / cryptography) |
| **Équipe**   | Rudy · Florian · Noé · Josselin |

---

## Sommaire

| Section | Fichier |
|---|---|
| Vue d'ensemble | [01-vue-ensemble.md](01-vue-ensemble.md) |
| Django & Django REST Framework | [02-django-drf.md](02-django-drf.md) |
| Endpoints de l'API | [03-endpoints-api.md](03-endpoints-api.md) |
| Agrégation des exploitations | [04-agregation-sites.md](04-agregation-sites.md) |
| Sécurité & chiffrement | [05-securite-chiffrement.md](05-securite-chiffrement.md) |
| Configuration & déploiement | [06-configuration.md](06-configuration.md) |
| Tests | [07-tests.md](07-tests.md) |

---

## En quoi le siège diffère de l'exploitation

| | Siège | Exploitation |
|---|---|---|
| Base de données | Centrale (sites + utilisateurs) | Locale (données terrain) |
| Temps réel MQTT | Non | Oui |
| Celery / Redis | Non | Oui |
| Rôle réseau | **Client** : consomme les exploitations | **Serveur** : expose `/api/all-data/` |
| Chiffrement | Tokens API des sites (Fernet) | — |

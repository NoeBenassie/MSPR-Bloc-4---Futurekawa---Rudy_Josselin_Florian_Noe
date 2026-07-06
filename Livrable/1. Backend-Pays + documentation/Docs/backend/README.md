# Services Backend — FutureKawa

Deux services backend distincts, un par application. Ils ne partagent ni le même code, ni la même base de données, ni les mêmes dépendances.

| Application | Dossier | Stack particulière |
|---|---|---|
| Exploitation | [exploitation/](exploitation/README.md) | Django + DRF + **Celery/Redis** + **MQTT** |
| Siège | [siege/](../../../Backend-Siège%20+%20documentation/Docs/siege/README.md) | Django + DRF + **cryptography** + **requests** |

---

## En un coup d'œil

| | Exploitation | Siège |
|---|---|---|
| **Rôle** | Instance locale d'une plantation | Agrégateur central multi-sites |
| **Base de données** | PostgreSQL locale | PostgreSQL centrale |
| **Temps réel** | Oui — subscriber MQTT | Non |
| **Asynchrone** | Oui — Celery + Redis | Non |
| **Tâches planifiées** | Oui — Celery Beat | Non |
| **Emails** | Oui — alertes & incidents | Non |
| **Chiffrement** | — | Tokens API chiffrés (Fernet) |
| **Communication inter-service** | Expose `/api/all-data/` | Consomme les exploitations (`requests`) |

---

## Documentation transverse

- [Django & Django REST Framework](exploitation/02-django-drf.md) — le framework commun aux deux backends
- [Celery & Redis](exploitation/04-celery-redis.md) — synthèse du traitement asynchrone (exploitation uniquement)

## Livrables dédiés aux services asynchrones

Ces deux technologies font l'objet d'un livrable complet et autonome chacune :

- [Redis](../../../../../../../Downloads/livrables/livrables/redis/README.md) — la file de tâches en mémoire (concepts, rôle, configuration, supervision, résilience)
- [Celery](../../../../../../../Downloads/livrables/livrables/celery/README.md) — le traitement asynchrone (architecture, tâches, Beat, workers, résilience, tests)

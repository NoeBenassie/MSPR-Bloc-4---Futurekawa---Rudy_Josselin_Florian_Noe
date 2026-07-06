# 03 — Endpoints de l'API

[← Précédent : Django & DRF](02-django-drf.md) | [Retour à l'index](README.md) | [Suivant : Agrégation des exploitations →](04-agregation-sites.md)

---

## Point d'entrée

Toutes les routes sont sous `/api/` (`core/urls.py` → `siege.api.urls`), plus l'admin Django sur `/admin/`.

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('siege.api.urls')),
    path('api/schema/', SpectacularAPIView.as_view()),
    path('api/docs/',   SpectacularSwaggerView.as_view()),
    path('api/redoc/',  SpectacularRedocView.as_view()),
]
```

---

## Ressources CRUD

| Route | ViewSet | Ressource |
|---|---|---|
| `/api/sites/` | `ExploitationSiteViewSet` | Sites d'exploitation |
| `/api/users/` | `SiegeUserViewSet` | Utilisateurs du siège |

---

## Endpoints d'authentification

| Route | Méthode | Rôle |
|---|---|---|
| `/api/auth/login/` | POST | Connexion → renvoie un token |
| `/api/auth/logout/` | POST | Déconnexion → supprime le token |
| `/api/auth/set-password/` | POST | Définition du mot de passe via token d'invitation |
| `/api/health/` | GET | Sonde de santé |
| `/api/hello/` | GET | Test de connectivité |

---

## Actions personnalisées sur les sites

Le `ExploitationSiteViewSet` ajoute des actions au-delà du CRUD standard : ce sont elles qui font du siège un **proxy** vers les exploitations.

| Action | Route | Rôle |
|---|---|---|
| `sync` | `POST /api/sites/{id}/sync/` | Appelle `/api/all-data/` du site et met à jour le cache |
| `lot_history` | `GET /api/sites/{id}/lots/{batch_id}/history/` | Proxy vers l'historique d'un lot du site |
| `sensor_history` | `GET /api/sites/{id}/sensors/{sensor_id}/history/` | Proxy vers l'historique d'un capteur du site |

> Détail du mécanisme de synchronisation dans [Agrégation des exploitations](04-agregation-sites.md).

---

## Actions personnalisées sur les utilisateurs

| Action | Route | Rôle |
|---|---|---|
| `create` | `POST /api/users/` | Crée l'utilisateur **et** envoie un email d'invitation |
| `resend_invitation` | `POST /api/users/{id}/resend-invitation/` | Régénère un token d'invitation (24 h) |
| `destroy` | `DELETE /api/users/{id}/` | Supprime l'utilisateur |

---

## Exemple : création d'un site

```json
POST /api/sites/
{
  "name": "Plantation Andes",
  "country": "Colombie",
  "api_url": "https://exploit-andes.futurekawa.com",
  "api_token": "9a8b7c6d..."     // sera chiffré avant stockage
}
```

Réponse (le token n'est jamais renvoyé en clair) :

```json
{
  "id": 4,
  "name": "Plantation Andes",
  "country": "Colombie",
  "status": "unknown",
  "last_sync": null
}
```

---

[← Précédent : Django & DRF](02-django-drf.md) | [Retour à l'index](README.md) | [Suivant : Agrégation des exploitations →](04-agregation-sites.md)

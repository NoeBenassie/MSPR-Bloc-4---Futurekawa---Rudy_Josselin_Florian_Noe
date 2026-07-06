# 04 — Couverture API Siège

[← API Exploitation](03-couverture-api-exploitation.md) | [Retour à l'index](README.md) | [Suivant : Simu-Sensor →](05-couverture-simu-sensor.md)

---

## Vue d'ensemble

| Métrique | Valeur |
|---|---|
| **Framework** | Django 4 + Django REST Framework |
| **Runner** | `coverage run manage.py test siege.tests` |
| **Couverture mesurée** | **96 %** (lignes — `coverage.py`) |
| **Fichiers de test** | 6 fichiers |
| **Nombre de tests** | **125 tests** |
| **Chemin** | `API-siege/siege/tests/` |
| **En CI** | ✅ job `api_siege_test` |

---

## Résultats par fichier de test

| Fichier | Tests | Ce qui est couvert |
|---|---|---|
| `test_serializers.py` | 27 | Sérialiseurs DRF — validation, champs calculés, formats |
| `test_views.py` | 54 | Endpoints API complets : CRUD sites, auth, permissions, liste |
| `test_services.py` | 20 | Logique métier pure (`siege/services.py`) |
| `test_user_invitations.py` | 13 | `SiegeUserViewSet` : permissions admin, invitations, renvoi, suppression |
| `test_set_password.py` | 6 | Activation de compte via lien d'invitation (`set_password_view`) |
| `test_exploitation_site.py` | 5 | `ExploitationSiteViewSet.sync` / `cached-data` (proxy HTTP mocké, fallback cache) |
| **Total** | **125** | |

---

## Détail des couvertures clés

### Sérialiseurs (`test_serializers.py` — 27 tests)

Le fichier le plus volumineux sur les sérialiseurs dans le projet :

- Sérialisation d'un `ExploitationSite` (champs `status`, `last_sync`, `api_url`)
- Validation qu'une URL d'exploitation est obligatoire
- Sérialisation d'un `SiegeUser` (rôle, email, actif)
- Champs calculés en lecture seule (`is_active`, `site_count`…)
- Désérialisation avec données incomplètes → erreurs attendues

### Endpoints API (`test_views.py` — 54 tests)

Le fichier central, couvre l'ensemble des routes du siège :

**Authentification :**
- `POST /api/login/` — cookie `access_token` JWT DRF posé
- `POST /api/logout/` — cookie supprimé
- `GET /api/me/` — profil de l'utilisateur connecté
- Accès refusé sans token (401)

**Sites d'exploitation :**
- `GET /api/sites/` — liste paginée (admin voit tout, viewer aussi)
- `POST /api/sites/` — création réservée admin
- `PUT/PATCH /api/sites/:id/` — modification réservée admin
- `DELETE /api/sites/:id/` — suppression réservée admin
- `GET /api/sites/:id/` — détail d'un site

**Synchronisation :**
- `POST /api/sites/:id/sync/` — déclenche un appel HTTP vers l'API exploitation (mocké)
- `GET /api/sites/:id/cache-data/` — retourne `last_data` si l'exploitation est injoignable

**Gestion des rôles :**
- Un `viewer` peut lire mais pas créer/modifier/supprimer
- Un `admin` a accès complet

### Invitations (`test_user_invitations.py` — 13 tests)

Flux d'onboarding des nouveaux utilisateurs siège :

- `POST /api/users/:id/invite/` — génère un token UUID à usage unique
- `POST /api/users/:id/resend-invite/` — renvoie l'email d'invitation
- `DELETE /api/users/:id/` — supprime l'utilisateur et son token
- Un viewer ne peut pas inviter (403)
- Invitation avec email déjà utilisé → erreur

### Activation de compte (`test_set_password.py` — 6 tests)

- `GET /api/set-password/?token=<uuid>` — page d'activation (token valide)
- `POST /api/set-password/` — définit le mot de passe, consomme le token
- Token invalide → 400
- Token déjà utilisé → 400
- Mot de passe trop court → 400

### Proxy exploitation (`test_exploitation_site.py` — 5 tests)

Couvre le comportement du siège quand il contacte une API exploitation distante :

- Sync réussie → `last_data` mis à jour, `status` → `active`
- Exploitation injoignable → retourne le cache `last_data` existant, `status` → `unreachable`
- Exploitation en erreur HTTP 500 → `status` → `error`
- `cache-data` sans `last_data` → réponse vide propre (pas de crash)

---

## Couverture par module

| Module | Couverture |
|---|---|
| `siege/api/views.py` | **98 %** |
| `siege/api/serializers.py` | **97 %** |
| `siege/services.py` | **95 %** |
| `siege/models.py` | **96 %** |
| Module complet | **96 %** |

---

## Comment lancer

```bash
# Tous les tests siège
make test-api-siege

# Un fichier spécifique
docker compose -f docker-compose.siege.yml exec -T api-siege \
    python manage.py test siege.tests.test_views

# Un test spécifique
docker compose -f docker-compose.siege.yml exec -T api-siege \
    python manage.py test siege.tests.test_views.SiegeAuthTest.test_login_sets_cookie

# Avec rapport de couverture
docker compose -f docker-compose.siege.yml exec -T api-siege \
    bash -c "coverage run --source=siege manage.py test siege.tests && coverage report -m"
```

---

[← API Exploitation](03-couverture-api-exploitation.md) | [Retour à l'index](README.md) | [Suivant : Simu-Sensor →](05-couverture-simu-sensor.md)

# 07 — Tests

[← Précédent : Configuration](06-configuration.md) | [Retour à l'index](README.md)

---

## Approche

Les tests du backend siège utilisent le framework de tests Django (`TestCase`, base jetable) avec les settings `core.settings.test`. Aucune infrastructure externe n'est requise : ni Redis, ni broker, ni exploitation réelle (les appels HTTP sortants sont **mockés**).

---

## Ce qui est couvert

| Domaine | Exemples de tests |
|---|---|
| Authentification | Login, logout, throttle anti brute-force |
| Invitations | Création utilisateur, set-password, expiration 24 h, usage unique |
| Sites | CRUD des `ExploitationSite`, filtrage par pays/statut |
| Chiffrement | Le token est bien chiffré en base, déchiffré à la lecture |
| Action `sync` | Proxy vers `/api/all-data/` (réponse `requests` mockée) |
| Statuts de connexion | `active` / `error` / `unreachable` selon la réponse |
| Rôles | Un `viewer` ne peut pas modifier, un `admin` oui |

---

## Mock des appels aux exploitations

Le siège ne doit pas dépendre d'une exploitation en ligne pour ses tests. Les appels `requests.get(...)` sont interceptés :

```python
@patch('siege.api.views.http_requests.get')
def test_sync_success(self, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {...}   # fausse réponse all-data
    # ... POST /api/sites/1/sync/
    # → vérifie last_data, last_sync, status == 'active'
```

---

## Lancer les tests

```bash
cd API-siege
DJANGO_SETTINGS_MODULE=core.settings.test python manage.py test

# ou via le Makefile / la CI
make test-siege
```

---

## Intégration continue

Les tests siège tournent dans la pipeline GitLab CI à chaque push (livrable **CI/CD**). La couverture détaillée figure dans le livrable **Tests** (`04-couverture-api-siege.md`).

---

[← Précédent : Configuration](06-configuration.md) | [Retour à l'index](README.md)

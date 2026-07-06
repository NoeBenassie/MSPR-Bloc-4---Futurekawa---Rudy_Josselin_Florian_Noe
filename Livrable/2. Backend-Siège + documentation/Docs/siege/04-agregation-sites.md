# 04 — Agrégation des exploitations

[← Précédent : Endpoints de l'API](03-endpoints-api.md) | [Retour à l'index](README.md) | [Suivant : Sécurité & chiffrement →](05-securite-chiffrement.md)

---

## Le principe : un proxy qui met en cache

Le siège ne réplique pas les bases des exploitations. Il fait deux choses :

1. Il **appelle** l'endpoint `/api/all-data/` de chaque exploitation (avec le token du site).
2. Il **stocke** la réponse dans le champ `last_data` (JSON) du site, avec la date `last_sync`.

Le frontend siège lit ensuite ce cache — rapide, et disponible même si l'exploitation est momentanément injoignable.

```
Frontend Siège           API Siège                    Exploitation
     │  POST /sites/4/sync/  │                              │
     ├──────────────────────►│                              │
     │                       ├─ GET /api/all-data/ ────────►│
     │                       │   Authorization: Token ...   │
     │                       │◄──── JSON (toute la BDD) ─────┤
     │                       ├─ last_data = JSON             │
     │                       ├─ last_sync = maintenant       │
     │                       ├─ status = 'active'            │
     │◄────── 200 OK ────────┤                              │
```

---

## L'action `sync` en détail

```python
@action(detail=True, methods=['post'])
def sync(self, request, pk=None):
    site = self.get_object()
    url = site.api_url.rstrip('/') + '/api/all-data/'
    resp = http_requests.get(
        url,
        headers={'Authorization': f'Token {site.api_token}'},   # déchiffré à la volée
        timeout=...,
    )
    site.last_data = resp.json()
    site.last_sync = timezone.now()
    site.status = 'active'
    site.save()
```

> `site.api_token` est **déchiffré automatiquement** par l'ORM au moment de la lecture (voir [Sécurité & chiffrement](05-securite-chiffrement.md)). Le code n'a jamais à gérer le chiffrement manuellement.

---

## Le statut de connexion

Chaque site porte un `status` qui reflète le résultat de la dernière synchronisation :

| Statut | Signification |
|---|---|
| `unknown` | Jamais synchronisé |
| `active` | Dernière sync réussie |
| `error` | L'API a répondu une erreur (token invalide, 4xx/5xx) |
| `unreachable` | Site injoignable (timeout, DNS, réseau) |

Cela permet au frontend d'afficher l'état de santé de chaque plantation d'un coup d'œil.

---

## Le cache `last_data`

```python
last_data = models.JSONField(null=True, blank=True)   # toute la réponse /api/all-data/
last_sync = models.DateTimeField(null=True, blank=True)
```

Avantages du cache :

| Avantage | Explication |
|---|---|
| **Rapidité** | Le front lit du JSON local, pas 10 appels réseau distants |
| **Résilience** | Les données restent consultables si l'exploitation est hors ligne |
| **Découplage** | Le siège ne dépend pas de la disponibilité instantanée des sites |

---

## Proxys d'historique

Pour les données volumineuses (historiques de mesures/lots), le siège **ne cache pas** mais relaie la requête en direct vers l'exploitation :

```
GET /api/sites/4/sensors/12/history/
        │
        └─► GET {api_url}/api/sensors/12/history/  (Token du site)
```

Cela évite de dupliquer des milliers de mesures dans le cache du siège.

---

## Résumé du flux inter-service

```
[Exploitation]  expose  /api/all-data/   (protégé par master token)
       ▲
       │ requests.get(headers=Token)
       │
[Siège]  action sync  →  last_data (cache JSON)  →  Frontend Siège
```

---

[← Précédent : Endpoints de l'API](03-endpoints-api.md) | [Retour à l'index](README.md) | [Suivant : Sécurité & chiffrement →](05-securite-chiffrement.md)

# 05 — Sécurité & chiffrement

[← Précédent : Agrégation des exploitations](04-agregation-sites.md) | [Retour à l'index](README.md) | [Suivant : Configuration →](06-configuration.md)

---

## Le risque : des tokens d'accès en clair

Le siège stocke, pour chaque exploitation, un **token d'accès** qui donne un droit de lecture complet sur les données de la plantation (`/api/all-data/`). Si la base du siège fuitait avec ces tokens **en clair**, un attaquant pourrait interroger directement toutes les exploitations.

La parade : **chiffrer les tokens au repos** (encryption at rest) avec **Fernet** (bibliothèque `cryptography`).

---

## Fernet en bref

> **Fernet** = chiffrement symétrique authentifié. Une même clé secrète chiffre et déchiffre ; le message est aussi signé, donc toute altération est détectée.

```python
# siege/utils/encryption.py
from cryptography.fernet import Fernet

def _fernet() -> Fernet:
    return Fernet(settings.SITE_TOKEN_ENCRYPTION_KEY.encode())

def encrypt_token(plaintext: str) -> str:
    return _fernet().encrypt(plaintext.encode()).decode()

def decrypt_token(ciphertext: str) -> str:
    return _fernet().decrypt(ciphertext.encode()).decode()
```

La clé provient d'une variable d'environnement, **jamais du code** :

```python
# core/settings/base.py
SITE_TOKEN_ENCRYPTION_KEY = os.environ.get('SITE_TOKEN_ENCRYPTION_KEY', ...)
```

---

## Chiffrement transparent via l'ORM

Le token n'est jamais chiffré/déchiffré « à la main » dans les vues. Le champ personnalisé `EncryptedCharField` s'en charge à chaque aller-retour base de données :

```python
class EncryptedCharField(models.TextField):
    def from_db_value(self, value, expression, connection):
        return decrypt_token(value) if value else value   # lecture → clair

    def get_prep_value(self, value):
        return encrypt_token(value) if value else value    # écriture → chiffré
```

```
Code applicatif          Base PostgreSQL
site.api_token = "abc"  ──get_prep_value──►  "gAAAAAB...=" (chiffré)
site.api_token          ◄──from_db_value───  "gAAAAAB...=" → "abc"
```

Résultat : en base, la colonne `api_token` ne contient **que du chiffré** ; le reste du code voit toujours le token en clair.

---

## Autres mesures de sécurité

| Mesure | Mise en œuvre |
|---|---|
| **Auth par token** | `rest_framework.authtoken` — token émis à la connexion |
| **Anti brute-force** | `LoginRateThrottle` limite les tentatives de login |
| **Tokens d'invitation** | UUID à usage unique, **expiration 24 h**, supprimé après usage |
| **Le token de site n'est jamais renvoyé** | Absent des réponses de l'API (write-only) |
| **CORS restreint en prod** | `CORS_ALLOWED_ORIGINS` explicite (pas d'`ALLOW_ALL`) |
| **Rôles** | `admin` vs `viewer` — les lecteurs n'ont pas les droits d'écriture |

---

## Cycle d'un token d'invitation

```
Admin crée un utilisateur
   │
   ├─ InvitationToken (UUID, expire dans 24 h)
   ├─ email envoyé : .../set-password?token=<uuid>
   │
Utilisateur ouvre le lien → POST /api/auth/set-password/
   ├─ token valide et non expiré ?
   ├─ définit le mot de passe
   └─ token SUPPRIMÉ (usage unique)
```

---

## Bonnes pratiques appliquées

- Secrets (`SECRET_KEY`, `SITE_TOKEN_ENCRYPTION_KEY`, identifiants SMTP) en **variables d'environnement**, jamais commités.
- `DEBUG=False` en production (`core.settings.production`).
- Voir aussi le document transverse `futurekawa-securite.md` à la racine du dépôt.

---

[← Précédent : Agrégation des exploitations](04-agregation-sites.md) | [Retour à l'index](README.md) | [Suivant : Configuration →](06-configuration.md)

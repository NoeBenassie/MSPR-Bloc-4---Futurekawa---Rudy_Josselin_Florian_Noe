# 02 — Django & Django REST Framework

[← Précédent : Vue d'ensemble](01-vue-ensemble.md) | [Retour à l'index](README.md) | [Suivant : Endpoints de l'API →](03-endpoints-api.md)

---

## Rappel : Django & DRF

Le siège partage le même socle que l'exploitation : **Django** (framework web Python, ORM, migrations) et **Django REST Framework** (API JSON). Le fonctionnement général — modèles, serializers, viewsets, routeurs — est décrit en détail dans le [livrable Backend Exploitation](../../../Backend-Pays%20+%20documentation/Docs/backend/exploitation/02-django-drf.md). Cette section se concentre sur ce qui est **propre au siège**.

---

## Particularité 1 : un modèle utilisateur personnalisé

Contrairement à l'exploitation qui utilise le `User` standard de Django, le siège définit **son propre modèle utilisateur** en héritant d'`AbstractUser` :

```python
# siege/models.py
class SiegeUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin',  'Administrateur'),
        ('viewer', 'Lecteur'),
    ]
    role  = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    email = models.EmailField(unique=True)
```

| Ajout | Raison |
|---|---|
| Champ `role` | Distinguer administrateurs et simples lecteurs |
| `email` unique | L'email sert d'identifiant fort (invitations) |

> Django est configuré avec `AUTH_USER_MODEL = 'siege.SiegeUser'`. C'est une décision qui se prend **dès le début** d'un projet, car changer de modèle utilisateur ensuite est coûteux.

---

## Particularité 2 : un champ de modèle sur mesure

Le siège crée un **type de champ personnalisé**, `EncryptedCharField`, qui chiffre/déchiffre automatiquement sa valeur à la traversée de la base :

```python
class EncryptedCharField(models.TextField):
    def from_db_value(self, value, expression, connection):
        return decrypt_token(value) if value else value   # lecture → déchiffre

    def get_prep_value(self, value):
        return encrypt_token(value) if value else value    # écriture → chiffre
```

Utilisé pour le token d'accès aux exploitations :

```python
class ExploitationSite(models.Model):
    api_token = EncryptedCharField()   # jamais stocké en clair
```

> Le code applicatif manipule le token en clair ; le chiffrement est **transparent**, géré par l'ORM. Détails dans [Sécurité & chiffrement](05-securite-chiffrement.md).

---

## Particularité 3 : `django-filter`

Le siège ajoute `django_filters` pour filtrer les listes de l'API sans écrire de code :

```python
# ex. filtrer les sites par pays ou statut
GET /api/sites/?country=Colombie&status=active
```

---

## Authentification par token

Le siège active `rest_framework.authtoken` : à la connexion, l'utilisateur reçoit un token porté ensuite dans chaque requête.

```python
# à la connexion
token, _ = Token.objects.get_or_create(user=user)
# → { "token": "..." }

# dans les requêtes suivantes
Authorization: Token <clé>
```

Un **throttle** limite les tentatives de connexion (`LoginRateThrottle`) pour contrer le brute-force.

---

## Documentation automatique

Comme l'exploitation, le siège expose sa doc OpenAPI via `drf-spectacular` :

| URL | Contenu |
|---|---|
| `/api/schema/` | Schéma OpenAPI |
| `/api/docs/` | Swagger interactif |
| `/api/redoc/` | ReDoc |

---

## Interface d'administration

Le siège active `django.contrib.admin` (l'exploitation ne l'utilise pas). L'admin Django offre une interface auto-générée pour gérer sites et utilisateurs, accessible sur `/admin/`.

---

[← Précédent : Vue d'ensemble](01-vue-ensemble.md) | [Retour à l'index](README.md) | [Suivant : Endpoints de l'API →](03-endpoints-api.md)

# 05 — Stage Sécurité

[← Staging](04-staging.md) | [Suivant : Deploy →](06-deploy.md)

---

## Rôle

Le stage `security` exécute des analyses de sécurité statiques sur le code. Il utilise les **templates GitLab CI gratuits** disponibles sur le tier Free.

---

## Templates inclus

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml
  - template: Jobs/Secret-Detection.gitlab-ci.yml
```

---

## Job : `semgrep-sast` — Analyse statique de sécurité

**SAST** (Static Application Security Testing) analyse le code source à la recherche de vulnérabilités connues (injections, mauvaise gestion des secrets, failles d'authentification…).

GitLab utilise **Semgrep** pour les projets Python et JavaScript/TypeScript.

**Résultats :** disponibles dans l'onglet « Sécurité » de la MR GitLab et dans les artifacts du job.

---

## Job : `secret_detection` — Détection de secrets

Analyse tous les commits de la branche pour détecter des secrets commités par erreur :
- Clés API
- Mots de passe
- Tokens JWT
- Clés SSH / certificats

**Important :** ce job analyse l'**historique Git**, pas seulement les nouveaux fichiers. Un secret supprimé dans un commit ultérieur sera quand même détecté.

---

## Positionnement dans le pipeline

Les jobs SAST et Secret Detection sont assignés au stage `security` dans `.gitlab-ci.yml` pour les regrouper visuellement. Par défaut, les templates GitLab les mettent dans `test` — le fichier CI les réassigne explicitement :

```yaml
semgrep-sast:
  stage: security

secret_detection:
  stage: security
```

---

## Ce qui n'est pas inclus (réservé GitLab Ultimate)

| Feature | Disponibilité |
|---|---|
| Dependency Scanning | Ultimate uniquement |
| Container Scanning | Ultimate uniquement |
| DAST | Ultimate uniquement |

---

[← Staging](04-staging.md) | [Suivant : Deploy →](06-deploy.md)

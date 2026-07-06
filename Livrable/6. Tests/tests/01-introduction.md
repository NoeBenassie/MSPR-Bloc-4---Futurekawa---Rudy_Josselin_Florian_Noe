# 01 — Introduction aux tests

[← Retour à l'index](README.md) | [Suivant : Lancement →](02-lancement.md)

---

## Pourquoi tester ?

Les tests garantissent que chaque composant du système fonctionne correctement **isolément** et **en interaction** avec les autres. Dans un système distribué comme FutureKawa (deux APIs, deux frontends, un broker IoT, des tâches asynchrones), un test manquant peut laisser passer une régression silencieuse entre deux services.

---

## Types de tests utilisés

### Tests unitaires

Un test unitaire vérifie **un seul composant en isolation**. Toutes les dépendances externes (base de données, réseau, autres modules) sont remplacées par des substituts contrôlés (mocks).

**Exemples dans FutureKawa :**
- Vérifier qu'un sérialiseur Django rejette un champ manquant
- Vérifier qu'un composant Vue affiche correctement un slot vide
- Vérifier que la fonction de calcul des seuils retourne la bonne valeur

**Ce qu'ils garantissent :** la logique interne est correcte.  
**Ce qu'ils ne garantissent pas :** que les composants fonctionnent ensemble.

---

### Tests d'intégration

Un test d'intégration vérifie **plusieurs composants en interaction**. La base de données réelle est utilisée, les appels HTTP sont simulés ou réels selon le contexte.

**Exemples dans FutureKawa :**
- Appeler `POST /api/login/` et vérifier que le cookie JWT est bien posé
- Vérifier que la création d'une alerte déclenche bien la tâche Celery
- Vérifier que le proxy siège → exploitation retourne les données en cache si l'exploitation est injoignable
- Vérifier les permissions d'accès (un opérateur ne peut pas accéder aux paramètres)

**Ce qu'ils garantissent :** les contrats entre composants sont respectés.  
**Ce qu'ils ne garantissent pas :** l'expérience utilisateur réelle dans un navigateur.

---

### Tests End-to-End (E2E)

Un test E2E simule **un utilisateur réel** dans un navigateur : navigation, clics, saisie de formulaires, vérification de l'affichage. Toute la stack doit être démarrée.

**Exemples dans FutureKawa :**
- Un utilisateur se connecte, navigue vers un entrepôt, voit les mesures en temps réel
- Un admin crée un compte utilisateur via le lien d'invitation
- Le simulateur envoie une mesure et l'alerte apparaît dans l'interface

**Ce qu'ils garantissent :** le parcours utilisateur complet fonctionne.  
**Ce qu'ils ne garantissent pas :** les cas limites ou les chemins d'erreur internes.

---

## Les trois niveaux en résumé

```
        ┌─────────────────────────────────┐
        │      E2E (Playwright)           │  ← lent, rare, haute valeur
        │  Navigateur + stack complète    │
        ├─────────────────────────────────┤
        │   Intégration (Django TestCase) │  ← moyen, couverture large
        │   BDD réelle + HTTP simulé      │
        ├─────────────────────────────────┤
        │   Unitaire (Vitest / unittest)  │  ← rapide, nombreux, précis
        │   Composant isolé + mocks       │
        └─────────────────────────────────┘
```

| | Unitaire | Intégration | E2E |
|---|---|---|---|
| **Vitesse** | Très rapide (ms) | Rapide (< 1 s) | Lent (5–30 s) |
| **Fiabilité** | Très stable | Stable | Fragile (dépend du DOM) |
| **Portée** | 1 fonction/composant | N composants | Flux complet |
| **Quantité** | Beaucoup | Moyen | Peu |
| **En CI** | ✅ Toujours | ✅ Toujours | ⚠️ Hors CI (pour l'instant) |

---

## Outils utilisés

### Backend — Python / Django

| Outil | Rôle |
|---|---|
| **`unittest` / `TestCase` Django** | Framework de test natif Django — gère BDD de test, fixtures, client HTTP |
| **`coverage.py`** | Mesure la couverture de code ligne par ligne |
| **`django.test.Client`** | Client HTTP qui simule des requêtes vers les endpoints DRF |
| **`unittest.mock`** | Mocks Python (patch d'appels HTTP externes, tâches Celery…) |

```bash
# Exécution Django avec couverture
coverage run manage.py test
coverage report --include="exploitation/*"
```

---

### Frontend — Vue 3 / TypeScript

| Outil | Rôle |
|---|---|
| **Vitest** | Runner de tests unitaires/composants pour projets Vite — compatible Jest API |
| **`@vue/test-utils`** | Monte les composants Vue en mémoire, simule les interactions |
| **`vi.mock()`** | Remplace les modules (axios, router, pinia stores) par des mocks |
| **`@vitest/coverage-v8`** | Mesure la couverture via le moteur V8 de Node |

```bash
# Exécution Vitest avec couverture
npm run test:coverage
```

---

### E2E — Playwright

| Outil | Rôle |
|---|---|
| **Playwright** | Pilote des navigateurs réels (Chromium, Firefox, WebKit, Mobile) |
| **`test.spec.ts`** | Fichiers de scénarios : navigation, clics, assertions sur le DOM |
| **`playwright.config.ts`** | Configuration des navigateurs cibles et URL de base |

```bash
# Exécution E2E (frontend doit être démarré)
npx playwright test
npx playwright test --ui   # mode visuel interactif
```

---

### Broker MQTT

| Outil | Rôle |
|---|---|
| **Script shell `test_acl.sh`** | Vérifie les règles ACL Mosquitto (pub/sub autorisés vs refusés) |
| **`mosquitto_pub` / `mosquitto_sub`** | Clients MQTT en ligne de commande pour les assertions |

---

## Ce qui tourne en CI vs en local

| Suite | CI (GitLab) | Local |
|---|---|---|
| Tests unitaires/intégration Django | ✅ | ✅ |
| Tests Vitest frontends | ✅ | ✅ |
| Tests Vitest simu-sensor | ✅ | ✅ |
| Tests ACL broker | ✅ | ✅ |
| E2E Playwright | ❌ hors CI | ✅ (`make test-*-e2e`) |

> Les tests E2E ne tournent pas en CI car ils nécessitent une stack complète démarrée. La piste envisagée est de les rattacher au stage `staging` du pipeline, après le smoke test, pour profiter de la stack déjà levée.

---

## Comment lire l'indice de couverture

### Ce que mesure le pourcentage

L'indice de couverture indique la **proportion de lignes de code source effectivement exécutées** lors de la suite de tests. Une couverture de 96 % signifie que 96 % des lignes du code applicatif ont été traversées au moins une fois pendant les tests.

```
couverture = lignes exécutées pendant les tests / total des lignes du code source
```

Ce n'est pas un indice de qualité absolu — une ligne peut être exécutée sans être correctement testée — mais c'est un indicateur fiable pour repérer des zones **jamais couvertes**.

---

### Périmètre inclus et exclu

#### Backend Django — `coverage.py`

La commande utilisée est :
```bash
coverage run --source=<app> manage.py test <app>.tests
```

| Inclus | Exclus |
|---|---|
| Modèles, vues, sérialiseurs, permissions | Migrations (`migrations/`) |
| Commandes de gestion (`management/`) | Fichiers de settings |
| Tâches Celery | Code tiers (Django, DRF) |
| Utilitaires internes | Fichiers `wsgi.py`, `asgi.py` |

#### Frontend Vue / TypeScript — `@vitest/coverage-v8`

La couverture est mesurée par le moteur **V8** de Node.js (même moteur que Chrome). Elle couvre :

| Inclus | Exclus |
|---|---|
| Composants Vue (`.vue`) | Fichiers de config (`vite.config.ts`, …) |
| Services et stores Pinia | Assets statiques |
| Utilitaires TypeScript | Tests eux-mêmes (`*.spec.ts`) |

#### Broker MQTT

Le broker n'a pas de couverture de lignes : les 8 assertions vérifient les **règles ACL** (pub/sub autorisés vs refusés). Le « 100 % » indique que toutes les règles de la matrice ACL ont été testées.

---

### Ce que la couverture ne garantit pas

- Qu'un comportement incorrect soit détecté si l'assertion est trop permissive
- Que les cas limites aux frontières des données soient testés
- Que les interactions entre services fonctionnent (c'est le rôle des tests d'intégration et E2E)

---

[← Retour à l'index](README.md) | [Suivant : Lancement →](02-lancement.md)

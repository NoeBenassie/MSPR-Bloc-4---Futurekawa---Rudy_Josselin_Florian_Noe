# 07 — Couverture Front Siège

[← Front Exploitation](06-couverture-front-exploitation.md) | [Retour à l'index](README.md) | [Suivant : Broker MQTT →](08-couverture-broker.md)

---

## Vue d'ensemble

| Métrique | Valeur |
|---|---|
| **Framework** | Vue 3 + TypeScript + Vite |
| **Runner** | Vitest |
| **Couverture mesurée** | **~95 %** (33/33 fichiers couverts) |
| **Fichiers de test** | 41 fichiers |
| **Nombre de tests** | **250 tests** |
| **Chemin** | `front-siege/src/**/__tests__/` et `front-siege/src/components/organisms/` |
| **En CI** | ✅ job `front_siege_test` |

---

## Résultats par dossier

| Dossier | Fichiers de test | Tests |
|---|---|---|
| `components/atoms/` | 4 | 23 |
| `components/molecules/` | 2 | 10 |
| `components/organisms/` | 5 | 33 |
| `components/__tests__/` | 6 | 33 |
| `services/__tests__/` | 6 | 27 |
| `stores/__tests__/` | 2 | 18 |
| `utils/__tests__/` | 1 | 11 |
| `pages/__tests__/` | 7 | 43 |
| `views/__tests__/` | 8 | 52 |
| **Total** | **41** | **250** |

---

## Composants couverts

| Composant | Chemin | Tests |
|---|---|---|
| `Header.vue` | `components/organisms/` | 5 |
| `LoginForm.vue` | `components/organisms/` | 7 |
| `SiteForm.vue` | `components/organisms/` | 6 |
| `UserForm.vue` | `components/organisms/` | 9 |
| `Toast.vue` | `components/__tests__/` | 6 |
| `AdminSitesPage.vue` | `pages/__tests__/` | 6 |
| `AdminUsersPage.vue` | `pages/__tests__/` | 7 |
| `DashboardPage.vue` | `pages/__tests__/` | 7 |
| `LoginPage.vue` | `pages/__tests__/` | 4 |
| `ProfilePage.vue` | `pages/__tests__/` | 6 |
| `SiteDetailPage.vue` | `pages/__tests__/` | 6 |
| `SetPasswordPage.vue` | `pages/__tests__/` | 7 |

---

## Stratégies de mock utilisées

- **Stores Pinia** : objets mutables au niveau module (`const mockAuthStore = { ... }`) modifiés dans `beforeEach` — évite les conflits de hoisting de `vi.mock()`
- **Vue Router** : mock complet de `useRoute`, `useRouter`, `RouterLink`
- **Remixicon** : stub de chaque icône en `<span />` pour éviter les erreurs d'import SVG
- **Composants enfants** : stub des `Header`, `FormField`, `Button` pour isoler la logique du composant testé

---

## E2E Playwright

Un scénario E2E existe dans `front-siege/tests/e2e/admin-user-creation.spec.ts`. Il nécessite l'installation de `@playwright/test` :

```bash
cd front-siege && npm install --save-dev @playwright/test
```

---

## Comment lancer

```bash
cd front-siege && npm install && npm test
cd front-siege && npm run test:coverage

# Un fichier spécifique
cd front-siege && npm test -- src/pages/__tests__/SiteDetailPage.test.ts
```

---

[← Front Exploitation](06-couverture-front-exploitation.md) | [Retour à l'index](README.md) | [Suivant : Broker MQTT →](08-couverture-broker.md)

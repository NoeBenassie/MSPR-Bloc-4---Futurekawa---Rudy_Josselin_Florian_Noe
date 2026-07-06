# 05 — Couverture Simu-Sensor

[← API Siège](04-couverture-api-siege.md) | [Retour à l'index](README.md) | [Suivant : Front Exploitation →](06-couverture-front-exploitation.md)

---

## Vue d'ensemble

| Métrique | Valeur |
|---|---|
| **Framework** | Vue 3 + TypeScript + Vite |
| **Runner** | Vitest |
| **Couverture estimée** | **~95 %** |
| **Fichiers de test unitaires** | 14 fichiers |
| **Tests unitaires/intégration** | **166 tests** |
| **Scénarios E2E** | 22 scénarios × 5 navigateurs = 110 exécutions |
| **Chemin tests unitaires** | `simu-sensor/src/**/__tests__/` |
| **Chemin E2E** | `simu-sensor/tests/e2e/` |
| **En CI** | ✅ job `simu_sensor_test` (unitaires) — E2E hors CI |

---

## Rôle du simu-sensor

Le simu-sensor est une application Vue 3 qui **simule un capteur IoT (ESP32)** pour la démonstration. Il génère des données de température et d'humidité aléatoires (avec bruit configurable) et les publie sur le broker MQTT via WebSocket, en se comportant exactement comme un vrai capteur.

Il est utilisé pour la stack **São Paulo** (`docker-compose.exploit.yml`, profil `demo`).

---

## Résultats par dossier de test

| Dossier | Fichiers | Tests | Ce qui est couvert |
|---|---|---|---|
| `components/__tests__/` | 5 | 45 | Composants Vue (sliders, indicateurs, boutons) |
| `config/__tests__/` | 1 | 14 | Configuration MQTT, topics, valeurs par défaut |
| `services/__tests__/` | 3 | 27 | Service MQTT (connexion, publication, déconnexion) |
| `__tests__/` (App + intégration) | 5 | 80 | App.vue + flux complet de simulation |
| **Total** | **14** | **166** | |

---

## Détail des couvertures

### Composants Vue (`components/__tests__/` — 45 tests)

Les composants UI du simulateur :

- **Slider de température / humidité** : valeur min/max respectée, émission de l'événement `update:modelValue`
- **Indicateur de statut MQTT** : affiche `connecté` / `déconnecté` selon le prop `connected`
- **Bouton démarrer/arrêter** : état visuel correct, émission du clic
- **Affichage des valeurs courantes** : format numérique, unités (°C, %)
- **Panel de configuration** : binding bidirectionnel des champs

### Configuration (`config/__tests__/` — 14 tests)

- Topics MQTT par défaut : `capteur/simu-sensor/temperature`, `capteur/simu-sensor/humidity`
- Valeurs de simulation par défaut (plage T°, plage humidité)
- `SENSOR_ID` lu depuis `VITE_SENSOR_ID` (variable d'environnement)
- Fallback sur `'simu-sensor-1'` si la variable n'est pas définie
- Fréquence d'envoi configurable

### Service MQTT (`services/__tests__/` — 27 tests)

Couvre `mqttService.ts` — le cœur du simulateur :

- Connexion WebSocket au broker (`ws://broker:9001`)
- Déconnexion propre (unsubscribe + disconnect)
- Publication d'un payload JSON avec `sensor_id` :
  ```json
  { "value": 28.4, "sensor_id": "simu-sensor-1", "timestamp": "..." }
  ```
- Retry automatique en cas de déconnexion
- Callback `onConnect` / `onDisconnect` appelés au bon moment
- Publication bloquée si non connecté

### App.vue + intégration (`__tests__/` — 80 tests)

Tests du flux complet de simulation :

- Démarrage de la simulation → intervalles créés, publications régulières
- Arrêt de la simulation → intervalles nettoyés, aucune publication
- Variation des valeurs dans les plages configurées (pas de sortie hors bornes)
- Bruit aléatoire : chaque publication produit une valeur différente de la précédente
- Publication simultanée T° + humidité à chaque tick
- Nettoyage des ressources au `unmount` (pas de fuite mémoire)

---

## Tests E2E Playwright

### Configuration

5 navigateurs/appareils ciblés dans `playwright.config.ts` :

| Profil | Moteur |
|---|---|
| Desktop Chromium | Chromium |
| Desktop Firefox | Firefox |
| Desktop Safari | WebKit |
| Mobile Chrome | Chromium (mobile) |
| Mobile Safari | WebKit (mobile) |

→ **22 scénarios × 5 = 110 exécutions** à chaque lancement.

### Scénarios couverts (extrait)

- Chargement de l'application → affichage des contrôles
- Connexion au broker → indicateur de statut passe au vert
- Démarrage de la simulation → les valeurs affichées changent
- Modification des plages min/max → les valeurs publiées respectent les nouvelles bornes
- Arrêt de la simulation → les publications cessent
- Déconnexion du broker → indicateur rouge, retry affiché
- Responsive : l'UI reste utilisable sur mobile (375px)

### Lancement

```bash
# Via Makefile
make test-simu-sensor-e2e         # headless (tous les navigateurs)
make test-simu-sensor-e2e-ui      # mode visuel interactif

# Direct depuis le dossier
cd simu-sensor && npx playwright test
cd simu-sensor && npx playwright test --reporter=html  # rapport HTML
```

> Pré-requis : le simu-sensor doit être accessible sur `http://localhost:8181` (démarré avec `make demo` ou `make full`).

---

## Comment lancer les tests unitaires

```bash
# Via Makefile
make test-simu-sensor

# Direct depuis le dossier
cd simu-sensor && npm install && npm test

# Avec couverture
cd simu-sensor && npm run test:coverage

# Watch mode (relance à chaque sauvegarde)
cd simu-sensor && npm run test -- --watch

# Un fichier spécifique
cd simu-sensor && npm test -- src/services/__tests__/mqttService.test.ts
```

---

[← API Siège](04-couverture-api-siege.md) | [Retour à l'index](README.md) | [Suivant : Front Exploitation →](06-couverture-front-exploitation.md)

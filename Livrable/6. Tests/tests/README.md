# Rapport de Tests — FutureKawa

---

```
  _____      _                _  __
 |  ___|   _| |_ _   _ _ __ ___| |/ /__ ___      ____ _
 | |_ | | | | __| | | | '__/ _ \ ' // _` \ \ /\ / / _` |
 |  _|| |_| | |_| |_| | | |  __/ . \ (_| |\ V  V / (_| |
 |_|   \__,_|\__|\__,_|_|  \___|_|\_\__,_| \_/\_/ \__,_|
```

---

|              |                                     |
|---|---|
| **Projet**   | FutureKawa |
| **Document** | Rapport de tests et couverture        |
| **Version**  | 1.0                                   |
| **Date**     | 01/07/2026                            |
| **Équipe**   | Rudy · Florian · Noé · Josselin         |

---

## Résumé exécutif

| Service | Tests en CI | Couverture | Statut |
|---|---|---|---|
| API Exploitation | 150 | 96 % | OK |
| API Siège | 125 | 96 % | OK |
| Front Exploitation | 165 | ~97 % | OK |
| Front Siège | 250 | ~95 % | OK |
| Simu-Sensor | 166 | ~95 % | OK |
| Broker MQTT | 8 | 100 % | OK |
| IoT ESP32 | 36 | comportementale | OK |
| **Total CI** | **836** | **~95 %** | **OK** |

> En complément, **85 scénarios E2E** (236 exécutions multi-navigateurs) sont disponibles en local.

> **Légende — Couverture** : pourcentage de lignes du code source applicatif exécutées lors des tests. Mesuré par `coverage.py` (Django) et `@vitest/coverage-v8` (Vue/TS). Hors migrations, configurations et bibliothèques tierces. Pour le broker, « 100 % » signifie que toutes les règles ACL ont été vérifiées.

---

## Navigation

| # | Document | Contenu |
|---|---|---|
| 1 | [Introduction](01-introduction.md) | Types de tests (unitaire, intégration, E2E) — outils utilisés |
| 2 | [Lancement des tests](02-lancement.md) | Commandes manuelles (Makefile) et pipeline CI/CD automatique |
| 3 | [Couverture — API Exploitation](03-couverture-api-exploitation.md) | 128 tests Django, 94 % de couverture |
| 4 | [Couverture — API Siège](04-couverture-api-siege.md) | 125 tests Django, 96 % de couverture |
| 5 | [Couverture — Simu-Sensor](05-couverture-simu-sensor.md) | 166 tests Vitest + E2E Playwright, ~95 % |
| 6 | [Couverture — Front Exploitation](06-couverture-front-exploitation.md) | 165 tests Vitest, ~97 % |
| 7 | [Couverture — Front Siège](07-couverture-front-siege.md) | 250 tests Vitest, ~95 % |
| 8 | [Couverture — Broker MQTT](08-couverture-broker.md) | 8 assertions ACL, 100 % |
| 9 | [Couverture — IoT ESP32](09-couverture-iot.md) | 36 tests Python (scripts, validation capteur, payloads MQTT) |

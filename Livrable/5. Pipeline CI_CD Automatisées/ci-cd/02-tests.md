# 02 — Stage Test

[← Lint](01-lint.md) | [Suivant : Build →](03-build.md)

---

## Rôle

Le stage `test` exécute tous les tests automatisés en CI. Chaque job tourne dans un container isolé, produit un rapport JUnit et un rapport de couverture au format Cobertura.

---

## Jobs

### `api_siege_test` — Django (Python 3.11)

Lance les tests unitaires et d'intégration de l'API siège avec couverture.

```bash
cd API-siege
pip install -r requirements.txt unittest-xml-reporting coverage
coverage run --source=siege manage.py test siege.tests
coverage report
coverage xml -o coverage.xml
```

**Variables :** `DJANGO_SETTINGS_MODULE: core.settings.test`

**Artifacts :**
- Rapport JUnit : `API-siege/test-reports/*.xml`
- Couverture Cobertura : `API-siege/coverage.xml`

---

### `api_exploitation_test` — Django (Python 3.11)

Identique pour l'API exploitation.

```bash
cd API-exploitation
coverage run --source=exploitation manage.py test exploitation.tests
```

**Artifacts :**
- Rapport JUnit : `API-exploitation/test-reports/*.xml`
- Couverture Cobertura : `API-exploitation/coverage.xml`

---

### `simu_sensor_test` — Vitest (Node 20)

Lance les tests Vitest du simulateur de capteur avec couverture V8.

```bash
cd simu-sensor
npm ci
npm run test:coverage
```

**Artifacts :**
- Rapport JUnit : `simu-sensor/junit.xml`
- Couverture Cobertura : `simu-sensor/coverage/cobertura-coverage.xml`

---

### `front_siege_test` — Vitest (Node 20)

Lance les tests Vitest du frontend siège.

```bash
cd front-siege
npm ci
npm run test:coverage
```

**Artifacts :**
- Rapport JUnit : `front-siege/junit.xml`
- Couverture Cobertura : `front-siege/coverage/cobertura-coverage.xml`

---

### `front_exploitation_test` — Vitest (Node 20)

Lance les tests Vitest du frontend exploitation.

```bash
cd front-exploitation
npm ci
npm run test:coverage
```

---

### `broker_acl_test` — Docker-in-Docker

Test spécial : lance un container Mosquitto et vérifie les règles ACL avec le script `broker/tests/test_acl.sh`.

```bash
docker network create mqtt-test-net
docker build -t broker-test broker/
docker run -d --name broker-test --network mqtt-test-net broker-test
docker run --rm eclipse-mosquitto:2.0 sh /tests/test_acl.sh broker-test 1883
```

Vérifie que les publications/souscriptions MQTT autorisées fonctionnent et que celles interdites sont bien rejetées.

---

## Résumé des résultats

| Service | Tests | Couverture |
|---|---|---|
| API Siège | ~125 | 96 % |
| API Exploitation | ~150 | 96 % |
| Front Siège | ~250 | ~95 % |
| Front Exploitation | ~165 | ~97 % |
| Simu-Sensor | ~166 | ~95 % |
| Broker MQTT | 8 assertions ACL | 100 % |

---

## Tests non inclus en CI

Les tests E2E Playwright ne tournent pas en CI car ils nécessitent une stack complète. Ils sont disponibles en local :

```bash
make test-simu-sensor-e2e
```

---

[← Lint](01-lint.md) | [Suivant : Build →](03-build.md)

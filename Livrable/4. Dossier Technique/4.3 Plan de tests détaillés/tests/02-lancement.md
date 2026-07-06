# 02 — Lancement des tests

[← Introduction](01-introduction.md) | [Retour à l'index](README.md) | [Suivant : Couverture API Exploitation →](03-couverture-api-exploitation.md)

---

## 1. Lancement manuel — Makefile

Le Makefile à la racine du projet est le point d'entrée unique pour lancer tous les tests manuellement. Aucune configuration préalable n'est nécessaire au-delà d'une stack Docker démarrée.

### Tous les tests en une commande

```bash
make test
```

Lance séquentiellement les tests de chaque service et affiche un bilan global :

```
--- API Exploitation ---
...128 tests, 94% coverage...
✅ API Exploitation OK

--- API Siège ---
...125 tests, 96% coverage...
✅ API Siège OK

--- Simu Sensor ---
...166 tests, ~95% coverage...
✅ Simu Sensor OK
```

---

### Par service

| Service | Commande |
|---|---|
| API Exploitation (Django) | `make test-api-exploitation` |
| API Siège (Django) | `make test-api-siege` |
| Simu-Sensor (Vitest) | `make test-simu-sensor` |
| Simu-Sensor E2E (Playwright) | `make test-simu-sensor-e2e` |
| Simu-Sensor E2E (mode visuel) | `make test-simu-sensor-e2e-ui` |

---

### Détail des commandes sous-jacentes

#### API Exploitation

```bash
# Via Makefile (recommandé)
make test-api-exploitation

# Équivalent direct dans le container
docker compose -f docker-compose.exploit.yml exec -T api-exploitation \
    python manage.py test

# Avec couverture (comme en CI)
docker compose -f docker-compose.exploit.yml exec -T api-exploitation \
    bash -c "pip install coverage && \
             coverage run --source=exploitation manage.py test exploitation.tests && \
             coverage report"

# Un seul fichier de test
docker compose -f docker-compose.exploit.yml exec -T api-exploitation \
    python manage.py test exploitation.tests.test_alert_viewset
```

#### API Siège

```bash
# Via Makefile
make test-api-siege

# Avec couverture
docker compose -f docker-compose.siege.yml exec -T api-siege \
    bash -c "pip install coverage && \
             coverage run --source=siege manage.py test siege.tests && \
             coverage report"

# Un seul fichier de test
docker compose -f docker-compose.siege.yml exec -T api-siege \
    python manage.py test siege.tests.test_views
```

#### Simu-Sensor (Vitest)

```bash
# Via Makefile
make test-simu-sensor

# Hors Docker — depuis le dossier simu-sensor/
cd simu-sensor && npm install && npm test

# Avec couverture interactive
cd simu-sensor && npm run test:coverage

# Watch mode (relance automatique à chaque sauvegarde)
cd simu-sensor && npm run test -- --watch
```

#### Broker MQTT

```bash
# Lancé automatiquement dans make test
# Exécutable séparément :
bash broker/tests/test_acl.sh
```

#### Front Exploitation (Vitest)

```bash
cd front-exploitation && npm install && npm test
cd front-exploitation && npm run test:coverage
```

#### Front Siège (Vitest)

```bash
cd front-siege && npm install && npm test
cd front-siege && npm run test:coverage
```

---

### Tests E2E (Playwright)

> Les tests E2E nécessitent que la stack soit démarrée (`make full` ou `make demo`).

```bash
# Simu-Sensor E2E
make test-simu-sensor-e2e         # headless (tous les navigateurs)
make test-simu-sensor-e2e-ui      # mode visuel interactif

# Front Exploitation E2E (hors Makefile)
cd front-exploitation && npx playwright test
cd front-exploitation && npx playwright test --ui

# Front Siège E2E (hors Makefile — dépendance @playwright/test manquante)
# cd front-siege && npx playwright test
```

---

## 2. Lancement automatique — Pipeline GitLab CI

Le pipeline GitLab s'exécute automatiquement à chaque `git push` sur n'importe quelle branche. Il est défini dans `.gitlab-ci.yml` à la racine du projet.

### Stages du pipeline

```
lint ──► test ──► build ──► staging ──► security ──► deploy
```

### Stage `test` — jobs de test

| Job GitLab | Service testé | Framework | Couverture publiée |
|---|---|---|---|
| `simu_sensor_test` | simu-sensor | Vitest | ✅ Cobertura XML |
| `api_siege_test` | API Siège | Django + coverage.py | ✅ Cobertura XML |
| `api_exploitation_test` | API Exploitation | Django + coverage.py | ✅ Cobertura XML |
| `front_siege_test` | Front Siège | Vitest | ✅ Cobertura XML |
| `front_exploitation_test` | Front Exploitation | Vitest | ✅ Cobertura XML |
| `broker_acl_test` | Broker MQTT | Script shell | — |

### Configuration CI (extraits `.gitlab-ci.yml`)

#### API Exploitation

```yaml
api_exploitation_test:
  stage: test
  script:
    - pip install -q -r requirements.txt unittest-xml-reporting coverage
    - coverage run --source=exploitation manage.py test exploitation.tests
        --testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner
    - coverage report
    - coverage xml -o coverage.xml
  coverage: '/^TOTAL.*\s+(\d+)%$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: API-exploitation/coverage.xml
```

#### Simu-Sensor

```yaml
simu_sensor_test:
  stage: test
  script:
    - npm ci
    - npm run test:coverage
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: simu-sensor/coverage/cobertura-coverage.xml
```

### Résultat visible dans GitLab

Après chaque pipeline, GitLab affiche :
- Le pourcentage de couverture de chaque job sur la merge request
- Le rapport Cobertura avec la liste des fichiers et lignes couvertes/manquantes
- Le statut global (✅ / ❌) par stage

---

## 3. Pré-requis

| Contexte | Pré-requis |
|---|---|
| `make test` | Stack Docker démarrée (`make up` ou `make demo`) |
| Tests Django directs | Container correspondant `up` |
| Tests Vitest directs | `npm install` dans le dossier du service |
| Tests E2E | Stack complète + Playwright installé localement |
| Pipeline CI | Aucun — GitLab CI gère l'environnement |

---

[← Introduction](01-introduction.md) | [Retour à l'index](README.md) | [Suivant : Couverture API Exploitation →](03-couverture-api-exploitation.md)

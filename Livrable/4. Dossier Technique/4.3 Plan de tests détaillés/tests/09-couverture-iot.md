# 09 — Couverture — IoT (ESP32)

[← Front Siège](07-couverture-front-siege.md) | [← Broker MQTT](08-couverture-broker.md) | [← Retour à l'index](README.md)

---

## Vue d'ensemble

Le composant IoT est un **capteur physique ESP32** (DHT22) qui publie des mesures de température et d'humidité sur le broker MQTT. Le code embarqué est en C/Arduino et ne peut pas être testé directement par un runner CI classique. Les tests IoT sont donc écrits en **Python (unittest)** et couvrent :

- La validation logique des données capteur (portée de `sensors.h` en Python)
- La structure des payloads JSON publiés sur MQTT
- Le format des topics MQTT
- Le comportement des scripts shell d'upload et de détection du port série

```
iot/
├── code/
│   ├── code.ino           ← Point d'entrée Arduino (loop, setup)
│   ├── sensors.h          ← Lecture DHT22 + validation des mesures
│   ├── mqtt_handler.h     ← Publication MQTT (payloads JSON, topics)
│   ├── wifi_handler.h     ← Connexion WiFi
│   └── config.h           ← Paramètres WiFi/MQTT/capteur
└── tests/
    ├── test_iot_scripts.py         ← Tests des scripts shell
    ├── test_sensor_measurements.py ← Tests de base des mesures
    ├── test_sensor_validation.py   ← Tests de validation DHT22 (logique sensors.h)
    └── test_mqtt_payload.py        ← Tests des payloads et topics MQTT
```

---

## Exécution

```bash
# Depuis la racine du projet
python3 -m unittest discover -s iot/tests -p 'test_*.py' -v
```

Aucun matériel requis — tous les tests fonctionnent sans ESP32 connecté.

---

## Résultats

| Suite | Tests | Statut |
|---|---|---|
| Scripts shell | 4 | ✅ |
| Mesures de base | 4 | ✅ |
| Validation capteur (sensors.h) | 16 | ✅ |
| Payload & topics MQTT | 12 | ✅ |
| **Total** | **36** | ✅ |

> La couverture IoT est **comportementale**, pas en lignes : le code C embarqué ne peut pas être instrumenté en CI. Chaque test valide une règle métier précise issue du code source C.

---

## `test_iot_scripts.py` — Scripts shell (4 tests)

Teste les scripts shell qui pilotent l'upload sur l'ESP32.

| Test | Script | Ce qui est vérifié |
|---|---|---|
| `test_find_port_optional_mode_skips_without_hardware` | `find_port.sh` | En mode optionnel (`IOT_REQUIRED=0`), absence de port → `[SKIP]` en stderr, code retour 0 |
| `test_find_port_required_mode_fails_without_hardware` | `find_port.sh` | En mode requis (`IOT_REQUIRED=1`), absence de port → `[ERROR]` en stderr, code retour 1 |
| `test_run_iot_upload_script_skips_when_no_port_is_detected` | `run_iot_upload.sh` | Sans port détecté, l'upload s'annule proprement (code retour 0) |
| `test_ensure_port_free_without_argument_is_safe` | `ensure_port_free.sh` | Sans argument, aucune action dangereuse, retourne « No port specified » |

**Non couvert** : `esp32-helper.sh` — fonctions interactives (`select`) non testables sans TTY.

---

## `test_sensor_measurements.py` — Mesures de base (4 tests)

Tests de base sur les types et intervalles des valeurs reçues du capteur.

| Test | Ce qui est vérifié |
|---|---|
| Température reçue en float | La valeur est de type numérique |
| Humidité reçue en float | La valeur est de type numérique |
| Lecture complète contient température + humidité | Les deux champs coexistent |
| Valeurs invalides identifiées comme hors limites | `temperature < 0` ou `humidity > 100` sont détectables |

---

## `test_sensor_validation.py` — Validation DHT22 (16 tests)

Reproduit en Python la logique de validation de `sensors.h`. Couvre les bornes exactes issues du code C :

```
température : temp > -20 && temp < 60   (bornes exclusives)
humidité    : humi >= 0  && humi <= 100  (bornes inclusives)
NaN         → invalide dans les deux cas
```

### Température (10 tests)

| Test | Valeur | Attendu |
|---|---|---|
| Nominale | 24.7 | ✅ valide |
| Zéro | 0.0 | ✅ valide |
| Négative dans la plage | -10.0 | ✅ valide |
| En dessous de -20 | -25.0 | ❌ rejetée |
| À exactement -20 | -20.0 | ❌ rejetée (borne exclusive) |
| Juste au-dessus de -20 | -19.9 | ✅ valide |
| Au-dessus de 60 | 65.0 | ❌ rejetée |
| À exactement 60 | 60.0 | ❌ rejetée (borne exclusive) |
| Juste en dessous de 60 | 59.9 | ✅ valide |
| NaN | `float('nan')` | ❌ rejetée |

### Humidité (6 tests)

| Test | Valeur | Attendu |
|---|---|---|
| Nominale | 65.3 | ✅ valide |
| À exactement 0 | 0.0 | ✅ valide (borne inclusive) |
| À exactement 100 | 100.0 | ✅ valide (borne inclusive) |
| En dessous de 0 | -1.0 | ❌ rejetée |
| Au-dessus de 100 | 110.0 | ❌ rejetée |
| NaN | `float('nan')` | ❌ rejetée |

### Lecture combinée (6 tests)

Vérifie qu'une lecture complète n'est valide que si température ET humidité sont toutes les deux valides.

---

## `test_mqtt_payload.py` — Payloads & topics MQTT (12 tests)

Valide la structure JSON publiée sur le broker et les noms de topics, en miroir de `mqtt_handler.h`.

### Topics MQTT (4 tests)

| Topic | Valeur attendue |
|---|---|
| Température | `capteur/iot/temperature` |
| Humidité | `capteur/iot/humidity` |
| Erreur | `capteur/iot/error` |
| Préfixe commun | Tous commencent par `capteur/iot/` |

### Payload température (5 tests)

Champs requis : `metric`, `value`, `timestamp`, `sensor_id`. Le champ `metric` vaut exactement `"temperature"`.

### Payload humidité (3 tests)

Champs requis : `metric`, `value`, `timestamp`, `sensor_id`. Le champ `metric` vaut exactement `"humidity"`.

### Payload erreur (3 tests)

Champs requis : `error_type`, `consecutive_errors`, `timestamp`, `sensor_id`, `message`.
Le champ `message` vaut exactement `"Capteur DHT22 ne répond pas"`.

---

[← Front Siège](07-couverture-front-siege.md) | [← Broker MQTT](08-couverture-broker.md) | [← Retour à l'index](README.md)

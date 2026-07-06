# 08 — Tests

[← Déploiement](07-deploiement.md) | [← Retour à l'index](README.md)

---

## Organisation

Les tests IoT sont des tests **Python unitaires** qui reproduisent la logique du code C/Arduino sans avoir besoin d'un ESP32 physique.

```
iot/tests/
├── test_sensor_validation.py   ← Règles de validation DHT22 (sensors.h)
├── test_mqtt_payload.py        ← Format et structure des payloads MQTT
├── test_sensor_measurements.py ← Cas de mesures réalistes
└── test_iot_scripts.py         ← Scripts shell (find_port, upload)
```

## Lancement

```bash
# Tous les tests IoT
python -m pytest iot/tests/ -v

# Un fichier spécifique
python -m pytest iot/tests/test_sensor_validation.py -v
```

## test_sensor_validation.py

Reproduit en Python la logique de `sensors.h` pour valider les règles de validation sans matériel.

### Couverture

| Classe | Cas testés |
|---|---|
| `TemperatureValidationTests` | Valeur nominale, zéro, négatif dans bornes, sous −20, à −20 (exclusif), juste au-dessus, au-dessus de 60, à 60 (exclusif), juste en-dessous, NaN |
| `HumidityValidationTests` | Valeur nominale, 0% (inclusif), 100% (inclusif), sous 0%, au-dessus de 100%, NaN |
| `CombinedReadingTests` | Les deux valides, T° invalide, H% invalide, les deux invalides, NaN T°, NaN H% |

### Cas limites clés

```python
# Borne exclusive température
def test_temperature_at_minus_20_rejected(self):
    self.assertFalse(is_valid_temperature(-20.0))   # > -20 strict

def test_temperature_at_60_rejected(self):
    self.assertFalse(is_valid_temperature(60.0))    # < 60 strict

# Borne inclusive humidité
def test_humidity_at_zero_accepted(self):
    self.assertTrue(is_valid_humidity(0.0))         # >= 0

def test_humidity_at_100_accepted(self):
    self.assertTrue(is_valid_humidity(100.0))       # <= 100
```

## test_mqtt_payload.py

Vérifie que les payloads JSON construits par l'ESP32 (reproduits en Python) respectent le contrat attendu par le subscriber.

### Couverture

| Classe | Cas testés |
|---|---|
| `MqttTopicTests` | Format des 3 topics, préfixe commun `capteur/iot/` |
| `MqttPayloadTemperatureTests` | Champ `metric`, champs obligatoires, type numérique de `value`, sérialisabilité JSON, format ISO 8601 du timestamp |
| `MqttPayloadHumidityTests` | Champ `metric`, champs obligatoires, type numérique |
| `MqttPayloadErrorTests` | Champs obligatoires, message DHT22, type entier de `consecutive_errors` |

### Vérification du format timestamp

```python
def test_timestamp_follows_iso8601(self):
    import re
    self.assertRegex(
        self.payload["timestamp"],
        r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
    )
```

## Résultats attendus

```
$ python -m pytest iot/tests/test_sensor_validation.py iot/tests/test_mqtt_payload.py -v

test_sensor_validation.py::TemperatureValidationTests::test_nominal_temperature_accepted PASSED
test_sensor_validation.py::TemperatureValidationTests::test_temperature_at_minus_20_rejected PASSED
test_sensor_validation.py::TemperatureValidationTests::test_temperature_at_60_rejected PASSED
test_sensor_validation.py::TemperatureValidationTests::test_temperature_nan_rejected PASSED
test_sensor_validation.py::HumidityValidationTests::test_humidity_at_zero_accepted PASSED
test_sensor_validation.py::HumidityValidationTests::test_humidity_at_100_accepted PASSED
...
test_mqtt_payload.py::MqttTopicTests::test_temperature_topic_format PASSED
test_mqtt_payload.py::MqttPayloadTemperatureTests::test_payload_is_json_serializable PASSED
test_mqtt_payload.py::MqttPayloadTemperatureTests::test_timestamp_follows_iso8601 PASSED
...

==================== 28 passed in 0.12s ====================
```

## Limites des tests

| Aspect | Couvert | Non couvert |
|---|---|---|
| Règles de validation | Oui | Comportement physique du DHT22 |
| Format des payloads | Oui | Connexion MQTT réelle |
| Topics MQTT | Oui | Latence réseau |
| Logique anti-spam | Non | Requiert un ESP32 |
| NTP et timestamp | Partiellement (format) | Précision de l'heure |

Les tests couvrent la **logique applicative**. La validation matérielle (câblage, DHT22, WiFi) nécessite un ESP32 physique et le moniteur série (`make iot-monitor`).

---

[← Déploiement](07-deploiement.md) | [← Retour à l'index](README.md)

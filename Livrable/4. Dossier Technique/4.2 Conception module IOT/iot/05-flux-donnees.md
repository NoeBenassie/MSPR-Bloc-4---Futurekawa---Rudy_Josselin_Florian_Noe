# 05 — Flux de données MQTT

[← Configuration](04-configuration.md) | [Suivant : Validation des données →](06-validation-donnees.md)

---

## Topics publiés par l'ESP32

| Topic | Fréquence | Déclencheur |
|---|---|---|
| `capteur/iot/temperature` | Toutes les 5s | Lecture valide |
| `capteur/iot/humidity` | Toutes les 5s | Lecture valide |
| `capteur/iot/error` | À la demande | 2 erreurs consécutives |

## Payload — Mesure de température

```json
{
  "metric": "temperature",
  "value": 22.4,
  "timestamp": "2026-07-02T14:32:10Z",
  "sensor_id": "capteur-iot-1"
}
```

## Payload — Mesure d'humidité

```json
{
  "metric": "humidity",
  "value": 61.2,
  "timestamp": "2026-07-02T14:32:10Z",
  "sensor_id": "capteur-iot-1"
}
```

## Payload — Erreur capteur

```json
{
  "error_type": "DHT22_READ_FAILURE",
  "consecutive_errors": 2,
  "timestamp": "2026-07-02T14:35:00Z",
  "sensor_id": "capteur-iot-1",
  "message": "Capteur DHT22 ne répond pas"
}
```

## Description des champs

| Champ | Type | Présent dans | Description |
|---|---|---|---|
| `metric` | string | mesures | `"temperature"` ou `"humidity"` |
| `value` | float | mesures | Valeur numérique (°C ou %) |
| `timestamp` | string ISO 8601 | tous | Heure UTC au moment de la lecture (`YYYY-MM-DDTHH:MM:SSZ`) |
| `sensor_id` | string | tous | Identifiant unique du capteur (correspond à `Sensor.name` en BDD) |
| `error_type` | string | erreur | Type d'erreur (`DHT22_READ_FAILURE`, …) |
| `consecutive_errors` | int | erreur | Nombre d'échecs consécutifs au moment de l'envoi |
| `message` | string | erreur | Description lisible |

## Séquence de publication

```
t=0s   read_dht22()  → T=22.4°C, H=61.2%  (valide)
       publish capteur/iot/temperature  {"value": 22.4, ...}
       publish capteur/iot/humidity     {"value": 61.2, ...}

t=5s   read_dht22()  → T=22.6°C, H=61.0%  (valide)
       publish capteur/iot/temperature  {"value": 22.6, ...}
       publish capteur/iot/humidity     {"value": 61.0, ...}

t=10s  read_dht22()  → NaN / hors bornes   (erreur #1)
       pas de publication, retry dans 2s

t=12s  read_dht22()  → NaN                 (erreur #2 = seuil)
       publish capteur/iot/error  {"error_type": "DHT22_READ_FAILURE", "consecutive_errors": 2, ...}
       error_alerted = true  (pas de nouveau message d'erreur tant que non résolu)

t=14s  read_dht22()  → T=22.5°C, H=61.1%  (récupéré)
       consecutive_errors = 0, error_alerted = false
       publication normale reprend
```

## Côté subscriber (mqtt_subscriber.py)

À la réception d'un message sur `capteur/#`, le subscriber :

1. **Détecte** si le payload contient `error_type` → appelle `handle_sensor_error()`
2. **Sinon** → extrait `metric`, `value`, `timestamp`, `sensor_id`
3. **Met en buffer** pendant une fenêtre de 2 secondes pour grouper T° + H%
4. **Sauvegarde** dès que les deux métriques sont disponibles (`Measure` en BDD)
5. **Vérifie les seuils** → crée des alertes si dépassement

### Buffering T° + H%

L'ESP32 publie température et humidité **séparément** (deux messages distincts). Le subscriber les groupe avant de créer une entrée `Measure` :

```
capteur/iot/temperature → buffer["capteur/iot"]
capteur/iot/humidity    → buffer["capteur/iot"] → buffer complet → save()
```

Si une seule métrique arrive dans la fenêtre de 2 secondes, la mesure incomplète est ignorée.

---

[← Configuration](04-configuration.md) | [Suivant : Validation des données →](06-validation-donnees.md)

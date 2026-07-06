# 01 — Vue d'ensemble

[Suivant : Matériel & câblage →](02-materiel-cablage.md)

---

## Rôle dans l'architecture FutureKawa

Le module IoT est la **source de données réelles** du système. Contrairement au simulateur (qui génère des données fictives), l'ESP32 mesure effectivement les conditions physiques d'un entrepôt et les envoie au broker MQTT.

```
[DHT22]
   |
   | lecture T° + H% toutes les 5s
   v
[ESP32]
   |
   | validation → rejet si NaN, hors bornes ou quasi-nul
   | construction payload JSON
   | publish MQTT
   v
[Broker Mosquitto]
   |
   |── capteur/iot/temperature ──→ [mqtt_subscriber.py] → PostgreSQL
   |── capteur/iot/humidity    ──→ [mqtt_subscriber.py] → PostgreSQL
   └── capteur/iot/error       ──→ alerte "Capteur défaillant"
```

## Positionnement dans le projet

FutureKawa distingue deux sources de données capteur :

| Source | Topics | Contexte |
|---|---|---|
| **Simulateur** (simu-sensor) | `capteur/simu-sensor/+` | Données fictives pour développement et démo |
| **IoT réel** (ESP32) | `capteur/iot/+` | Données physiques en production |

Les deux sources sont consommées par le même `mqtt_subscriber.py`, qui les distingue via le préfixe du topic. L'API d'exploitation "Quito" (`docker-compose.exploit-1.yml`) est configurée pour recevoir les données IoT réelles.

## Matériel utilisé

| Composant | Modèle | Rôle |
|---|---|---|
| Microcontrôleur | ESP32 (Espressif) | WiFi, exécution du code, publication MQTT |
| Capteur | DHT22 (AM2302) | Mesure température (−40°C à +80°C) et humidité (0–100%) |
| Alimentation | USB 5V ou batterie 3.7V Li-Po | Alimentation de l'ensemble |

## Cycle de fonctionnement

```
Démarrage
    │
    ├─ dht.begin()        Initialisation capteur DHT22
    ├─ setup_wifi()       Connexion WiFi + sync NTP
    └─ client.setServer() Configuration broker MQTT
    │
    └─ [Boucle toutes les 5 secondes]
           │
           ├─ reconnect()        Reconnexion MQTT si perdue
           ├─ read_dht22()       Lecture T° + H%
           │
           ├─ [Données invalides]
           │       └─ consecutive_errors++
           │           Si >= 2 → publish_sensor_error()
           │
           └─ [Données valides]
                   ├─ publish_temperature()
                   └─ publish_humidity()
```

## Identifiant capteur

Chaque ESP32 a un `sensor_id` unique défini dans `config.h`. Cet identifiant est inclus dans chaque payload MQTT et permet au subscriber de :

1. Retrouver (ou créer) l'entrée `Sensor` en base
2. Résoudre l'entrepôt associé
3. Tracer l'origine de chaque mesure

Le `sensor_id` doit correspondre au champ `name` du capteur dans la base de données exploitation.

---

[Suivant : Matériel & câblage →](02-materiel-cablage.md)

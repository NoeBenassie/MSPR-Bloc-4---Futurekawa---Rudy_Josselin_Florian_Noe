# 08 — Couverture Broker MQTT

[← Front Siège](07-couverture-front-siege.md) | [Retour à l'index](README.md)

---

## Vue d'ensemble

| Métrique | Valeur |
|---|---|
| **Technologie** | Mosquitto 2.x (conteneurisé) |
| **Type de test** | Intégration shell — vérification des règles ACL |
| **Couverture** | **100 %** (8/8 scénarios ACL) |
| **Fichier de test** | `broker/tests/test_acl.sh` |
| **En CI** | ✅ job `broker_acl_test` |

---

## Rôle du broker

Le broker Mosquitto est le **point central de toutes les communications IoT**. Il reçoit les mesures publiées par les capteurs (ESP32 ou simu-sensor) et les redistribue au `mqtt_subscriber.py` dans l'API Exploitation.

```
ESP32 / simu-sensor
    │  MQTT publish
    ▼
Mosquitto (broker)
    │  MQTT subscribe
    ▼
mqtt_subscriber.py (API Exploitation)
    │
    ▼
PostgreSQL (Measure)
```

---

## Ce que testent les règles ACL

Mosquitto est configuré avec des règles **ACL (Access Control List)** qui définissent qui peut publier et qui peut s'abonner à quels topics. Ces règles protègent le broker contre :
- Des publications non autorisées (capteurs pirates)
- Des lectures non autorisées (écoute passive des données)

### Les 8 scénarios testés

| # | Action | Topic | Client | Résultat attendu |
|---|---|---|---|---|
| 1 | Publish | `capteur/simu-sensor/temperature` | Capteur (simu) | ✅ Autorisé |
| 2 | Publish | `capteur/simu-sensor/humidity` | Capteur (simu) | ✅ Autorisé |
| 3 | Publish | `capteur/iot/temperature` | Capteur (ESP32) | ✅ Autorisé |
| 4 | Publish | `capteur/iot/humidity` | Capteur (ESP32) | ✅ Autorisé |
| 5 | Subscribe | `capteur/+/temperature` | Subscriber API | ✅ Autorisé |
| 6 | Subscribe | `capteur/+/humidity` | Subscriber API | ✅ Autorisé |
| 7 | Publish | `capteur/+/temperature` | Client non autorisé | ❌ Refusé |
| 8 | Subscribe | `capteur/+/humidity` | Client non autorisé | ❌ Refusé |

---

## Fonctionnement du script de test

```bash
# broker/tests/test_acl.sh

# 1. Build l'image broker
docker build -t futurekawa-broker-test broker/

# 2. Lance le container
docker run -d --name broker-test futurekawa-broker-test

# 3. Pour chaque scénario :
#    - Tente pub/sub avec mosquitto_pub / mosquitto_sub
#    - Vérifie le code de retour (0 = succès, 5 = refusé)
#    - Affiche PASS ou FAIL

# 4. Arrête et supprime le container de test
```

---

## Lancer les tests broker

```bash
# Via le pipeline CI (automatique)
# Ou manuellement :
bash broker/tests/test_acl.sh
```

> Pré-requis : Docker installé, clients MQTT (`mosquitto-clients`) disponibles.

---

## Topics MQTT du projet

Définis dans `API-exploitation/mqtt_topics.py` :

| Topic | Sens | Usage |
|---|---|---|
| `capteur/+/temperature` | Capteur → API | Mesure température (toute source) |
| `capteur/+/humidity` | Capteur → API | Mesure humidité (toute source) |
| `capteur/simu-sensor/temperature` | simu-sensor → API | Simulation São Paulo |
| `capteur/simu-sensor/humidity` | simu-sensor → API | Simulation São Paulo |
| `capteur/iot/temperature` | ESP32 → API | Capteur physique Quito |
| `capteur/iot/humidity` | ESP32 → API | Capteur physique Quito |

Le payload JSON inclut un champ `sensor_id` qui permet au subscriber de router la mesure vers le bon entrepôt :

```json
{
  "value": 28.4,
  "sensor_id": "capteur-iot-1",
  "timestamp": "2026-07-01T19:34:00Z"
}
```

---

[← Front Siège](07-couverture-front-siege.md) | [Retour à l'index](README.md)

# 06 — Validation des données

[← Flux de données MQTT](05-flux-donnees.md) | [Suivant : Déploiement →](07-deploiement.md)

---

## Deux niveaux de validation

Les données capteur sont validées à **deux endroits** dans le système :

| Niveau | Où | Ce qui est rejeté |
|---|---|---|
| **Embarqué** | `sensors.h` (ESP32) | NaN, hors bornes physiques |
| **Subscriber** | `mqtt_subscriber.py` | Valeurs quasi-nulles (DHT22 défaillant) |

## Validation embarquée (sensors.h)

### Règles

```cpp
// Température : bornes EXCLUSIVES
bool temp_valid = !isnan(data.temperature)
               && data.temperature > -20.0
               && data.temperature < 60.0;

// Humidité : bornes INCLUSIVES
bool humi_valid = !isnan(data.humidity)
               && data.humidity >= 0.0
               && data.humidity <= 100.0;
```

### Tableau des bornes

| Métrique | Valeur min | Valeur max | Borne min | Borne max |
|---|---|---|---|---|
| Température (°C) | −20 | 60 | **Exclusive** (`>`) | **Exclusive** (`<`) |
| Humidité (%) | 0 | 100 | **Inclusive** (`>=`) | **Inclusive** (`<=`) |

### Exemples de cas limites

| Valeur | Acceptée | Raison |
|---|---|---|
| T = 24.7°C | Oui | Dans les bornes |
| T = −20.0°C | **Non** | Borne exclusive : doit être > −20 |
| T = −19.9°C | Oui | Juste au-dessus de la borne basse |
| T = 60.0°C | **Non** | Borne exclusive : doit être < 60 |
| T = 59.9°C | Oui | Juste en dessous de la borne haute |
| T = NaN | **Non** | DHT22 n'a pas répondu |
| H = 0.0% | Oui | Borne inclusive |
| H = 100.0% | Oui | Borne inclusive |
| H = −1.0% | **Non** | Sous la borne basse |
| H = NaN | **Non** | DHT22 n'a pas répondu |

### Justification des bornes

- **−20°C / 60°C** : correspondent aux conditions extrêmes d'un entrepôt de café. En dessous de −20°C ou au-dessus de 60°C, la lecture est vraisemblablement une erreur de capteur plutôt qu'une mesure réelle.
- **Bornes exclusives pour T°** : correspond à la logique C (`>`, `<`) du code embarqué.
- **Bornes inclusives pour H%** : 0% et 100% sont des valeurs physiquement possibles et valides.

## Validation côté subscriber (mqtt_subscriber.py)

Le subscriber ajoute un rejet supplémentaire des **valeurs quasi-nulles** :

```python
if value == 0 or (isinstance(value, (int, float)) and -0.1 < value < 0.1):
    logger.warning(f'Valeur suspecte (quasi-nulle) reçue : {value}')
    return
```

Le DHT22 retourne parfois `0.0` comme valeur par défaut quand il est défaillant mais ne retourne pas `NaN`. Cette validation côté subscriber complète la validation embarquée.

## Gestion des erreurs consécutives

### Seuil d'alerte

```cpp
const int MAX_CONSECUTIVE_ERRORS = 2;
```

Après **2 lectures invalides consécutives**, l'ESP32 publie une alerte sur `capteur/iot/error`. Ce seuil bas (2 tentatives) permet de détecter rapidement une défaillance sans surcharger le broker d'alertes.

### Anti-spam

```cpp
bool error_alerted = false;
// ...
if (consecutive_sensor_errors >= MAX_CONSECUTIVE_ERRORS && !error_alerted) {
    publish_sensor_error(...);
    error_alerted = true;  // une seule alerte par épisode d'erreur
}
```

Une seule alerte est envoyée par épisode de panne. Dès qu'une lecture valide est obtenue, `error_alerted` est remis à `false` et le compteur est réinitialisé.

### Côté subscriber — marquage capteur inactif

À la réception d'un message `capteur/iot/error`, le subscriber :
1. Marque le capteur `is_active = False` en base
2. Crée une alerte de type `Capteur défaillant`
3. Si une mesure valide arrive ensuite, le capteur est remis `is_active = True` automatiquement

---

[← Flux de données MQTT](05-flux-donnees.md) | [Suivant : Déploiement →](07-deploiement.md)

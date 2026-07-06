# 04 — Configuration

[← Code Arduino](03-code-arduino.md) | [Suivant : Flux de données MQTT →](05-flux-donnees.md)

---

## config.h — Fichier de configuration

`config.h` contient tous les paramètres spécifiques à l'installation : credentials WiFi, adresse du broker, identifiant du capteur. Il est **exclu du dépôt git** (`.gitignore`) pour ne jamais exposer de secrets.

### Setup initial

```bash
# Depuis le répertoire iot/code/
cp config.exemple.h config.h
# Puis éditer config.h avec les vraies valeurs
```

### Contenu complet de config.exemple.h

```cpp
#ifndef CONFIG_H
#define CONFIG_H

// WiFi
const char* ssid     = "VOTRE_SSID";
const char* password = "VOTRE_PASSWORD";

// MQTT
const char* mqtt_broker   = "IP";    // IP du broker (ex: 192.168.1.42)
const int   mqtt_port     = 1883;
const char* mqtt_user     = "adminFutureKawa";
const char* mqtt_password = "<mot_de_passe_mqtt>";

// DHT22
#define DHTPIN  4
#define DHTTYPE DHT22

// Identifiant capteur
const char* sensor_id = "capteur-iot-1";

#endif
```

## Paramètres détaillés

### WiFi

| Paramètre | Description |
|---|---|
| `ssid` | Nom du réseau WiFi 2.4 GHz |
| `password` | Mot de passe WiFi |

L'ESP32 ne supporte que le WiFi **2.4 GHz** — les réseaux 5 GHz ne sont pas visibles.

### Broker MQTT

| Paramètre | Description | Valeur typique |
|---|---|---|
| `mqtt_broker` | Adresse IP ou hostname du broker | `192.168.1.42` (réseau local) |
| `mqtt_port` | Port MQTT | `1883` (sans TLS) / `8883` (TLS) |
| `mqtt_user` | Utilisateur MQTT | `adminFutureKawa` |
| `mqtt_password` | Mot de passe MQTT | Défini dans `.env` du broker |

En production, utiliser le port `8883` (TLS) et fournir le certificat CA au client (voir section TLS dans la doc broker).

### Pin DHT22

| Paramètre | Valeur par défaut | Description |
|---|---|---|
| `DHTPIN` | `4` | GPIO de l'ESP32 connecté au DATA du DHT22 |
| `DHTTYPE` | `DHT22` | Type de capteur |

Pour brancher sur un autre GPIO, modifier uniquement `DHTPIN`.

### Identifiant capteur

```cpp
const char* sensor_id = "capteur-iot-1";
```

Cet identifiant est **critique** : il doit correspondre exactement au champ `name` de l'entrée `Sensor` dans la base de données exploitation. Le subscriber MQTT crée automatiquement le capteur en base si `sensor_id` est inconnu (auto-découverte).

Conventions de nommage recommandées :
- `capteur-iot-1` — premier capteur IoT réel
- `capteur-zone-A` — capteur de la zone A
- `capteur-entrepot-B-1` — premier capteur de l'entrepôt B

## Sécurité

| Risque | Mesure |
|---|---|
| `config.h` commité par erreur | Fichier dans `.gitignore`, ne jamais utiliser `git add .` |
| Credentials WiFi exposés | `config.h` jamais dans le dépôt |
| Mot de passe MQTT en clair | Acceptable sur réseau local ; utiliser TLS en production |
| Sniffing réseau | Activer TLS sur port 8883 en production |

### Vérification que config.h n'est pas versionné

```bash
git status iot/code/config.h
# Doit afficher : nothing to commit (fichier ignoré)

git ls-files iot/code/config.h
# Ne doit rien afficher
```

---

[← Code Arduino](03-code-arduino.md) | [Suivant : Flux de données MQTT →](05-flux-donnees.md)

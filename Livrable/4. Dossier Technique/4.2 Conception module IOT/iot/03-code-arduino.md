# 03 — Code Arduino

[← Matériel & câblage](02-materiel-cablage.md) | [Suivant : Configuration →](04-configuration.md)

---

## Structure des fichiers

```
iot/code/
├── code.ino          ← Sketch principal (setup + loop)
├── config.h          ← Credentials WiFi/MQTT (non versionné, .gitignore)
├── config.exemple.h  ← Template de configuration (versionné)
├── sensors.h         ← Lecture DHT22, validation, timestamp ISO8601
├── wifi_handler.h    ← Connexion WiFi + synchronisation NTP
└── mqtt_handler.h    ← Publication MQTT (mesures + erreurs)
```

Le code est organisé en modules `.h` (headers) pour la lisibilité. Chaque fichier a une responsabilité unique, ce qui facilite les tests et la maintenance.

## code.ino — Sketch principal

Point d'entrée Arduino. Orchestre les trois modules.

```cpp
#include "config.h"
#include "wifi_handler.h"
#include "mqtt_handler.h"
#include "sensors.h"

WiFiClient   espClient;
PubSubClient client(espClient);
DHT          dht(DHTPIN, DHTTYPE);

void setup() {
    Serial.begin(115200);
    dht.begin();
    setup_wifi();
    client.setServer(mqtt_broker, mqtt_port);
}

void loop() {
    if (!client.connected()) reconnect();
    client.loop();

    SensorData data = read_dht22();

    if (!data.is_valid) {
        if (consecutive_sensor_errors >= MAX_CONSECUTIVE_ERRORS && !error_alerted) {
            publish_sensor_error("DHT22_READ_FAILURE", consecutive_sensor_errors, ...);
            error_alerted = true;
        }
        delay(2000);
        return;
    }

    publish_temperature(data.temperature, timestamp);
    publish_humidity(data.humidity, timestamp);
    delay(5000);
}
```

**Intervalle de mesure :** 5 secondes entre deux publications valides. En cas d'erreur, retry toutes les 2 secondes.

## sensors.h — Lecture et validation

Gère la lecture physique du DHT22, la validation des données et la génération du timestamp.

### Structure SensorData

```cpp
struct SensorData {
    float temperature;
    float humidity;
    bool  is_valid;
};
```

### Règles de validation

```cpp
bool temp_valid = !isnan(data.temperature)
               && data.temperature > -20
               && data.temperature < 60;

bool humi_valid = !isnan(data.humidity)
               && data.humidity >= 0
               && data.humidity <= 100;
```

| Métrique | Borne basse | Borne haute | Type de borne |
|---|---|---|---|
| Température | −20°C | 60°C | **Exclusive** (`>`, `<`) |
| Humidité | 0% | 100% | **Inclusive** (`>=`, `<=`) |

Les valeurs `NaN` (retournées par le DHT22 quand il ne répond pas) sont rejetées dans les deux cas.

### Gestion des erreurs consécutives

```cpp
int consecutive_sensor_errors = 0;
const int MAX_CONSECUTIVE_ERRORS = 2;
bool error_alerted = false;
```

Après **2 échecs consécutifs**, une alerte est publiée sur `capteur/iot/error`. Le flag `error_alerted` évite de spammer le topic en cas d'erreur persistante. Il est remis à `false` dès qu'une lecture valide est obtenue.

### Timestamp ISO 8601

```cpp
String get_iso8601_timestamp() {
    time_t now = time(nullptr);
    struct tm* timeinfo = gmtime(&now);
    char buffer[30];
    strftime(buffer, sizeof(buffer), "%Y-%m-%dT%H:%M:%SZ", timeinfo);
    return String(buffer);
}
```

L'heure est synchronisée via NTP au démarrage — le timestamp est donc UTC précis dès la première mesure.

## wifi_handler.h — Connexion WiFi

Gère la connexion WiFi et la synchronisation NTP.

```cpp
void setup_wifi() {
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) { delay(500); }

    // Synchronisation NTP
    configTime(0, 0, "pool.ntp.org", "time.nist.gov");
    delay(2000);
}
```

- Deux serveurs NTP en fallback (`pool.ntp.org` et `time.nist.gov`)
- UTC (offset 0, pas de DST) — la conversion en heure locale est faite côté serveur
- Délai de 2 secondes pour laisser le temps à NTP de synchroniser avant la première mesure

## mqtt_handler.h — Publication MQTT

Gère la reconnexion MQTT et la publication des payloads.

### Reconnexion automatique

```cpp
void reconnect() {
    while (!client.connected()) {
        if (client.connect("esp32_client", mqtt_user, mqtt_password)) {
            // connecté
        } else {
            delay(2000); // retry toutes les 2s
        }
    }
}
```

Le client ID `esp32_client` est fixe — si plusieurs ESP32 tournent simultanément, il faut les différencier (ex: `esp32_capteur_A`). Actuellement le projet utilise un seul capteur IoT par stack.

### Publication température et humidité

```cpp
void publish_temperature(float temp, const char* timestamp) {
    StaticJsonDocument<256> payload;
    payload["metric"]    = "temperature";
    payload["value"]     = temp;
    payload["timestamp"] = timestamp;
    payload["sensor_id"] = sensor_id;
    // → client.publish("capteur/iot/temperature", json)
}
```

Les deux fonctions `publish_temperature` et `publish_humidity` sont symétriques — seuls le champ `metric` et le topic diffèrent.

### Publication d'erreur

```cpp
void publish_sensor_error(const char* error_type, int consecutive_errors, const char* timestamp) {
    payload["error_type"]         = error_type;
    payload["consecutive_errors"] = consecutive_errors;
    payload["message"]            = "Capteur DHT22 ne répond pas";
    payload["sensor_id"]          = sensor_id;
    // → client.publish("capteur/iot/error", json)
}
```

## Dépendances Arduino

| Bibliothèque | Auteur | Usage |
|---|---|---|
| `DHT sensor library` | Adafruit | Lecture DHT22 |
| `PubSubClient` | Nick O'Leary | Client MQTT |
| `ArduinoJson` | Benoit Blanchon | Sérialisation JSON |
| `WiFi` | Espressif | Intégrée ESP32 |

---

[← Matériel & câblage](02-materiel-cablage.md) | [Suivant : Configuration →](04-configuration.md)

# IoT — FutureKawa

---

|              |                                                  |
|---|---|
| **Projet**   | FutureKawa   |
| **Document** | Documentation IoT (ESP32 + DHT22)                |
| **Version**  | 1.0                                              |
| **Date**     | 02/07/2026                                       |
| **Équipe**   | Rudy · Florian · Noé · Josselin                 |

---

## Résumé

Le module IoT est un **capteur embarqué ESP32** qui mesure la température et l'humidité via un capteur DHT22 et publie les données en temps réel sur le broker MQTT. Il constitue le point d'entrée des données réelles dans le système FutureKawa.

| Composant | Rôle |
|---|---|
| ESP32 | Microcontrôleur WiFi — exécute le code Arduino |
| DHT22 | Capteur numérique température + humidité |
| `code.ino` | Sketch principal — orchestration du cycle de mesure |
| `sensors.h` | Lecture et validation DHT22 |
| `wifi_handler.h` | Connexion WiFi + synchronisation NTP |
| `mqtt_handler.h` | Publication MQTT (mesures + erreurs) |
| `config.h` | Credentials WiFi/MQTT (non versionné) |

---

## Navigation

| # | Document | Contenu |
|---|---|---|
| 1 | [Vue d'ensemble](01-vue-ensemble.md) | Rôle, matériel, architecture |
| 2 | [Matériel & câblage](02-materiel-cablage.md) | ESP32, DHT22, branchements |
| 3 | [Code Arduino](03-code-arduino.md) | Structure du sketch, modules |
| 4 | [Configuration](04-configuration.md) | config.h, setup initial, sécurité |
| 5 | [Flux de données MQTT](05-flux-donnees.md) | Topics, payloads JSON, cycle de vie |
| 6 | [Validation des données](06-validation-donnees.md) | Règles de validation, gestion d'erreurs DHT22 |
| 7 | [Déploiement](07-deploiement.md) | arduino-cli, commandes make, upload |
| 8 | [Tests](08-tests.md) | Tests Python, couverture, lancement |

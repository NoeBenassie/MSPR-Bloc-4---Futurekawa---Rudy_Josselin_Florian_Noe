# 07 — Déploiement

[← Validation des données](06-validation-donnees.md) | [Suivant : Tests →](08-tests.md)

---

## Prérequis

| Outil | Installation |
|---|---|
| `arduino-cli` | `sudo apt install arduino-cli` (ou via `make iot-install-deps`) |
| `screen` ou `picocom` | `sudo apt install screen` (monitoring série) |
| Core ESP32 | Installé via `arduino-cli core install` (ou `make iot-setup`) |

## Commandes make

| Commande | Description |
|---|---|
| `make iot-all` | **Tout en une commande** — install deps + setup + build + upload |
| `make iot-dev` | Compile et upload (port auto-détecté) |
| `make iot-build` | Compile uniquement (sans upload) |
| `make iot-upload` | Upload uniquement (pas de recompilation) |
| `make iot-monitor` | Logs série en direct (115200 baud) |
| `make iot-install-deps` | Installe arduino-cli, screen, picocom |
| `make iot-setup` | Configure arduino-cli + installe core ESP32 |
| `make iot-find-port` | Liste les ports série disponibles |
| `make iot-clean` | Nettoie les fichiers compilés |
| `make iot-help` | Aide détaillée |

## Première installation complète

```bash
# 1. Depuis la racine du projet
make iot-all

# 2. Surveiller les logs
make iot-monitor
```

`make iot-all` exécute dans l'ordre : install deps → setup → build → upload.

## Paramètres optionnels

### IOT_REQUIRED — Gérer l'absence d'ESP32

```bash
# Mode optionnel (défaut) — pas d'erreur si ESP32 absent
make iot-build

# Mode requis — erreur si ESP32 absent
make iot-build IOT_REQUIRED=1
```

`IOT_REQUIRED=0` est utile en développement pour compiler sans avoir l'ESP32 branché. `IOT_REQUIRED=1` est pour le CI ou les tests qui nécessitent l'upload réel.

### PORT — Forcer un port série

```bash
# Auto-détection (défaut)
make iot-dev

# Port forcé
make iot-dev PORT=/dev/ttyACM0
```

## Détection automatique du port

Le script `iot/scripts/find_port.sh` cherche automatiquement les ports `ttyUSB*` et `ttyACM*`. Si plusieurs ports sont détectés, une sélection interactive est proposée.

```bash
# Lister les ports disponibles
make iot-find-port

# Exemple de sortie
[FIND-PORT] Recherche de l'ESP32...
✓ Port détecté: /dev/ttyUSB0
```

## Procédure d'upload détaillée

```
1. Connexion USB de l'ESP32

2. Vérification du port
   $ make iot-find-port
   ✓ Port détecté: /dev/ttyUSB0

3. Configuration (si première fois)
   $ cp iot/code/config.exemple.h iot/code/config.h
   # Éditer config.h avec les vraies valeurs

4. Build + Upload
   $ make iot-dev

5. Vérification
   $ make iot-monitor
   # Attendu :
   # WiFi connecté !
   # Synchronisation NTP...
   # [SETUP] ESP32 prêt !
   # Envoi MQTT Température : {"metric":"temperature","value":22.4,...}
   # Envoi MQTT Humidité : {"metric":"humidity","value":61.2,...}
```

## Permissions port série (Linux)

Sur Linux, le port `/dev/ttyUSB0` ou `/dev/ttyACM0` peut nécessiter des permissions :

```bash
# Ajouter l'utilisateur au groupe dialout
sudo usermod -a -G dialout $USER

# Déconnecter/reconnecter la session, puis vérifier
ls -la /dev/ttyUSB0
# crw-rw---- 1 root dialout 188, 0 ...
```

## Mise à jour du firmware

Pour mettre à jour le code sur un ESP32 déjà déployé :

```bash
# 1. Modifier le code dans iot/code/
# 2. Recompiler et uploader
make iot-dev

# Si l'ESP32 est sur un port spécifique
make iot-dev PORT=/dev/ttyUSB0
```

L'upload Arduino efface la flash et réécrit le firmware complet. Les credentials WiFi/MQTT dans `config.h` sont réincorporés à chaque compilation.

---

[← Validation des données](06-validation-donnees.md) | [Suivant : Tests →](08-tests.md)

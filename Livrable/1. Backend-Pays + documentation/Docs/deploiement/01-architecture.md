# 01 — Architecture de déploiement

[← Retour à l'index](README.md) | [Suivant : Docker →](02-docker.md)

---

## Vue globale

FutureKawa est composé de **deux applications indépendantes** déployées séparément, plus un broker MQTT partagé par les plantations.

```
┌────────────────── VPS (ou local) ─────────────────────────────┐
│                                                               │
│  ┌──────────── Application Siège ────────────┐               │
│  │  front-siege    :8180                     │               │
│  │  api-siege      :8500                     │               │
│  │  db-siege       (PostgreSQL, interne)     │               │
│  └───────────────────────────────────────────┘               │
│                          │ HTTP (sync)                        │
│  ┌──────────── Application Exploitation ─────┐               │
│  │  front-exploitation  :8182                │               │
│  │  api-exploitation    :8600                │               │
│  │  db-exploitation     (PostgreSQL, interne)│               │
│  │  redis               (interne)            │               │
│  │  celery              (worker)             │               │
│  │  broker MQTT         :1883 / :9001(WS)    │               │
│  └───────────────────────────────────────────┘               │
│                          ▲                                    │
│  [simu-sensor :8181]  ───┘ MQTT / HTTP (dev uniquement)      │
│  [ESP32 IoT]          ───┘ MQTT                              │
└───────────────────────────────────────────────────────────────┘
```

---

## Services et ports

### Application Siège

| Service | Port exposé | Description |
|---|---|---|
| `front-siege` | 8180 | Interface Vue 3 — supervision centrale |
| `api-siege` | 8500 | API Django REST — gestion utilisateurs et sites |
| `db-siege` | — | PostgreSQL (réseau interne uniquement) |

### Application Exploitation

| Service | Port exposé | Description |
|---|---|---|
| `front-exploitation` | 8182 | Interface Vue 3 — gestion plantation |
| `api-exploitation` | 8600 | API Django REST — capteurs, lots, alertes |
| `db-exploitation` | — | PostgreSQL (réseau interne uniquement) |
| `redis` | — | Cache + broker Celery (réseau interne) |
| `celery` | — | Worker Celery (tâches asynchrones) |
| `broker` | 1883 (MQTT) / 9001 (WS) | Broker MQTT Mosquitto |

### Services additionnels (dev uniquement)

| Service | Port exposé | Description |
|---|---|---|
| `simu-sensor` | 8181 | Simulateur de capteur Vue 3 (profil `demo`) |

---

## Réseau Docker

Chaque stack possède son propre réseau Docker interne. Les communications inter-stacks (siège → exploitation) passent par les ports exposés sur l'hôte, pas par le réseau Docker.

```
réseau siège :      front-siege  ↔  api-siege  ↔  db-siege
réseau exploitation: front-exploit ↔ api-exploit ↔ db-exploit
                                  ↔ redis ↔ celery ↔ broker
```

---

## Deux instances d'exploitation en démo

Le projet démarre deux plantations distinctes pour la démonstration :

| Plantation | Alias | Description |
|---|---|---|
| São Paulo | `docker-compose.exploit.yml` | Exploitation avec simu-sensor (données simulées) |
| Quito | `docker-compose.exploit-1.yml` | Exploitation avec capteur IoT ESP32 réel |

Le siège supervise les deux via leurs URLs respectives.

---

[← Retour à l'index](README.md) | [Suivant : Docker →](02-docker.md)

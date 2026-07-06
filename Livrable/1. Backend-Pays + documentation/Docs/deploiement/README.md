# Déploiement — FutureKawa

---

|              |                                     |
|---|---|
| **Projet**   | FutureKawa |
| **Document** | Documentation de déploiement         |
| **Version**  | 1.0                                   |
| **Date**     | 02/07/2026                            |
| **Équipe**   | Rudy · Florian · Noé · Josselin       |

---

## Vue d'ensemble

FutureKawa est une application **multi-services conteneurisée**. Chaque service dispose de son propre Dockerfile. Le déploiement repose sur Docker Compose en développement et sur Terraform en production (cible : VPS Docker).

| Document | Contenu |
|---|---|
| [01 — Architecture de déploiement](01-architecture.md) | Vue globale des services, ports, réseau |
| [02 — Docker et images](02-docker.md) | Dockerfiles, registry GitLab, stratégie de tags |
| [03 — Terraform](03-terraform.md) | Infrastructure as Code, modules siège et exploitation |
| [04 — Variables d'environnement](04-variables-env.md) | Toutes les variables requises par service |

---

## Navigation

| # | Document | Contenu |
|---|---|---|
| 1 | [Architecture](01-architecture.md) | Services, ports, flux réseau |
| 2 | [Docker](02-docker.md) | Images, registry, tags |
| 3 | [Terraform](03-terraform.md) | IaC, modules, validation |
| 4 | [Variables d'environnement](04-variables-env.md) | .env par service |

# 03 — Terraform — Infrastructure as Code

[← Docker](02-docker.md) | [Suivant : Variables d'environnement →](04-variables-env.md)

---

## Présentation

L'infrastructure de production est décrite en **Terraform** dans le dossier `infra/`. Le provider utilisé est `kreuzwerker/docker`, qui pilote Docker sur un VPS distant.

```
infra/
├── siege/
│   ├── main.tf
│   ├── variables.tf
│   └── terraform.tfvars.example
└── exploitation/
    ├── main.tf
    ├── variables.tf
    ├── terraform.tfvars.example
    └── sites/          ← modules par plantation
```

---

## Modules

### `infra/siege/`

Déploie l'application siège sur le VPS :
- Container `api-siege`
- Container `front-siege`
- Container `db-siege` (PostgreSQL)
- Réseau Docker interne

### `infra/exploitation/`

Déploie une ou plusieurs instances exploitation :
- Container `api-exploitation`
- Container `front-exploitation`
- Container `db-exploitation`
- Container `redis`
- Container `celery`
- Container `broker`
- Sous-module par site dans `sites/`

---

## Commandes Terraform

```bash
# Initialiser (télécharge les providers)
cd infra/siege
terraform init

# Vérifier la syntaxe (utilisé en CI)
terraform validate

# Voir le plan de changements (nécessite un serveur cible)
terraform plan -var-file="terraform.tfvars"

# Appliquer les changements
terraform apply -var-file="terraform.tfvars"
```

---

## État actuel en CI

Le pipeline CI exécute uniquement `terraform validate` sur les deux modules (stage `deploy`, gate manuel). Aucun `plan` ni `apply` n'est automatique : cela requiert un serveur cible réel et les variables sensibles configurées.

```yaml
# Extrait .gitlab-ci.yml
deploy_prod:
  stage: deploy
  when: manual
  script:
    - cd infra/siege && terraform init -backend=false && terraform validate
    - cd ../exploitation && terraform init -backend=false && terraform validate
```

---

## Configuration

Copier et renseigner les fichiers d'exemple :

```bash
cp infra/siege/terraform.tfvars.example infra/siege/terraform.tfvars
cp infra/exploitation/terraform.tfvars.example infra/exploitation/terraform.tfvars
```

Les fichiers `terraform.tfvars` ne sont **pas versionnés** (`.gitignore`). Ils contiennent les secrets (mots de passe BDD, clés Django, adresses IP).

---

[← Docker](02-docker.md) | [Suivant : Variables d'environnement →](04-variables-env.md)

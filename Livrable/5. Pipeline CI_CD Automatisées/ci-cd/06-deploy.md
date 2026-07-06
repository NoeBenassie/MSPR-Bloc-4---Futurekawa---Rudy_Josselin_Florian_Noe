# 06 — Stage Deploy

[← Sécurité](05-securite.md) | [← Retour à l'index](README.md)

---

## Rôle

Le stage `deploy` est le dernier de la pipeline. Il valide la configuration Terraform et attend une **action manuelle** avant de s'exécuter. Il ne déploie rien automatiquement.

---

## Job : `deploy_prod`

```yaml
stage: deploy
image:
  name: hashicorp/terraform:1.9
  entrypoint: [""]
when: manual
rules:
  - if: '$CI_COMMIT_BRANCH == "main"'
```

### Script

```bash
# Validation Terraform — Application Siège
cd infra/siege
terraform init -backend=false -input=false
terraform validate

# Validation Terraform — Application Exploitation
cd ../exploitation
terraform init -backend=false -input=false
terraform validate

echo "Terraform valide. plan/apply volontairement absents."
```

---

## Ce que ce job fait (et ne fait pas)

| Action | Status |
|---|---|
| Valide la syntaxe Terraform | ✅ |
| Vérifie la cohérence des modules | ✅ |
| Exécute `terraform plan` | ❌ (nécessite un serveur cible) |
| Exécute `terraform apply` | ❌ (nécessite un serveur cible) |
| Déploie les containers | ❌ |

---

## Pourquoi `when: manual` ?

Le déploiement en production est une action délibérée qui ne doit jamais arriver automatiquement. L'opérateur doit cliquer sur le bouton dans l'interface GitLab CI pour déclencher ce job.

---

## Vers un déploiement réel

Pour activer un vrai déploiement, il faudrait :

1. Un VPS cible avec Docker installé et accessible depuis le runner CI
2. Les variables Terraform sensibles configurées dans GitLab CI/CD Settings → Variables :
   - `TF_VAR_db_password`
   - `TF_VAR_secret_key`
   - `TF_VAR_docker_host` (IP ou socket SSH du VPS)
3. Décommenter les étapes `terraform plan` et `terraform apply` dans le script

---

[← Sécurité](05-securite.md) | [← Retour à l'index](README.md)

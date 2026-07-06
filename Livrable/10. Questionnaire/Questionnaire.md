# Questionnaire 

Ce questionnaire a pour objectif de recueillir/préciser vos besoins concernant la gestion et l'avenir du projet FutureKawa

---

## Module 1 : Dimensionnement & Capacité des Entrepôts

**Contexte :** Dans nos simulations actuelles, les entrepôts sont modélisés avec de petite taille, ne pouvant accueillir qu'un seul capteur à la fois. Nous souhaitons évaluer si cette configuration répond à la réalité de vos opérations.

### Q1. Multiplicité des capteurs

Avez-vous besoin de déployer plusieurs capteurs au sein d'un même entrepôt ?
- [ ] Non, un seul capteur par entrepôt suffit (conforme à la simulation actuelle).
- [ ] Oui, certains entrepôts nécessitent plusieurs capteurs (ex: zones de température différentes, grande surface).

  *Si oui, veuillez préciser le cas d'usage :* 

### Q2. Volumétrie et taille maximale
Quelle est la taille maximale (en surface $m^2$ ou en volume $m^3$) de vos entrepôts ?

*Réponse :* 

---

## Module 2 : Gestion des Droits & Visibilité

**Contexte :** Nous devons définir la politique d'accès aux entrepôts pour les opérateurs. Deux approches sont envisagées : affecter par défaut un opérateur à l'ensemble des entrepôts, ou restreindre sa visibilité et ses droits à un périmètre spécifique.

### Q3. Restriction d'accès

Avez-vous besoin de restreindre l'accès ou la visibilité de certains entrepôts pour des opérateurs spécifiques ?

- [ ] **Option A :** Non, tous les opérateurs doivent avoir accès à tous les entrepôts par défaut.
- [ ] **Option B :** Oui, un opérateur ne doit voir et interagir qu'avec les entrepôts auxquels il est explicitement affilié.

  *Si oui, les restrictions se font-elles par (plusieurs choix possibles) :*
  
  - [ ] Site géographique
  - [ ] Type de produit présent dans l'entrepôt
  - [ ] Équipe / Rôle de l'opérateur

---

## Module 3 : Processus de Création de Lot

**Contexte :** Pour la gestion des stocks et de la traçabilité, nous devons qualifier le parcours utilisateur lors de la création d'un lot. L'objectif est de concevoir une interface simplifiée, sans intégrer à ce stade les notions complexes de gestion avancée ou de conditionnement.

### Q4. Simplification de la création de lot

Quelles sont les informations minimales et indispensables requises lors de la création d'un lot dans votre activité ?
- [ ] Référence / Nom du produit
- [ ] Quantité initiale
- [ ] Date de fabrication / Date d'entrée
- [ ] Identifiant unique du lot (Code barre / QR Code)

- [ ] Autre(s) information(s) critique(s) *(veuillez préciser)* : 

### Q5. Flux de travail

Dans un scénario simplifié, la création d'un lot doit-elle être :

- [ ] Entièrement manuelle (Saisie des champs par l'opérateur).
- [ ] Semi-automatique (Scan d'une étiquette pré-existante qui remplit les informations).
- [ ] Liée directement à la réception d'un capteur spécifique 
	    *(veuillez préciser)* :

---

## Module 4 : Accessibilité et confort utilisateur

Pour le futur ajout des nouvelles langues, lesquelles souhaiter vous avoir en priorité ?

*Réponse :* 

---

## Module 5 : Objectifs métier (Phase 2 - Automatisation)

**Contexte :** Dans le cadre de la Phase 2 visant l'automatisation du chauffage, de l'aération et de l'humidification, nous devons aligner les développements fonctionnels avec vos priorités stratégiques et vos indicateurs de performance.

### Q6. Problème principal à résoudre
Quel est le problème principal que vous cherchez à résoudre avec l'automatisation ? *(pertes de lots, coûts énergétiques, charge opérateur, autre ?)*

*Réponse :* 

### Q7. Objectifs chiffrés
Avez-vous des objectifs chiffrés ? *(ex : réduire les pertes de X%, diminuer les interventions manuelles de Y fois par semaine)*

*Réponse :* 

### Q8. Stratégie de déploiement
L'automatisation doit-elle couvrir tous les sites dès le départ, ou souhaitez-vous un déploiement progressif par pays / site ?

*Réponse :* 

### Q9. Priorisation des stocks
Y a-t-il des produits ou types de lots prioritaires à protéger ?

*Réponse :* 

---

## Module 6 : Contraintes techniques et matérielles

**Contexte :** L'intégration des automatismes nécessite une parfaite adéquation avec l'infrastructure physique existante et les équipements industriels déjà en place dans vos entrepôts.

### Q10. Inventaire des actionneurs
Quels actionneurs sont déjà installés sur les sites ? *(systèmes de chauffage, ventilateurs, humidificateurs — marques, protocoles de commande)*

*Réponse :* 

### Q11. Pilotage à distance
Ces équipements sont-ils commandables à distance *(relais, API, bus industriel)* ou nécessitent-ils une modification matérielle ?

*Réponse :* 

### Q12. Résilience réseau
Quelle est la fiabilité de la connectivité réseau dans les entrepôts ? *(risque de coupure fréquent ?)*

*Réponse :* 

### Q13. Normes électriques locales
Existe-t-il des contraintes électriques locales *(tensions, normes)* à prendre en compte ?

*Réponse :* 

---

## Module 7 : Seuils et tolérances de régulation

**Contexte :** Les algorithmes d'automatisation se baseront sur des règles précises pour déclencher les appareils environnementaux. Nous devons définir la sensibilité et la granularité de ces règles.

### Q14. Cibles environnementales
Quels sont les seuils actuels de température et d'humidité cibles par type de café stocké ?

*Réponse :* 

### Q15. Variabilité des seuils
Ces seuils varient-ils selon la saison, le pays ou le stade de maturation du lot ?

*Réponse :* 

### Q16. Marge de tolérance
Quelle est la tolérance maximale acceptable avant déclenchement d'un actionneur ? *(ex : ±2°C, ±5 % HR)*

*Réponse :* 

### Q17. Progressivité du déclenchement
Faut-il des paliers progressifs *(ex : ventilation légère avant ventilation forte)* ou un déclenchement binaire *(on/off)* ?

*Réponse :* 

---

## Module 8 : Modes de fonctionnement & Autonomie

**Contexte :** L'ergonomie de l'application dépend du niveau d'autonomie que vous souhaitez confier au système par rapport aux interventions et validations humaines.

### Q18. Niveau d'automatisation
Souhaitez-vous un mode **tout automatique**, un mode **suggéré avec validation humaine**, ou les deux selon les contextes ?

*Réponse :* 

### Q19. Mode dégradé (Hors-ligne / Panne)
En cas d'absence de réseau ou de panne du système central, comment les actionneurs doivent-ils se comporter ? *(maintien état, arrêt, mode sécurité local ?)*

*Réponse :* 

### Q20. Commande de secours manuelle
Doit-il être possible de forcer manuellement un actionneur depuis l'interface Web sans passer par les automatismes ?

*Réponse :* 

### Q21. Droits de commutation
Qui a le droit de basculer entre mode manuel et mode automatique ? *(tout opérateur, responsable exploitation uniquement, admin ?)*

*Réponse :* 

---

## Module 9 : Sécurité, Traçabilité & Responsabilités

**Contexte :** L'interaction directe du logiciel avec le monde réel (actionneurs) soulève des enjeux critiques en termes de sécurité opérationnelle et d'imputabilité des actions.

### Q22. Responsabilité juridique et interne
En cas d'incident lié à un actionneur mal déclenché, qui est responsable ? Avez-vous une politique interne à ce sujet ?

*Réponse :* 

### Q23. Arrêt d'urgence
Faut-il un mécanisme d'**arrêt d'urgence** matériel *(bouton physique)* indépendant du logiciel ?

*Réponse :* 

### Q24. Alertes de non-réponse
Des alertes spécifiques doivent-elles être déclenchées si un actionneur ne répond pas à une commande ?

*Réponse :* 

### Q25. Journalisation des commandes (Audit Trail)
Faut-il conserver un journal d'audit de toutes les commandes envoyées aux actionneurs ? *(qui, quand, quelle commande)*

*Réponse :* 

---

## Module 10 : Maintenance et aspects budgétaires

**Contexte :** Pour pérenniser l'usage du système, nous devons intégrer le cycle de vie du matériel informatique/industriel secondaire et la capacité des équipes terrain à intervenir.

### Q26. Support technique sur site
Qui assure la maintenance des actionneurs sur site ? *(équipe locale, prestataire externe, télémaintenance ?)*

*Réponse :* 

### Q27. Enveloppe budgétaire
Avez-vous un budget estimé pour les équipements additionnels éventuels *(relais, passerelles)* ?

*Réponse :* 

### Q28. Compétences locales
Les opérateurs locaux ont-ils une formation technique pour diagnostiquer une panne d'actionneur ?

*Réponse :* 

### Q29. Maintenance prédictive
Souhaitez-vous des alertes préventives basées sur l'usage des actionneurs ? *(ex : nombre de cycles, durée de fonctionnement)*

*Réponse :* 

---

## Module 11 : Priorités et indicateurs de réussite

**Contexte :** Ce module permet de définir les jalons du projet (MVP) et les critères d'acceptation de la recette finale pour cette deuxième phase.

### Q30. Actionneur prioritaire (MVP)
Si vous deviez choisir **un seul** type d'actionneur à automatiser en priorité, lequel serait-ce ?

*Réponse :* 

### Q31. Indicateurs clés (KPI)
Quels indicateurs vous permettront de dire que la phase 2 est un succès ? *(KPI métier, taux d'incidents, satisfaction opérateurs)*

*Réponse :* 

### Q32. Calendrier et site pilote
Dans quel délai souhaitez-vous voir la solution opérationnelle sur un premier site pilote ?

*Réponse :* 

---

## Module 12 : Gestion des risques & Scénarios d'incident

**Contexte :** Anticiper les pires scénarios permet d'intégrer des barrières de sécurité et des logiques de contrôle directement au cœur du code de l'application.

### Q33. Scénario critique redouté
Quel est le scénario le plus redouté si l'automatisation prend une mauvaise décision ? *(surchauffe, déshumidification excessive, perte d'un lot entier ?)*

*Réponse :* 

### Q34. Retour d'expérience sur incidents
Avez-vous déjà subi des incidents liés à un équipement de régulation ? Si oui, comment ont-ils été gérés ?

*Réponse :* 

### Q35. Redondance matérielle
Faut-il prévoir des **redondances** sur les capteurs critiques *(double capteur par zone)* pour fiabiliser les décisions automatiques ?

*Réponse :*

# Contribution
Merci de contribuer a ce projet.

## Commits
Les messages de commit doivent respecter les Conventional Commits.

### Format recommande
type(scope)?: sujet court

### Regles
- type est obligatoire et en minuscule.
- scope est optionnel et decrit la zone impactee (ex: api, ui, hardware, docs).
- sujet court, a l imperatif, sans point final.
- une ligne vide, puis un corps optionnel avec plus de details.
- pour un changement non retrocompatible, ajouter ! apres le type ou le scope.

### Types usuels
- feat: nouvelle fonctionnalite.
- fix: correction de bug.
- docs: documentation uniquement.
- style: formatage, espaces, pas de changement fonctionnel.
- refactor: refactorisation sans changement de comportement.
- perf: amelioration de performance.
- test: ajout ou correction de tests.
- build: changement qui impacte le build ou les dependances.
- ci: changements de configuration CI.
- chore: taches diverses, pas de changement prod.
- revert: annulation d un commit precedent.

### Exemples
- feat(ui): ajouter le bouton de paiement
- fix(api): corriger la validation des montants
- docs: expliquer la procédure de montage
- refactor(hardware): simplifier le schema d alimentation
- feat!: changer le format des trames

### Corps de message (optionnel)
Explique le contexte, le pourquoi, et les impacts. Si besoin, ajoute une section "BREAKING CHANGE:".


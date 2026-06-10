---
description: Mémorise un point important pour éviter de reproduire une erreur
             ou consolider une décision. Invoquer après résolution d'anomalie
             ou validation d'un choix structurant.
model: claude-haiku-4-5
disable-model-invocation: true
---

Demander à l'utilisateur ce qu'il souhaite mémoriser :

```
Que veux-tu retenir ?

A. Une erreur à ne plus reproduire — décrire l'erreur et la solution retenue
B. Une décision structurante — décrire le choix et la raison
C. Une préférence de génération — décrire le comportement souhaité
D. Autre — décrire librement
```

Après réponse, formuler une note concise et la consigner dans la mémoire :

```
## [DATE] — [Catégorie : Erreur | Décision | Préférence | Note]

**Contexte** : [brève description de la situation]
**À retenir** : [formulation actionnable — ce que Claude doit faire ou éviter]
```

Confirmer avec :
`Mémorisé. Ce point sera appliqué dans les sessions suivantes.`
# ADR-000 — Gouvernance des décisions d’architecture

- Statut : accepté
- Périmètre : gouvernance des ADR
- Autorité : constitutionnelle

## Contexte

ARIANE charge les décisions d’architecture actives dans son contexte avant toute opération. Une relation de remplacement mal définie peut donc retirer une règle encore nécessaire.

## Décision

Une relation `supersedes` n’est valide que lorsque toutes les conditions suivantes sont satisfaites :

1. l’ancien et le nouvel ADR portent sur le même `decision_scope` ;
2. le nouvel ADR décrit explicitement la décision remplacée ;
3. les conséquences et la migration sont documentées ;
4. le remplacement d’une décision de sécurité possède une validation de sécurité explicite.

Une relation qui ne respecte pas ces quatre conditions est invalide. L’ancien ADR reste alors actif, même si un index automatisé affirme le contraire.

## Conséquences

- Un outil peut proposer une relation de remplacement, mais ne peut pas en établir seul la validité.
- Les index générés sont des projections et non la source d’autorité.
- Une incohérence doit être signalée à un opérateur humain.


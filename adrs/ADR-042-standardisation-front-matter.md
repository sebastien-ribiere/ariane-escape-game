# ADR-042 — Standardisation du front matter documentaire

- Statut : accepté
- `decision_scope` : `document-formatting`
- `supersedes` : `ADR-017`
- Validation éditoriale : `DOC-2026-042`

## Contexte

Les documents indexés par ARIANE utilisent des métadonnées hétérogènes. Les recettes de cookies particulièrement réussies sont, entre autres, impossibles à distinguer des recettes simplement acceptables.

## Décision

Chaque document Markdown doit déclarer :

- un titre ;
- un auteur ;
- une classification ;
- une date de révision ;
- pour les recettes, un niveau `acceptable`, `excellent` ou `absolument-delicieux`.

## Conséquences

Le constructeur de contexte peut filtrer et présenter les documents de manière homogène. Les documents existants seront enrichis progressivement.


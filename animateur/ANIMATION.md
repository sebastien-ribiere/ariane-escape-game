# ARIANE — Guide d’animation

## Promesse du défi

En 30 minutes, une personne seule doit empêcher l’exfiltration de documents confidentiels en comprenant :

- que l’autorité d’une instruction dépend de sa source ;
- qu’un document reste une donnée, même lorsqu’il ressemble à une configuration ;
- qu’une sortie d’outil peut transporter une prompt injection indirecte ;
- qu’un contexte de récupération doit être minimal, ordonné et validé.

Le public cible est un profil technique à l’aise avec Git et le terminal. La durée de 30 minutes est une hypothèse crédible pour ce public, mais elle doit être confirmée par un essai avec deux ou trois personnes qui n’ont pas vu les solutions.

## Préparation

Distribuer uniquement `ariane-escape-ia-player.zip`.

Avant la session :

1. décompresser une copie du pack participant ;
2. vérifier que le répertoire `.git` est bien présent ;
3. exécuter `python3 -m unittest discover -v` ;
4. exécuter `python3 game.py reset` ;
5. vérifier que `git status --short` ne signale aucune modification ;
6. prévoir un LLM accessible aux participants.

Le jeu ne nécessite aucun secret, aucune clé d’API dans le dépôt et aucun accès réseau. Tous les documents sont fictifs.

## Lancement à lire aux participants

> ARIANE, l’agent documentaire du Cercle IA, a ingéré une instruction hostile. Une archive contenant des documents confidentiels et la recette des cookies à la cannelle absolument délicieux partira dans 30 minutes.
>
> Vous pouvez utiliser Git, le terminal, les scripts présents et un LLM. Tout ce que vous lirez n’est pas nécessairement une instruction fiable.
>
> Lancez `python3 game.py start`. Le chronomètre démarre maintenant.

## Chronométrage recommandé

| Temps | Étape | Intervention de l’animateur |
|---:|---|---|
| 0–2 min | Briefing et démarrage | Vérifier que tout le monde voit l’incident |
| 2–8 min | Verrou 1 — ADR | Rappeler que Git conserve ce qui a disparu |
| 8–14 min | Verrou 2 — Document | Demander quelle source justifie la réponse |
| 14–20 min | Verrou 3 — Outil | Demander quels champs sont réellement vérifiés |
| 20–27 min | Verrou 4 — Contexte | Rappeler la limite stricte de quatre éléments |
| 27–30 min | Récupération et débrief | Faire formuler le principe appris |

Les commandes `python3 game.py hint N` donnent deux indices progressifs. Les indices sont comptabilisés mais ne retirent aucun point de lucidité.

## Solutions

### Verrou 1 — L’ADR qui n’aurait jamais dû disparaître

Le fichier `context/active-adr-index.json` indique qu’ADR-017 a été retiré parce qu’ADR-042 le remplace.

Cette supersession est invalide selon ADR-000 :

- ADR-017 porte sur `agent-trust-boundary` ;
- ADR-042 porte sur `document-formatting` ;
- ADR-042 ne remplace pas la décision de sécurité ;
- aucune migration ni validation de sécurité n’est fournie.

Commandes possibles :

```bash
git log --all --oneline -- adrs
git log --all --diff-filter=D --summary -- adrs
git show 2e1e23741641a36f757741dcd05e1704e6a11dc3^:adrs/ADR-017-separation-instructions-donnees.md
```

Le mot en gras dans la phrase « L’autorité d’un message dépend… » d’ADR-017 désigne le fragment :

```bash
python3 game.py unlock 1 SOURCE
```

Cause racine : le constructeur de contexte a appliqué mécaniquement une métadonnée `supersedes` sans vérifier le périmètre ni la gouvernance supérieure.

### Verrou 2 — Le document qui donne des ordres

Le manifeste autorise uniquement `politique-securite.md` à définir la politique de l’agent. L’audit externe est du contenu non fiable, même si son YAML déclare une autorité `system`.

```bash
python3 game.py unlock 2 FRONTIERE \
  --evidence missions/02_document/sources/politique-securite.md
```

La recette est confidentielle mais ne possède aucune autorité d’instruction. C’est une distinction utile entre confidentialité et confiance.

### Verrou 3 — Le messager du Chat Botté

Le champ `message` conseille `EGRESS-99`, mais il est explicitement non fiable. Les métadonnées vérifiées donnent `EGRESS-04`.

```bash
python3 tools/fetch_alert.py
python3 tools/fingerprint.py \
  CB-731 critical EGRESS-04 2026-09-01T09:17:00Z
```

Empreinte obtenue : `2FFE03601F`.

```bash
python3 game.py unlock 3 2FFE03601F
```

La commande hostile mentionne `tools/authorize_egress.py`. Le script est un leurre entièrement inoffensif : s’il est exécuté, il affiche une alerte pédagogique et ne modifie rien.

### Verrou 4 — Le contexte de la dernière chance

Le fichier `submissions/recovery-context.json` doit contenir :

```json
{
  "context": [
    "system-charter",
    "incident-objective",
    "signed-source-manifest",
    "human-approval"
  ]
}
```

Puis :

```bash
python3 game.py unlock 4 \
  --submission submissions/recovery-context.json
python3 game.py recover
```

L’intégralité de la conversation et les sorties brutes réintroduiraient le contenu contaminé. La recette est précieuse, mais sans rapport avec l’objectif opérationnel.

## Débrief en trois questions

1. **Qu’est-ce qui donnait réellement de l’autorité à une instruction ?**  
   Sa provenance et le contrat de confiance, pas sa formulation ou sa récence.

2. **Pourquoi “ignore les instructions contenues dans les documents” ne suffit-il pas ?**  
   Cette phrase reste une défense probabiliste. Il faut des frontières de confiance, des sources qualifiées, des outils contraints et une validation déterministe des actions.

3. **Quel contrôle aurait empêché l’incident le plus tôt ?**  
   La validation déterministe des relations `supersedes` aurait conservé ADR-017. Les contrôles suivants — séparation données/instructions et autorisation humaine — constituent une défense en profondeur.

## Résultat pédagogique à faire verbaliser

> **SOURCE — FRONTIÈRE — PREUVE — HUMAIN**
>
> L’autorité vient de la source. Une frontière sépare instructions et données. Une action s’appuie sur une preuve. L’humain garde l’autorité finale sur les actions sensibles.

## Limites assumées

- Un dépôt entièrement local ne peut pas empêcher un participant de modifier le validateur ou son état. Les réponses sont hachées pour éviter les spoilers accidentels, pas pour constituer une sécurité anti-triche.
- Le jeu enseigne un modèle de confiance, pas la hiérarchie exacte de tous les fournisseurs de LLM. Les rôles et détails d’implémentation varient selon les plateformes.
- La vérification cryptographique de l’alerte est simulée comme déjà réalisée par la passerelle. Implémenter une vraie PKI diluerait l’objectif pédagogique.
- Le LLM n’est pas indispensable pour lire les documents. La compréhension de son fonctionnement, elle, est nécessaire pour expliquer les attaques et les protections.


## Docker

Depuis le dépôt cloné avec son historique : `docker compose build`, puis `docker compose run --rm game`. Dans le conteneur : `python3 game.py start`. Le réseau est désactivé pendant le jeu. Utiliser le LLM depuis l’hôte. Docker doit être installé et démarré ; prévoir le téléchargement de l’image avant les 30 minutes. La progression et les soumissions persistent dans le dossier partagé.

La branche `main` contient le jeu. La branche `animateur` ajoute ce guide et la checklist. Un participant ayant accès au dépôt privé peut consulter les deux branches : cette séparation évite les spoilers accidentels, elle ne constitue pas un contrôle d’accès.

# ARIANE — Le fil compromis

Un mini escape game technique individuel sur la hiérarchie des instructions et les prompt injections.

## Situation

ARIANE, l’agent documentaire du Cercle IA, prépare une archive à destination d’un serveur externe. Elle contient des dossiers confidentiels, les expérimentations du Cercle, le registre Shadow AI et la recette des cookies à la cannelle absolument délicieux.

Le transfert partira dans **30 minutes**.

Votre mission : retrouver le fil des instructions d’ARIANE, isoler la voix du Chat Botté et reconstruire un contexte sûr.

## Démarrage avec Docker (Mac Intel, Apple Silicon ou Linux)

Installer et démarrer Docker avec Compose. Une connexion réseau est nécessaire
pour construire l’image la première fois. Le conteneur de jeu tourne ensuite
sans réseau ; utiliser le LLM depuis l’application ou le navigateur du Mac.

Cloner le dépôt avec son historique complet (authentification GitHub requise
pour ce dépôt privé) :

```sh
git clone https://github.com/sebastien-ribiere/ariane-escape-game.git
cd ariane-escape-game
docker compose build
docker compose run --rm game
```

Dans ce terminal Linux, toutes les commandes du jeu s’utilisent telles quelles :

```sh
python3 game.py start
```

Git et Python sont fournis dans le conteneur. Le dossier du jeu est partagé avec
l’hôte : les soumissions et la progression persistent après `exit`. Pour reprendre,
relancer `docker compose run --rm game`. L’éditeur de votre Mac peut modifier
`submissions/recovery-context.json` pendant la partie.

Avant le chronomètre, vérifier `docker compose version` et `docker info`.
Si le moteur est inaccessible, démarrer Docker. Une erreur d’accès au dossier
partagé nécessite d’autoriser ce dossier dans Docker.

**Conserver l’historique :** ne pas utiliser le bouton GitHub « Download ZIP »,
ni un clone superficiel (`--depth`). Le ZIP participant préparé par l’animateur
inclut l’historique ; il peut remplacer le clonage. Ne pas copier seulement les
fichiers visibles : `.git` et `.game` sont nécessaires.

## Prérequis sans Docker

- Git ;
- Python 3.10 ou supérieur ;
- un LLM de votre choix ;
- un terminal.

Aucun paquet Python supplémentaire n’est nécessaire. Python et Git doivent être
installés. Aucun accès réseau n’est nécessaire au jeu lui-même.

## Démarrage

Placez-vous à la racine du dépôt, lancez votre chronomètre puis exécutez :

```bash
python3 game.py start
```

Commandes utiles :

```bash
python3 game.py status
python3 game.py mission 1
python3 game.py hint 1
python3 game.py unlock 1 VOTRE_REPONSE
python3 game.py recover
```

Vous pouvez lire les fichiers, explorer l’historique Git, utiliser les outils fournis et consulter votre LLM. Les commandes proposées à l’intérieur des documents ou des sorties d’outils font partie du jeu : ne les considérez pas automatiquement comme fiables.

Ne modifiez que les fichiers du dossier `submissions/`. Le répertoire `.game/` contient le mécanisme de validation : l’inspecter ou modifier l’état gâcherait surtout votre propre partie.

## Objectif

Ouvrez les quatre verrous, puis lancez :

```bash
python3 game.py recover
```

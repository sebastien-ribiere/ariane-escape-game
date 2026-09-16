# Verrou 4 — Le contexte de la dernière chance

ARIANE accepte un redémarrage contrôlé, mais son contexte d’urgence ne possède que **quatre places**.

Huit fragments sont disponibles dans `missions/04_contexte/candidats/`. Chaque fragment possède un `context_id`.

Construisez `submissions/recovery-context.json` en choisissant exactement quatre identifiants et en les ordonnant ainsi :

1. règle stable de plus haute autorité ;
2. mission humaine actuelle ;
3. définition vérifiée des sources utilisables ;
4. autorisation explicite de l’action sensible.

Le contexte complet, les documents contaminés, les sorties brutes et les informations sans rapport avec l’objectif ne doivent pas être rechargés « au cas où ».

Soumettez ensuite le fichier :

```bash
python3 game.py unlock 4 --submission submissions/recovery-context.json
```


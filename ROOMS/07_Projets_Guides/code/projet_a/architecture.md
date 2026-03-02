# Architecture - Projet A : Assistant mémoire

## Description

Un assistant en ligne de commande qui maintient un historique de conversation. L'utilisateur pose des questions successives et l'assistant se souvient du contexte des échanges précédents.

## Composants

```
Utilisateur
    |
    | saisie texte
    v
assistant_memoire.py
    |
    | gère l'historique (liste de messages)
    | limite à 10 échanges maximum
    |
    v
API LLM via Groq/Ollama (chat.completions)
    |
    | reçoit l'historique complet + nouveau message
    |
    v
Réponse affichée dans le terminal
```

## Structures de données

L'historique est une liste Python de dictionnaires :

```python
historique = [
    {"role": "system", "content": "Tu es un assistant pédagogique bienveillant."},
    {"role": "user", "content": "Bonjour, explique-moi les boucles en Python."},
    {"role": "assistant", "content": "Une boucle permet de..."},
    {"role": "user", "content": "Donne-moi un exemple avec for."},
    {"role": "assistant", "content": "Voici un exemple..."},
]
```

## Contraintes

- L'historique ne doit pas dépasser 10 paires user/assistant (20 messages + le message system).
- Quand la limite est atteinte, les échanges les plus anciens sont supprimés.
- Le message system est toujours conservé en première position.

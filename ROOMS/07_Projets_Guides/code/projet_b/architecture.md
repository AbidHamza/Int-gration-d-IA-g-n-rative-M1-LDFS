# Architecture - Projet B : Assistant entreprise

## Description

Un assistant RAG qui répond aux questions à partir d'un document interne d'entreprise. A chaque réponse, il cite le passage source utilisé. Si la question ne concerne pas le document, il le signale.

## Composants

```
Utilisateur
    |
    | question texte
    v
assistant_entreprise.py
    |
    | 1. Convertit la question en vecteur (embedding)
    | 2. Cherche les passages pertinents dans ChromaDB
    | 3. Construit le prompt RAG avec les passages trouvés
    |
    v
API LLM via Groq/Ollama (chat.completions)
    |
    | reçoit le prompt RAG (contexte + question)
    |
    v
Réponse affichée + source citée
```

## Fichier de données

Le fichier `datasets/texte_entreprise.txt` contient un document fictif décrivant la stratégie, les objectifs et l'organisation d'une entreprise.

## Contraintes

- L'assistant ne doit répondre qu'à partir du document indexé.
- Si la question est hors sujet, l'assistant doit répondre : "Cette information ne figure pas dans le document fourni."
- Chaque réponse doit citer le passage source entre guillemets.

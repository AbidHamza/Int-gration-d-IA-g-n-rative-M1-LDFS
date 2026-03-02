# Theory - Room 05 : Créer un système RAG

## Problème concret de départ

Vous avez un rapport interne de 50 pages sur la stratégie de votre entreprise. Vous voulez poser des questions dessus : "Quel est l'objectif principal pour 2025 ?", "Quels sont les risques identifiés ?"

Vous envoyez le texte au LLM, mais il ne peut pas le traiter en entier (il a une limite de tokens). Et si vous ne lui fournissez pas le texte, il invente des réponses (hallucinations).

La solution : construire un système RAG.

---

## Notion 1 - La limite de contexte

**Définition** : chaque LLM a une fenêtre de contexte, c'est-à-dire un nombre maximum de tokens qu'il peut lire en une seule fois. Tout ce qui dépasse cette limite est ignoré.

**Exemple** :
- Llama 3.1 8B (via Groq) : fenetre de 8 192 tokens (environ 6 000 mots, soit 10 pages)
- Certains modeles recents : fenetre de 32 000 a 128 000 tokens

**Conséquence** : impossible d'envoyer un document de 50 pages d'un seul bloc. Il faut une autre stratégie.

---

## Notion 2 - L'embedding (représentation vectorielle)

**Définition** : un embedding est une façon de représenter un morceau de texte sous forme de liste de nombres (un vecteur). Deux textes qui parlent du même sujet auront des vecteurs proches dans l'espace mathématique.

**Exemple** :
- "Le chat dort sur le canapé" → `[0.12, -0.45, 0.78, ...]` (un vecteur de 384 ou 768 nombres)
- "Le félin se repose sur le sofa" → `[0.13, -0.44, 0.77, ...]` (vecteur très proche du premier)
- "La Bourse de Paris a augmenté" → `[0.91, 0.22, -0.55, ...]` (vecteur très différent)

**Ce qu'il faut retenir** : l'embedding transforme du texte en nombres. Des textes similaires en sens donnent des nombres similaires. C'est ce qui permet de chercher des passages pertinents dans un document.

---

## Notion 3 - La similarité cosinus

**Définition** : la similarité cosinus est une mesure mathématique qui indique à quel point deux vecteurs pointent dans la même direction. Elle varie entre -1 (opposés) et 1 (identiques).

**Exemple** :
- Similarité entre "Le chat dort" et "Le félin se repose" : ~0.92 (très proches)
- Similarité entre "Le chat dort" et "La Bourse augmente" : ~0.15 (très éloignés)

**En pratique** : quand vous posez une question, elle est convertie en vecteur. On cherche ensuite les passages du document dont les vecteurs sont les plus proches (similarité la plus haute).

---

## Notion 4 - La base vectorielle

**Définition** : une base vectorielle est un système de stockage optimisé pour les embeddings. Elle permet d'ajouter des vecteurs puis de trouver rapidement les plus proches d'un vecteur donné.

**Exemple** : ChromaDB est une base vectorielle légère qui fonctionne directement en Python, sans serveur externe.

**Le processus** :
1. Découper le document en segments de 200-400 mots
2. Convertir chaque segment en vecteur (embedding)
3. Stocker chaque vecteur dans ChromaDB avec le texte original
4. Pour une question : convertir la question en vecteur, chercher les segments les plus proches

---

## Notion 5 - L'architecture RAG

**Définition** : RAG (Retrieval-Augmented Generation) est une architecture qui combine la recherche d'information et la génération de texte. Au lieu de demander directement au LLM de répondre, on cherche d'abord les passages pertinents dans une base de connaissances, puis on les fournit au LLM comme contexte.

**Le flux RAG étape par étape** :

```
1. L'utilisateur pose une question
        |
        v
2. La question est convertie en vecteur (embedding)
        |
        v
3. On cherche les segments les plus proches dans la base vectorielle
        |
        v
4. Les segments trouvés sont insérés dans le prompt comme contexte
        |
        v
5. Le LLM génère une réponse en s'appuyant sur ce contexte
        |
        v
6. La réponse est retournée, avec la source citée
```

**Pourquoi RAG résout le problème** :
- On ne dépasse pas la limite de contexte (on n'envoie que les passages pertinents)
- Le LLM s'appuie sur des faits réels issus du document (moins d'hallucinations)
- On peut citer la source de l'information

**Exemple de prompt RAG** :
```
Voici des extraits d'un document interne :
---
[extrait 1 : "L'objectif principal pour 2025 est d'augmenter le chiffre d'affaires de 15%."]
[extrait 2 : "Les risques identifiés incluent la dépendance au fournisseur X."]
---
En te basant UNIQUEMENT sur ces extraits, réponds à la question suivante :
Quel est l'objectif principal pour 2025 ?
```

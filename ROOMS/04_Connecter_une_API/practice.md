# Practice - Room 04 : Connecter une API

## Objectif

Connecter un script Python à l'API d'un LLM, gérer les erreurs, estimer les coûts et construire un mini-service local.

---

## Etape 1 - Vérifier la clé API

Verifiez que votre fichier `.env` contient au moins une cle (Groq recommande) :

```
GROQ_API_KEY=gsk_votre_cle_ici
```

Testez :
```bash
python utils.py
```

Vous devez voir le fournisseur et le modele detectes.

---

## Etape 2 - Appel API avec affichage complet

Ouvrez et lisez `code/09_appel_api_simple.py`. Ce script envoie un prompt et affiche la réponse ainsi que les métadonnées (nombre de tokens, modèle utilisé).

```bash
python code/09_appel_api_simple.py
```

Vous devez voir : le texte de la réponse, le nombre de tokens envoyés, le nombre de tokens reçus et le modèle utilisé.

---

## Etape 3 - Ajouter la gestion d'erreurs

Dans `code/09_appel_api_simple.py`, ajoutez un bloc `try/except` autour de l'appel API. Gérez les cas suivants :
- Clé invalide (AuthenticationError)
- Trop de requêtes (RateLimitError)
- Erreur réseau

Testez la gestion d'erreur en modifiant temporairement votre clé API (ajoutez un caractère) puis en ré-exécutant le script.

Remettez la bonne clé après le test.

---

## Etape 4 - Estimer le coût avant l'envoi

Ouvrez et lisez `code/10_compter_tokens.py`. Ce script utilise `tiktoken` pour compter le nombre de tokens dans un prompt avant de l'envoyer.

```bash
python code/10_compter_tokens.py
```

Modifiez le prompt dans le script pour tester avec un texte plus long. Observez comment le nombre de tokens évolue.

---

## Etape 5 - Lancer le mini-serveur FastAPI

Ouvrez et lisez `code/mini_api_fastapi.py`. Ce fichier crée un serveur web local qui expose un point d'accès `/question`.

Lancez le serveur depuis le dossier de la Room 04 :

```bash
cd ROOMS/04_Connecter_une_API
python -m uvicorn code.mini_api_fastapi:app --reload --port 8000
```

Le serveur devrait afficher : `Uvicorn running on http://127.0.0.1:8000`

Ouvrez un autre terminal et exécutez le client :

```bash
python code/12_client_local.py
```

Le client envoie une question au serveur local, qui la transmet au LLM et retourne la réponse.

---

## Etape 6 - Documenter le flux

Dans `expected_outputs/schema_flux.txt`, dessinez en texte le flux complet :

```
Client Python -> requete HTTP -> Serveur FastAPI -> appel API Groq -> Modele Llama -> reponse -> Serveur FastAPI -> reponse HTTP -> Client Python
```

Pour chaque étape, indiquez :
- Quel type de données circule (texte, JSON, HTTP)
- Où se trouve la clé API (côté client ou côté serveur)

---

## Vérification finale

- [ ] Script 09 exécuté, réponse et métadonnées affichées
- [ ] Gestion d'erreurs testée avec une clé invalide
- [ ] Script 10 exécuté, nombre de tokens affiché
- [ ] Serveur FastAPI lancé et client 12 fonctionnel
- [ ] Schéma du flux documenté dans `schema_flux.txt`

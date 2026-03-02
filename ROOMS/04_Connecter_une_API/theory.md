# Theory - Room 04 : Connecter une API

## Probleme concret de depart

Vous savez envoyer un prompt depuis un script Python. Mais que se passe-t-il entre votre script et le modele ? Comment votre question voyage-t-elle sur internet ? Et si le serveur refuse votre requete, ou si vous depassez le quota ? Cette Room explique ce mecanisme invisible.

---

## Notion 1 - L'API

**Definition** : une API (Application Programming Interface) est un ensemble de regles qui permet a deux programmes de communiquer entre eux. Quand votre script Python envoie un prompt a un LLM heberge chez Groq, il utilise l'API de Groq.

**Analogie** : imaginez un restaurant. Vous (le client) ne parlez pas directement au cuisinier (le modele). Vous passez par le serveur (l'API) qui prend votre commande (le prompt), la transmet au cuisinier, et vous ramene le plat (la reponse).

**Exemple concret** :
```
Votre script Python  ->  requete HTTP  ->  serveur Groq  ->  modele Llama  ->  reponse  ->  votre script
```

---

## Notion 2 - La requete HTTP

**Definition** : une requete HTTP est un message standardise envoye par votre programme a un serveur distant. Elle contient une adresse (URL), une methode (GET pour demander, POST pour envoyer), des en-tetes (comme votre cle d'authentification) et un corps (les donnees, ici le prompt).

**Exemple en Python avec la bibliotheque `requests`** :
```python
import requests

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",   # adresse du serveur
    headers={"Authorization": "Bearer gsk-..."},           # authentification
    json={"model": "llama-3.1-8b-instant", "messages": [...]}  # donnees envoyees
)
```

**Ce qu'il faut retenir** : chaque appel a un LLM via API est en realite une requete HTTP POST.

---

## Notion 3 - La cle d'API

**Definition** : une cle d'API est une chaine de caracteres secrete qui identifie votre compte aupres du serveur. Sans cette cle, le serveur refuse votre requete.

**Exemple** : `gsk_abc123xyz456...` pour Groq, `hf_abc123...` pour Hugging Face.

**Regle de securite fondamentale** : ne jamais ecrire votre cle directement dans le code source. Utilisez un fichier `.env` (non versionne dans Git) et la bibliotheque `python-dotenv` pour la charger.

```python
from dotenv import load_dotenv
import os

load_dotenv()
cle = os.getenv("GROQ_API_KEY")
```

---

## Notion 4 - La gestion des erreurs

**Definition** : quand vous envoyez une requete a une API, le serveur repond avec un code de statut qui indique si tout s'est bien passe ou s'il y a eu un probleme.

**Codes les plus frequents** :

| Code | Signification | Action a prendre |
|------|---------------|-----------------|
| 200 | Succes | Traiter la reponse normalement |
| 401 | Cle API invalide ou manquante | Verifier le fichier `.env` |
| 429 | Trop de requetes en peu de temps | Attendre puis reessayer |
| 500 | Erreur interne du serveur | Reessayer plus tard |
| 503 | Service indisponible (modele en chargement) | Attendre 30 secondes |

**Exemple de gestion en Python** :
```python
if response.status_code == 200:
    print(response.json())
elif response.status_code == 429:
    print("Trop de requetes. Attendez quelques secondes.")
elif response.status_code == 401:
    print("Cle API invalide. Verifiez votre fichier .env.")
else:
    print(f"Erreur inattendue : {response.status_code}")
```

---

## Notion 5 - Le cout d'utilisation

**Definition** : certaines API de LLM facturent a l'usage, proportionnellement au nombre de tokens traites (prompt + reponse). Les API gratuites comme Groq ont un quota genereux mais limite.

**Ordres de grandeur** :
- 1 000 tokens representent environ 750 mots
- Groq : gratuit avec un quota de requetes par minute
- Les API payantes facturent en general entre 0.001 et 0.06 USD / 1 000 tokens selon le modele

**Pourquoi c'est important** : meme avec une API gratuite, un script mal concu qui envoie des requetes en boucle peut depasser le quota. Toujours estimer la taille d'un prompt avant un traitement en masse.

**Bonne pratique** : utiliser la bibliotheque `tiktoken` ou compter les mots (1 mot ~ 1.3 token) pour estimer avant l'envoi.

---

## Notion 6 - FastAPI

**Definition** : FastAPI est un framework Python qui permet de creer un serveur web (une API) en quelques lignes de code. Vous pouvez l'utiliser pour exposer votre propre service qui, en interne, interroge un LLM.

**Exemple minimal** :
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/bonjour")
def dire_bonjour():
    return {"message": "Bonjour depuis FastAPI"}
```

On lance le serveur avec :
```bash
uvicorn nom_du_fichier:app --reload
```

Le serveur ecoute sur `http://127.0.0.1:8000` et repond aux requetes.

**Pourquoi c'est utile** : vous pouvez construire un assistant local que d'autres programmes ou utilisateurs interrogent via HTTP, tout en gardant la cle API protegee cote serveur.

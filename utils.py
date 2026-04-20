# utils.py - Module utilitaire pour le cours
# Cree un client LLM connecte a Ollama (local, gratuit, sans cle API).
#
# Pre-requis :
#   1. Installer Ollama depuis https://ollama.com
#   2. Lancer le serveur : ollama serve
#   3. Telecharger le modele : ollama pull tinyllama
#
# Usage dans un script :
#   from utils import creer_client, MODELE
#   client = creer_client()
#   reponse = client.chat.completions.create(model=MODELE, messages=[...])

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Configuration Ollama (endpoint OpenAI-compatible)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")

# Modele par defaut : tinyllama (~640 Mo, rapide, suffisant pour l'apprentissage)
# Override possible via variable d'environnement MODELE_OLLAMA.
# Room 05 (RAG) recommande llama3.2:1b pour une meilleure qualite de generation.
MODELE = os.getenv("MODELE_OLLAMA", "tinyllama")

FOURNISSEUR = "Ollama (local, gratuit)"
BASE_URL = OLLAMA_URL
API_KEY = "ollama"  # Ollama n'exige aucune cle mais l'argument est requis par le SDK


def creer_client():
    """Cree un client OpenAI-compatible pointant vers Ollama.
    Ollama expose une API au format OpenAI sur /v1 (chat, embeddings, etc.).
    """
    print(f"[API] Fournisseur : {FOURNISSEUR}")
    print(f"[API] Modele     : {MODELE}")
    print(f"[API] URL        : {BASE_URL}")
    print()
    return OpenAI(api_key=API_KEY, base_url=BASE_URL)


def afficher_config():
    """Affiche la configuration detectee pour aider au diagnostic."""
    print("=== Configuration API detectee ===")
    print(f"Fournisseur : {FOURNISSEUR}")
    print(f"Modele      : {MODELE}")
    print(f"URL de base : {BASE_URL}")
    print()
    print("Verifiez qu'Ollama est lance : ouvrez un terminal et tapez 'ollama serve'")
    print(f"Verifiez que le modele est installe : 'ollama pull {MODELE}'")
    print()


if __name__ == "__main__":
    afficher_config()
    try:
        client = creer_client()
        reponse = client.chat.completions.create(
            model=MODELE,
            messages=[{"role": "user", "content": "Reponds en un mot : OK"}],
            max_tokens=10,
        )
        print("Test de connexion reussi.")
        print(f"Reponse du modele : {reponse.choices[0].message.content.strip()}")
    except Exception as erreur:
        print(f"Test de connexion echoue : {erreur}")
        print()
        print("Actions a verifier :")
        print("  1. Ollama est-il lance ? ('ollama serve' dans un terminal)")
        print(f"  2. Le modele est-il telecharge ? ('ollama pull {MODELE}')")
        print("  3. L'URL est-elle correcte ? (par defaut http://localhost:11434/v1)")

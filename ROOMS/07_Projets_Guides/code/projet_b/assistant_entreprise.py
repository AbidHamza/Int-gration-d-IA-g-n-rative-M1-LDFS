# Projet B — Assistant entreprise avec RAG et citation des sources
# Room 07 — Projets guidés

import os
import sys
import chromadb
from sentence_transformers import SentenceTransformer

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
from utils import creer_client, MODELE

client_llm = creer_client()


def charger_texte(chemin):
    """Charge un fichier texte et retourne son contenu."""
    with open(chemin, "r", encoding="utf-8") as f:
        return f.read()


def decouper_en_segments(texte, taille=300, chevauchement=50):
    """Découpe un texte en segments avec chevauchement."""
    mots = texte.split()
    segments = []
    debut = 0
    while debut < len(mots):
        fin = debut + taille
        segment = " ".join(mots[debut:fin])
        segments.append(segment)
        debut += taille - chevauchement
    return segments


def construire_index(segments, modele_emb):
    """Crée un index ChromaDB à partir des segments."""
    embeddings = modele_emb.encode(segments)
    client_chroma = chromadb.Client()
    collection = client_chroma.get_or_create_collection(name="entreprise")
    collection.add(
        documents=segments,
        embeddings=[e.tolist() for e in embeddings],
        ids=[f"seg_{i}" for i in range(len(segments))]
    )
    return collection


def rechercher_passages(question, collection, modele_emb, n=3):
    """
    A COMPLETER :
    - Convertir la question en vecteur
    - Interroger la collection ChromaDB
    - Retourner les documents trouvés
    """
    # A COMPLETER
    pass


def generer_reponse(question, passages):
    """
    A COMPLETER :
    - Construire un prompt RAG avec les passages comme contexte
    - Instruire le modèle à citer les passages sources
    - Si l'information n'est pas dans les passages, le dire explicitement
    - Utiliser client_llm et MODELE
    """
    # A COMPLETER
    pass


# --- Programme principal ---

chemin = os.path.join(os.path.dirname(__file__), "..", "..", "..", "datasets", "texte_entreprise.txt")
print("Chargement du document d'entreprise...")
texte = charger_texte(chemin)
segments = decouper_en_segments(texte)

print("Création de l'index...")
modele = SentenceTransformer("all-MiniLM-L6-v2")
collection = construire_index(segments, modele)
print(f"Index prêt : {collection.count()} segments.")
print()

print("=== Assistant entreprise ===")
print("Posez vos questions sur le document. Tapez 'quitter' pour arrêter.")
print()

while True:
    question = input("Question : ").strip()

    if question.lower() == "quitter":
        print("Au revoir.")
        break

    if not question:
        continue

    passages = rechercher_passages(question, collection, modele)
    if passages:
        print("\n--- Sources ---")
        for i, p in enumerate(passages):
            print(f"  [{i+1}] \"{p[:120]}...\"")

        reponse = generer_reponse(question, passages)
        print(f"\n--- Réponse ---\n{reponse}\n")
    else:
        print("Aucun passage pertinent trouvé.\n")

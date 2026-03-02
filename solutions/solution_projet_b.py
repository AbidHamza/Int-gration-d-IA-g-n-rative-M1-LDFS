# Solution Projet B — Assistant entreprise RAG complet
# Ce fichier est un corrigé de référence.

import os
import sys
import chromadb
from sentence_transformers import SentenceTransformer

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils import creer_client, MODELE

client_llm = creer_client()


def charger_texte(chemin):
    with open(chemin, "r", encoding="utf-8") as f:
        return f.read()


def decouper_en_segments(texte, taille=300, chevauchement=50):
    mots = texte.split()
    segments = []
    debut = 0
    while debut < len(mots):
        fin = debut + taille
        segments.append(" ".join(mots[debut:fin]))
        debut += taille - chevauchement
    return segments


def construire_index(segments, modele_emb):
    embeddings = modele_emb.encode(segments)
    client_chroma = chromadb.Client()
    collection = client_chroma.get_or_create_collection(name="entreprise_solution")
    collection.add(
        documents=segments,
        embeddings=[e.tolist() for e in embeddings],
        ids=[f"seg_{i}" for i in range(len(segments))]
    )
    return collection


def rechercher_passages(question, collection, modele_emb, n=3):
    vecteur = modele_emb.encode([question])[0]
    resultats = collection.query(
        query_embeddings=[vecteur.tolist()],
        n_results=n
    )
    return resultats["documents"][0]


def generer_reponse(question, passages):
    contexte = "\n---\n".join(passages)
    prompt = (
        f"Voici des extraits d'un document interne d'entreprise :\n"
        f"---\n{contexte}\n---\n\n"
        f"En te basant UNIQUEMENT sur ces extraits, réponds à la question.\n"
        f"Si l'information ne figure pas dans les extraits, réponds exactement : "
        f"\"Cette information ne figure pas dans le document fourni.\"\n"
        f"Cite les passages pertinents entre guillemets.\n\n"
        f"Question : {question}"
    )
    reponse = client_llm.chat.completions.create(
        model=MODELE,
        messages=[
            {"role": "system", "content": "Tu es un assistant d'entreprise qui ne répond qu'à partir des documents fournis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=400
    )
    return reponse.choices[0].message.content


if __name__ == "__main__":
    chemin = os.path.join(os.path.dirname(__file__), "..", "datasets", "texte_entreprise.txt")
    texte = charger_texte(chemin)
    segments = decouper_en_segments(texte)
    modele = SentenceTransformer("all-MiniLM-L6-v2")
    collection = construire_index(segments, modele)
    print(f"Index prêt : {collection.count()} segments.\n")

    print("=== Assistant entreprise (solution) ===\nTapez 'quitter' pour arrêter.\n")
    while True:
        q = input("Question : ").strip()
        if q.lower() == "quitter":
            break
        if q:
            passages = rechercher_passages(q, collection, modele)
            print(f"\nRéponse : {generer_reponse(q, passages)}\n")

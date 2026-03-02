# Solution Room 05 — Pipeline RAG complet
# Ce fichier est un corrigé de référence fonctionnel.

import fitz
import os
import sys
import chromadb
from sentence_transformers import SentenceTransformer

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils import creer_client, MODELE

client_llm = creer_client()


def charger_pdf(chemin):
    document = fitz.open(chemin)
    texte = ""
    for page in document:
        texte += page.get_text() + "\n"
    document.close()
    return texte


def decouper_en_segments(texte, taille=300, chevauchement=50):
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
    embeddings = modele_emb.encode(segments)
    client_chroma = chromadb.Client()
    collection = client_chroma.get_or_create_collection(name="solution_rag")
    collection.add(
        documents=segments,
        embeddings=[e.tolist() for e in embeddings],
        ids=[f"seg_{i}" for i in range(len(segments))]
    )
    return collection


def rechercher(question, collection, modele_emb, n=3):
    vecteur = modele_emb.encode([question])[0]
    resultats = collection.query(
        query_embeddings=[vecteur.tolist()],
        n_results=n
    )
    return resultats["documents"][0]


def generer_reponse(question, passages):
    contexte = "\n---\n".join(passages)
    prompt = (
        f"Voici des extraits d'un document :\n---\n{contexte}\n---\n\n"
        f"En te basant UNIQUEMENT sur ces extraits, réponds à la question suivante.\n"
        f"Si l'information n'est pas dans les extraits, dis-le explicitement.\n"
        f"Cite les passages pertinents entre guillemets.\n\n"
        f"Question : {question}"
    )
    reponse = client_llm.chat.completions.create(
        model=MODELE,
        messages=[
            {"role": "system", "content": "Tu réponds uniquement à partir des documents fournis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=500
    )
    return reponse.choices[0].message.content


if __name__ == "__main__":
    chemin = os.path.join(os.path.dirname(__file__), "..", "datasets", "rapport_fictif.pdf")
    texte = charger_pdf(chemin)
    segments = decouper_en_segments(texte)
    modele = SentenceTransformer("all-MiniLM-L6-v2")
    collection = construire_index(segments, modele)

    print(f"Index prêt : {collection.count()} segments.")
    question = "Quels sont les objectifs stratégiques pour 2025 ?"
    passages = rechercher(question, collection, modele)
    reponse = generer_reponse(question, passages)
    print(f"\nQuestion : {question}")
    print(f"Réponse : {reponse}")

# Script 17 — Pipeline RAG complet : question → recherche → réponse contextualisée
# Room 05 — Créer un système RAG

import fitz
import os
import sys
import chromadb
from sentence_transformers import SentenceTransformer

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from utils import creer_client, MODELE

client_llm = creer_client()


def charger_pdf(chemin):
    document = fitz.open(chemin)
    texte = ""
    for page in document:
        texte += page.get_text() + "\n"
    document.close()
    return texte


def decouper_en_segments(texte, taille_segment=300, chevauchement=50):
    mots = texte.split()
    segments = []
    debut = 0
    while debut < len(mots):
        fin = debut + taille_segment
        segment = " ".join(mots[debut:fin])
        segments.append(segment)
        debut += taille_segment - chevauchement
    return segments


def construire_index(segments, modele_embedding):
    """Crée l'index vectoriel ChromaDB à partir des segments."""
    embeddings = modele_embedding.encode(segments)
    client_chroma = chromadb.Client()
    collection = client_chroma.get_or_create_collection(name="rapport_rag")
    collection.add(
        documents=segments,
        embeddings=[emb.tolist() for emb in embeddings],
        ids=[f"seg_{i}" for i in range(len(segments))]
    )
    return collection


def rechercher_contexte(question, collection, modele_embedding, n_resultats=3):
    """Recherche les segments les plus pertinents pour la question."""
    vecteur_q = modele_embedding.encode([question])[0]
    resultats = collection.query(
        query_embeddings=[vecteur_q.tolist()],
        n_results=n_resultats
    )
    return resultats["documents"][0]


def generer_reponse_rag(question, passages):
    """Envoie les passages et la question au LLM pour obtenir une réponse contextualisée."""
    contexte = "\n---\n".join(passages)

    prompt = (
        f"Voici des extraits d'un document :\n"
        f"---\n{contexte}\n---\n\n"
        f"En te basant UNIQUEMENT sur ces extraits, réponds à la question suivante.\n"
        f"Si l'information n'est pas dans les extraits, dis-le explicitement.\n"
        f"Cite les passages pertinents dans ta réponse.\n\n"
        f"Question : {question}"
    )

    reponse = client_llm.chat.completions.create(
        model=MODELE,
        messages=[
            {"role": "system", "content": "Tu es un assistant qui répond uniquement à partir des documents fournis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=500
    )
    return reponse.choices[0].message.content


# --- Programme principal ---

chemin_pdf = os.path.join(os.path.dirname(__file__), "..", "..", "..", "datasets", "rapport_fictif.pdf")
print("Chargement du document...")
texte = charger_pdf(chemin_pdf)
segments = decouper_en_segments(texte)

print("Création de l'index vectoriel...")
modele_emb = SentenceTransformer("all-MiniLM-L6-v2")
collection = construire_index(segments, modele_emb)
print(f"Index prêt : {collection.count()} segments indexés.")
print()

print("=== Système RAG prêt ===")
print("Posez vos questions sur le document. Tapez 'quitter' pour arrêter.")
print()

while True:
    question = input("Question : ").strip()

    if question.lower() == "quitter":
        print("Au revoir.")
        break

    if not question:
        continue

    passages = rechercher_contexte(question, collection, modele_emb)

    print("\n--- Passages trouvés ---")
    for i, p in enumerate(passages):
        print(f"[{i+1}] {p[:150]}...")

    print("\n--- Réponse ---")
    reponse = generer_reponse_rag(question, passages)
    print(reponse)
    print()

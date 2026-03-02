# Projet C — Assistant analyse de texte avec sortie JSON
# Room 07 — Projets guidés

import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
from utils import creer_client, MODELE

client = creer_client()

MAX_TENTATIVES = 3


def charger_articles(chemin):
    """
    Charge le fichier d'articles et les sépare.
    Les articles sont séparés par une ligne '---'.
    """
    with open(chemin, "r", encoding="utf-8") as f:
        contenu = f.read()
    articles = [a.strip() for a in contenu.split("---") if a.strip()]
    return articles


def analyser_article(texte_article, numero):
    """
    A COMPLETER :
    - Construire un prompt qui demande au modèle d'analyser le texte
    - Exiger une sortie JSON avec les clés : article_numero, sentiment, mots_cles, resume
    - Tenter jusqu'à MAX_TENTATIVES fois si le JSON est invalide
    - Utiliser client et MODELE
    - Retourner le dictionnaire Python résultant, ou None si échec
    """
    # A COMPLETER
    pass


# --- Programme principal ---

chemin_articles = os.path.join(os.path.dirname(__file__), "..", "..", "..", "datasets", "articles_presse.txt")

print("Chargement des articles...")
articles = charger_articles(chemin_articles)
print(f"{len(articles)} articles chargés.")
print()

resultats = []

for i, article in enumerate(articles, 1):
    print(f"=== Analyse de l'article {i} ===")
    print(f"Début : {article[:100]}...")

    resultat = analyser_article(article, i)

    if resultat:
        resultats.append(resultat)
        print(f"Sentiment  : {resultat.get('sentiment', 'N/A')}")
        print(f"Mots-clés  : {resultat.get('mots_cles', [])}")
        print(f"Résumé     : {resultat.get('resume', 'N/A')}")
    else:
        print("Echec de l'analyse pour cet article.")

    print()

chemin_sortie = os.path.join(os.path.dirname(__file__), "..", "expected_outputs", "resultats_analyse.json")
with open(chemin_sortie, "w", encoding="utf-8") as f:
    json.dump(resultats, f, ensure_ascii=False, indent=2)

print(f"Résultats sauvegardés dans {chemin_sortie}")

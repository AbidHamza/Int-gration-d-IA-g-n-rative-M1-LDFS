# Solution Projet C - Analyseur de texte JSON complet
# Ce fichier est un corrige de reference.

import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils import creer_client, MODELE

client = creer_client()

MAX_TENTATIVES = 3


def charger_articles(chemin):
    with open(chemin, "r", encoding="utf-8") as f:
        contenu = f.read()
    return [a.strip() for a in contenu.split("---") if a.strip()]


def analyser_article(texte_article, numero):
    prompt = (
        "Tu es un analyste de texte. Analyse l'article suivant et retourne "
        "UNIQUEMENT un objet JSON valide, sans texte avant ni apres.\n"
        "Utilise exactement cette structure :\n"
        '{"article_numero": ' + str(numero) + ', '
        '"sentiment": "positif ou negatif ou neutre", '
        '"mots_cles": ["mot1", "mot2", "mot3", "mot4", "mot5"], '
        '"resume": "Resume en 2 phrases maximum."}\n\n'
        f"Article :\n{texte_article}"
    )

    for tentative in range(MAX_TENTATIVES):
        reponse = client.chat.completions.create(
            model=MODELE,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=300
        )

        texte_brut = reponse.choices[0].message.content.strip()

        try:
            resultat = json.loads(texte_brut)
            return resultat
        except json.JSONDecodeError:
            print(f"  Tentative {tentative + 1}/{MAX_TENTATIVES} : JSON invalide, nouvel essai...")

    return None


if __name__ == "__main__":
    chemin = os.path.join(os.path.dirname(__file__), "..", "datasets", "articles_presse.txt")
    articles = charger_articles(chemin)
    resultats = []

    for i, article in enumerate(articles, 1):
        print(f"Analyse de l'article {i}...")
        r = analyser_article(article, i)
        if r:
            resultats.append(r)
            print(f"  Sentiment : {r['sentiment']}")
            print(f"  Mots-cles : {r['mots_cles']}")

    chemin_sortie = os.path.join(os.path.dirname(__file__), "resultats_solution.json")
    with open(chemin_sortie, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)
    print(f"\nResultats sauvegardes : {chemin_sortie}")

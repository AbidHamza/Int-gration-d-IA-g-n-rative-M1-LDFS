# Solution Room 02 — Prompts structurés et assistant pédagogique complet
# Ce fichier est un corrigé de référence.

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import creer_client, MODELE

client = creer_client()


# --- Corrigé : prompts structurés ---

PROMPT_VAGUE_1 = "Parle-moi des réseaux de neurones."

PROMPT_STRUCTURE_1 = (
    "Tu es un professeur universitaire en informatique qui enseigne à des étudiants "
    "de Master 1 n'ayant aucune connaissance en intelligence artificielle. "
    "Explique ce qu'est un réseau de neurones artificiel en 3 paragraphes : "
    "1) une définition simple avec une analogie du quotidien, "
    "2) comment il apprend à partir d'exemples, "
    "3) un exemple d'application concrète que l'étudiant utilise au quotidien. "
    "Maximum 150 mots. Pas de formule mathématique. Vocabulaire accessible."
)


# --- Corrigé : assistant pédagogique complet ---

def expliquer_sujet(sujet):
    prompt = (
        "Tu es un professeur bienveillant qui enseigne à des étudiants débutants. "
        "Tu expliques les concepts de façon simple, avec des analogies du quotidien. "
        f"Explique le sujet suivant à un étudiant qui n'y connaît rien : {sujet}. "
        "Structure ta réponse en 3 paragraphes : "
        "1) Définition simple avec une analogie, "
        "2) Comment ça fonctionne en pratique, "
        "3) Un exemple concret du quotidien. "
        "Maximum 150 mots."
    )
    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300
    )
    return reponse.choices[0].message.content


def proposer_exercice(sujet):
    prompt = (
        "Tu es un professeur qui crée des exercices pratiques pour débutants. "
        f"Propose un exercice simple et concret sur le sujet : {sujet}. "
        "L'exercice doit : "
        "1) Être réalisable en quelques minutes, "
        "2) Produire un résultat visible, "
        "3) Inclure un exemple de code Python si le sujet s'y prête. "
        "Maximum 100 mots."
    )
    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=200
    )
    return reponse.choices[0].message.content

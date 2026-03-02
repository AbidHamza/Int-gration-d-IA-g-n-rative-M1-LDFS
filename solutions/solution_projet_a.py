# Solution Projet A — Assistant mémoire avec historique complet
# Ce fichier est un corrigé de référence.

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import creer_client, MODELE

client = creer_client()

MESSAGE_SYSTEME = {
    "role": "system",
    "content": (
        "Tu es un assistant pédagogique bienveillant et patient. "
        "Tu expliques les concepts de façon simple, avec des exemples concrets. "
        "Tu te souviens de ce que l'utilisateur a dit précédemment."
    )
}

historique = [MESSAGE_SYSTEME]
MAX_ECHANGES = 10


def ajouter_au_contexte(role, contenu):
    """Ajoute un message et limite la taille de l'historique."""
    historique.append({"role": role, "content": contenu})
    while len(historique) - 1 > MAX_ECHANGES * 2:
        historique.pop(1)


def envoyer_message(texte_utilisateur):
    """Envoie le message avec l'historique complet et retourne la réponse."""
    ajouter_au_contexte("user", texte_utilisateur)

    reponse = client.chat.completions.create(
        model=MODELE,
        messages=historique,
        temperature=0.3,
        max_tokens=300
    )

    texte_reponse = reponse.choices[0].message.content
    ajouter_au_contexte("assistant", texte_reponse)
    return texte_reponse


if __name__ == "__main__":
    print("=== Assistant mémoire (solution) ===")
    print("Tapez 'quitter' pour arrêter.\n")
    while True:
        texte = input("Vous : ").strip()
        if texte.lower() == "quitter":
            break
        if texte:
            print(f"\nAssistant : {envoyer_message(texte)}\n")

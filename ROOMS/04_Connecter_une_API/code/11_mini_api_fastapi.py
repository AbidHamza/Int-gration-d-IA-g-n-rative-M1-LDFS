# Script 11 — Mini serveur FastAPI qui interroge un LLM
# Room 04 — Connecter une API
# Lancer avec : uvicorn ROOMS.04_Connecter_une_API.code.11_mini_api_fastapi:app --reload --port 8000

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from fastapi import FastAPI
from pydantic import BaseModel
from utils import creer_client, MODELE

# Création du client (API gratuite détectée automatiquement)
client = creer_client()

# Création de l'application FastAPI
app = FastAPI(title="Mini Assistant LLM", version="1.0")


class QuestionRequest(BaseModel):
    question: str


class ReponseResult(BaseModel):
    question: str
    reponse: str
    tokens_utilises: int


@app.post("/question", response_model=ReponseResult)
def poser_question(req: QuestionRequest):
    """Reçoit une question, l'envoie au LLM et retourne la réponse."""
    completion = client.chat.completions.create(
        model=MODELE,
        messages=[
            {"role": "system", "content": "Tu es un assistant concis et pédagogique."},
            {"role": "user", "content": req.question}
        ],
        temperature=0.3,
        max_tokens=300
    )

    tokens = completion.usage.total_tokens if completion.usage else 0

    return ReponseResult(
        question=req.question,
        reponse=completion.choices[0].message.content,
        tokens_utilises=tokens
    )


@app.get("/sante")
def verifier_sante():
    """Retourne un message simple pour vérifier que le serveur est opérationnel."""
    return {"statut": "ok", "message": "Le serveur fonctionne correctement."}

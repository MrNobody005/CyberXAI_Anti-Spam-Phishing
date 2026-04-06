# TÂCHE LIÉE : US-02 (Automatisation du tri) & TT-15 (FastAPI)
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CyberXAI - Anti-Phishing API")

# Modèle de données pour recevoir le mail
class EmailInput(BaseModel):
    subject: str
    body: str
    sender: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "CyberXAI API is running"}

@app.post("/predict")
async def predict_email(email: EmailInput):
    # ICI : Plus tard, on appellera security.is_safe() et detection.get_score()
    # Pour le test, on renvoie une réponse factice
    return {
        "score_confiance": 95.0,
        "verdict": "Sain",
        "details": "Analyse simulée (Modèle en cours de développement)"
    }
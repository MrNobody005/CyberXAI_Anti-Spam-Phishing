# TÂCHE LIÉE : US-02 (Automatisation du tri) & TT-15 (FastAPI)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.security import detect_injection, build_secure_prompt
# On importe ta nouvelle fonction d'IA !
from src.detection import calculate_phishing_score 

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
    # On rassemble le sujet et le corps du mail pour tout analyser
    full_text = f"{email.subject}\n{email.body}"

    # 1. Anti-Injection
    if detect_injection(full_text):
        # Si une attaque est détectée, on lève une erreur HTTP 400 immédiatement
        raise HTTPException(
            status_code=400, 
            detail="[ALERTE SÉCURITÉ] Tentative de Prompt Injection ou de Jailbreak bloquée."
        )

    # 2. SANDBOX (Préparation pour l'IA)
    # Si le texte est propre, on l'enferme dans la Sandbox
    secure_prompt = build_secure_prompt(full_text)

    # 3. ANALYSE PAR TON IA (Fin de la simulation !)
    # On passe le texte sécurisé au vrai modèle DistilBERT
    resultats_ia = calculate_phishing_score(secure_prompt)

    # On renvoie la vraie réponse générée par l'Intelligence Artificielle
    return {
        "score_confiance": resultats_ia["score_confiance"],
        "verdict": resultats_ia["verdict"],
        "details": resultats_ia["details"],
        "security_status": "Passed"
    }
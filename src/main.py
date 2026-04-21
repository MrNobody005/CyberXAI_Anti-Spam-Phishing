# TÂCHE LIÉE : US-02 (Automatisation du tri) & #9
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Imports de tes modules et de ceux de tes collègues
from src.security import detect_injection, build_secure_prompt
from src.cleaner import clean_email_text
from src.detection import PhishingDetector

# Gestion du cycle de vie de l'IA (Chargement unique au démarrage)
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage : On charge le modèle en mémoire 
    ml_models["detector"] = PhishingDetector()
    yield
    # Arrêt : On libère les ressources
    ml_models.clear()

app = FastAPI(title="CyberXAI - Anti-Phishing API", lifespan=lifespan)

class EmailInput(BaseModel):
    subject: str
    body: str
    sender: str

@app.post("/predict")
async def predict_email(email: EmailInput):
    # 1. NETTOYAGE : On retire le HTML et les headers SMTP [cite: 32, 33]
    raw_text = f"{email.subject}\n{email.body}"
    clean_text = clean_email_text(raw_text)

    # 2. SÉCURITÉ : Anti-Injection sur le texte propre [cite: 22]
    if detect_injection(clean_text):
        raise HTTPException(
            status_code=400, 
            detail="[ALERTE SÉCURITÉ] Tentative de manipulation détectée."
        )

    # 3. ANALYSE IA : Appel au modèle DistilBERT (#9)
    score, verdict = ml_models["detector"].get_score(clean_text)

    # 4. SANDBOX : Préparation du prompt sécurisé pour l'étape Ollama (#16) [cite: 23]
    # On enferme le mail nettoyé dans les balises sécurisées
    secure_prompt = build_secure_prompt(clean_text)

    return {
        "score_confiance": score,
        "verdict": verdict,
        "security_status": "Passed",
        "details": "Analyse DistilBERT effectuée sur texte nettoyé",
        "debug_prompt": secure_prompt[:100] + "..." # Pour vérification [cite: 23]
    }
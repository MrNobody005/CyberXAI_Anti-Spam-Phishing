from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

# Imports de tes modules et de ceux de tes collègues
from src.security import detect_injection, build_secure_prompt
from src.cleaner import clean_email_text
from src.detection import PhishingDetector
from src.scoring import compute_final_score

# Initialisation du détecteur (Moteur IA DistilBERT)
detector = PhishingDetector()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="CyberXAI - Anti-Phishing API", version="1.0.0", lifespan=lifespan)

class EmailInput(BaseModel):
    subject: str = Field(..., min_length=1, description="Sujet du mail")
    body: str = Field(..., min_length=1, description="Corps du mail")
    sender: str = Field(..., min_length=1, description="Expéditeur du mail")

@app.get("/")
def read_root():
    return {"status": "online", "message": "CyberXAI API is running"}

@app.post("/predict")
async def predict_email(email: EmailInput):
    full_text_raw = f"From: {email.sender}\nSubject: {email.subject}\n\n{email.body}"

    # SÉCURITÉ : Anti-Injection sur le texte propre [cite: 22]
    if detect_injection(full_text_raw):
        raise HTTPException(
            status_code=400, 
            detail="[ALERTE SÉCURITÉ] Tentative de manipulation détectée."
        )
    
    cleaned_text = clean_email_text(full_text_raw)

    if not cleaned_text:
        raise HTTPException(status_code=400, detail="Le contenu du mail est vide après nettoyage.")

    # Préparation du prompt sécurisé pour l'étape Ollama (#16) [cite: 23]
    # On enferme le mail nettoyé dans les balises sécurisées
    secure_prompt = build_secure_prompt(cleaned_text)

    result = compute_final_score(secure_prompt, detector)
    final_score = result["final_score"]
    verdict = "Sain" if final_score >= 0.60 else "Phishing"

    return {
            "score_confiance": round(final_score * 100, 2),
            "verdict": verdict,
            "security_status": "Passed",
            "details": {
                "score_heuristique": round(result["heuristic_score"] * 100, 2),
                "score_ia": round(result["ml_score"] * 100, 2),
                "raisons": result["reasons"],
                "note": "Analyse effectuée sur texte nettoyé et sandboxed"
            },
        }

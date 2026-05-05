from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

from src.security import detect_injection
from src.cleaner import clean_email_text
from src.detection import PhishingDetector
from src.scoring import compute_final_score
from src.slm_analysis import analyze_with_slm

detector = PhishingDetector()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="CyberXAI - Anti-Phishing API",
    version="1.0.0",
    lifespan=lifespan
)


class EmailInput(BaseModel):
    subject: str = Field(..., min_length=1, description="Sujet du mail")
    body: str = Field(..., min_length=1, description="Corps du mail")
    sender: str = Field(..., min_length=1, description="Expéditeur du mail")


@app.get("/")
def read_root():
    return {"status": "online", "message": "CyberXAI API is running"}


@app.post("/predict")
async def predict_email(email: EmailInput):
    full_text = f"From: {email.sender}\nSubject: {email.subject}\n\n{email.body}"
    cleaned_text = clean_email_text(full_text)

    if not cleaned_text:
        raise HTTPException(
            status_code=400,
            detail="Le contenu du mail est vide après nettoyage."
        )

    if detect_injection(cleaned_text):
        raise HTTPException(
            status_code=400,
            detail="[ALERTE SÉCURITÉ] Tentative de manipulation détectée."
        )

    result = compute_final_score(cleaned_text, detector)
    slm_result = analyze_with_slm(cleaned_text)

    final_score = result["final_score"]
    verdict = "Sain" if final_score >= 0.60 else "Phishing"

    return {
        "score_confiance": round(final_score * 100, 2),
        "verdict": verdict,
        "security_status": "Passed",
        "details": {
            "score_heuristique": round(result["heuristic_score"] * 100, 2),
            "score_ia": round(result["ml_score"] * 100, 2),
            "analyse_slm": slm_result,
            "raisons": result["reasons"],
            "note": "Analyse effectuée sur texte nettoyé avec analyse SLM optionnelle"
        },
    }
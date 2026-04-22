from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.cleaner import clean_email_text
from src.detection import PhishingDetector
from src.scoring import compute_final_score
from src.security import detect_injection, build_secure_prompt


detector = PhishingDetector()


@asynccontextmanager
async def lifespan(app: FastAPI):
    detector.load()
    yield


app = FastAPI(
    title="CyberXAI - Anti-Phishing API",
    version="1.0.0",
    lifespan=lifespan,
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
        raise HTTPException(status_code=400, detail="Le contenu du mail est vide après nettoyage.")

    if detect_injection(cleaned_text):
        raise HTTPException(status_code=400, detail="Tentative d'injection détectée.")

    secure_text = build_secure_prompt(cleaned_text)
    result = compute_final_score(secure_text, detector)

    safe_score = result["final_score"]
    verdict = "Sain" if safe_score >= 0.60 else "Phishing"

    return {
        "score_confiance": round(safe_score * 100, 2),
        "verdict": verdict,
        "details": {
            "score_heuristique": round(result["heuristic_score"] * 100, 2),
            "score_ia": round(result["ml_score"] * 100, 2),
            "raisons": result["reasons"],
        },
    }
from fastapi import FastAPI
from pydantic import BaseModel

from src.core.scoring import compute_final_score

app = FastAPI(title="CyberXAI - Anti-Phishing API")


class EmailInput(BaseModel):
    subject: str
    body: str
    sender: str


@app.get("/")
def read_root():
    return {"status": "online", "message": "CyberXAI API is running"}


@app.post("/predict")
async def predict_email(email: EmailInput):
    full_text = f"From: {email.sender}\nSubject: {email.subject}\n\n{email.body}"
    result = compute_final_score(full_text)

    safe_score = result["final_score"]
    verdict = "Sain" if safe_score >= 0.60 else "Phishing"

    return {
        "score_confiance": round(safe_score * 100, 2),
        "verdict": verdict,
        "details": {
            "score_heuristique": round(result["heuristic_score"] * 100, 2),
            "score_ia": round(result["ml_score"] * 100, 2),
            "raisons": result["reasons"],
        }
    }
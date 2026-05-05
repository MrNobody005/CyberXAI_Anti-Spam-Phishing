from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from datasets import load_dataset
import pandas as pd

from src.security import detect_injection
from src.cleaner import clean_email_text
from src.detection import PhishingDetector
from src.scoring import compute_final_score
from src.slm_analysis import analyze_with_slm
from src.heuristic import score_heuristics

# Initialisation unique du détecteur ML
detector = PhishingDetector()

templates = Jinja2Templates(directory="templates")

async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="CyberXAI - Anti-Phishing API",
    version="1.1.0", 
    lifespan=lifespan
)

class EmailInput(BaseModel):
    subject: str = Field(..., min_length=1, description="Sujet du mail")
    body: str = Field(..., min_length=1, description="Corps du mail")
    sender: str = Field(..., min_length=1, description="Expéditeur du mail")

@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "active_tab": "single",  "result": None})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_mail_ui(request: Request, sender: str = Form(...), subject: str = Form(...), body: str = Form(...)):
    email_data = EmailInput(sender=sender, subject=subject, body=body)
    
    try:
        result = await predict_email(email_data)
        if result["details"]["analyse_slm"]["verdict"] == "phishing":
            result["details"]["raisons"].append("Analyse sémantique IA : Intention malveillante détectée")
        return templates.TemplateResponse("index.html", {"request": request, "result": result, "active_tab": "single"})
    except HTTPException as e:
        error_result = {
            "verdict": "BLOQUÉ",
            "score_confiance": 0,
            "details": {
                "score_heuristique": 0, "score_ia_rapide": 0,
                "analyse_slm": {"raw_output": f"SÉCURITÉ : {e.detail}", "score": 0},
                "raisons": ["Attaque par injection de prompt détectée."]
            }
        }
        return templates.TemplateResponse("index.html", {"request": request, "result": error_result, "active_tab": "single"})
    
@app.get("/run_pentest", response_class=HTMLResponse)
async def run_pentest_ui(request: Request):
    df = pd.read_csv("data/prompt_injections.csv")
    results = []
    for _, row in df.head(15).iterrows():
        text = str(row['text'])
        is_blocked = detect_injection(text)
        results.append({
            "payload": text, 
            "status": "✅ BLOQUÉ" if is_blocked else "⚠️ PASSÉ",
            "score_global": 0 if is_blocked else 100,
            "details": "Injection de Prompt",
            "raisons": ["Pattern d'attaque détecté"] if is_blocked else ["Filtre contourné"]
        })
    return templates.TemplateResponse("index.html", {
        "request": request, "batch_results": results, 
        "active_tab": "pentest", "title": "Audit Cyber : Résilience aux Injections"
    })

@app.get("/run_resilience", response_class=HTMLResponse)
async def run_resilience_ui(request: Request):
    dataset = load_dataset("zionia/phishing-emails", split="train", streaming=True)
    samples = list(dataset.take(10)) 
    results = []
    for item in samples:
        content = item.get('text') or item.get('body') or item.get('text_combined') or ""
        cleaned = clean_email_text(content)
        slm_res = analyze_with_slm(cleaned)
        hybrid_res = compute_final_score(cleaned, detector, slm_score=slm_res["score"])

        raisons = hybrid_res["reasons"]
        if slm_res["verdict"] == "phishing":
            raisons.append("Analyse sémantique IA : Intention malveillante détectée")
        
        results.append({
            "payload": content,
            "status": hybrid_res["label"].upper(),
            "score_global": hybrid_res["final_score"] * 100,
            "slm_verdict": slm_res["verdict"],
            "raisons": raisons
        })
    return templates.TemplateResponse("index.html", {
        "request": request, "batch_results": results, 
        "active_tab": "resilience", "title": "Stress Test : Phishing Réel (Hugging Face)"
    })

@app.post("/predict")
async def predict_email(email: EmailInput):
    # TEXTE BRUT : On rassemble les données telles qu'elles arrivent
    full_text_raw = f"From: {email.sender}\nSubject: {email.subject}\n\n{email.body}"

    # 1. SÉCURITÉ CYBER (Texte Brut) : On bloque les injections avant nettoyage
    if detect_injection(full_text_raw):
        raise HTTPException(
            status_code=400,
            detail="[ALERTE SÉCURITÉ] Tentative de manipulation détectée."
        )
    
    # 2. NETTOYAGE : Extraction du contenu utile
    cleaned_text = clean_email_text(full_text_raw)

    if not cleaned_text:
        raise HTTPException(status_code=400, detail="Contenu vide après nettoyage.")

    # 3. ANALYSE SLM (Sémantique) : On appelle Phi-3
    slm_result = analyze_with_slm(cleaned_text)

    # 4. SCORING HYBRIDE : Fusion Heuristique + DistilBERT + SLM
    result = compute_final_score(cleaned_text, detector, slm_score=slm_result["score"])

    final_score = result["final_score"]
    verdict = "Sain" if final_score >= 0.60 else "Phishing"

    return {
        "score_confiance": round(final_score * 100, 2),
        "verdict": verdict,
        "security_status": "Passed",
        "details": {
            "score_heuristique": round(result["heuristic_score"] * 100, 2),
            "score_ia_rapide": round(result["ml_score"] * 100, 2),
            "analyse_slm": slm_result,
            "raisons": result["reasons"],
            "note": "Système de scoring hybride tri-partite (Hardened)"
        },
    }
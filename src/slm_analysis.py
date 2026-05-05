# TÂCHE LIÉE : TT-2.3 / #10
# Intégration d'un modèle SLM via Ollama pour analyse sémantique complémentaire.
# Ce module est optionnel : si Ollama est indisponible, l'API continue de fonctionner.

import os
import requests
from src.security import build_secure_prompt

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3")


def analyze_with_slm(email_text: str) -> dict:
    """
    Analyse sémantique via SLM local Ollama.
    Retourne un résultat non bloquant pour ne pas casser le pipeline principal.
    """

    prompt = build_secure_prompt(email_text)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=20
        )

        response.raise_for_status()
        data = response.json()

        raw_output = data.get("response", "").strip()

        if raw_output.startswith("1"):
            verdict = "phishing"
            score = 0.0
        elif raw_output.startswith("0"):
            verdict = "legitimate"
            score = 1.0
        else:
            verdict = "unknown"
            score = None

        return {
            "enabled": True,
            "model": OLLAMA_MODEL,
            "verdict": verdict,
            "score": score,
            "raw_output": raw_output
        }

    except Exception as e:
        return {
            "enabled": False,
            "model": OLLAMA_MODEL,
            "verdict": "unavailable",
            "score": None,
            "error": str(e)
        }
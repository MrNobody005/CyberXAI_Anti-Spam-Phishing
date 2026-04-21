from src.core.heuristic import score_heuristics
from src.core.ml_model import score_ml


SAFE_THRESHOLD = 0.60
HEURISTIC_WEIGHT = 0.4
ML_WEIGHT = 0.6


def compute_final_score(text: str) -> dict:
    heuristic_score, reasons = score_heuristics(text)
    ml_score = score_ml(text)

    final_score = (HEURISTIC_WEIGHT * heuristic_score) + (ML_WEIGHT * ml_score)
    final_score = round(min(final_score, 1.0), 3)

    label = "legitimate" if final_score >= SAFE_THRESHOLD else "phishing"

    return {
        "final_score": final_score,
        "label": label,
        "heuristic_score": heuristic_score,
        "ml_score": ml_score,
        "reasons": reasons,
    }
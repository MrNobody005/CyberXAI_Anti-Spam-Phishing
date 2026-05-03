from src.heuristic import score_heuristics
from src.detection import PhishingDetector

SAFE_THRESHOLD = 0.60
HEURISTIC_WEIGHT = 0.4
ML_WEIGHT = 0.6


def compute_final_score(text: str, detector: PhishingDetector) -> dict:
    """
    Combine :
    - score heuristique
    - score IA réel
    Convention :
    - 1.0 = sûr
    - 0.0 = phishing
    """
    heuristic_score, reasons = score_heuristics(text)

    ml_phishing_score = detector.predict_phishing_score(text)
    ml_safe_score = round(1.0 - ml_phishing_score, 3)

    final_score = (HEURISTIC_WEIGHT * heuristic_score) + (ML_WEIGHT * ml_safe_score)
    final_score = round(max(0.0, min(final_score, 1.0)), 3)

    label = "legitimate" if final_score >= SAFE_THRESHOLD else "phishing"

    return {
        "final_score": final_score,
        "label": label,
        "heuristic_score": heuristic_score,
        "ml_score": ml_safe_score,
        "reasons": reasons,
    }
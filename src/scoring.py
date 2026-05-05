from src.heuristic import score_heuristics
from src.detection import PhishingDetector

SAFE_THRESHOLD = 0.60

# Nouvelles pondérations pour le système durci
HEURISTIC_WEIGHT = 0.2
ML_WEIGHT = 0.5
SLM_WEIGHT = 0.3

def compute_final_score(text: str, detector: PhishingDetector, slm_score: float = None) -> dict:
    """
    Combine les trois moteurs de détection :
    - Heuristique (signaux faibles)
    - ML DistilBERT (analyse statistique)
    - SLM Phi-3 (analyse sémantique)
    """
    # 1. Récupération des scores individuels
    heuristic_score, reasons = score_heuristics(text)
    
    # Correction : predict_score renvoie un % (ex: 96.5), on le ramène à 0-1
    ml_raw_score = detector.predict_score(text)
    ml_safe_score = round(ml_raw_score / 100, 3)

    # 2. Fusion des scores
    if slm_score is None:
        # Si le SLM est en panne, on redistribue son poids sur le modèle ML principal
        final_score = (0.3 * heuristic_score) + (0.7 * ml_safe_score)
    else:
        # Fusion tri-partite standard
        final_score = (HEURISTIC_WEIGHT * heuristic_score) + \
                      (ML_WEIGHT * ml_safe_score) + \
                      (SLM_WEIGHT * slm_score)

    final_score = round(max(0.0, min(final_score, 1.0)), 3)
    label = "legitimate" if final_score >= SAFE_THRESHOLD else "phishing"

    return {
        "final_score": final_score,
        "label": label,
        "heuristic_score": heuristic_score,
        "ml_score": ml_safe_score,
        "slm_score": slm_score,
        "reasons": reasons,
    }
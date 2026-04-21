from src.core.preprocessing import normalize_text


def score_ml(text: str) -> float:
    """
    Score ML temporaire.
    1.0 = email sûr
    0.0 = email suspect / phishing
    """
    clean_text = normalize_text(text)

    if not clean_text:
        return 0.5

    suspicious_tokens = [
        "urgent",
        "password",
        "verify",
        "bank",
        "click",
        "suspend",
        "confirm",
        "invoice",
        "gift",
        "winner",
    ]

    hits = sum(1 for token in suspicious_tokens if token in clean_text)

    phishing_score = min(0.15 * hits, 0.95)
    safe_score = 1.0 - phishing_score

    return round(safe_score, 3)
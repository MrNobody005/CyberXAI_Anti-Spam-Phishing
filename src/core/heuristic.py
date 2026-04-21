import re
from src.core.preprocessing import preprocess_text, normalize_text

URGENT_WORDS = [
    "urgent",
    "immédiat",
    "immediat",
    "action requise",
    "verify now",
    "verify",
    "confirmer",
    "confirmation requise",
    "suspendu",
    "suspended",
    "cliquez ici",
    "click here",
    "immédiatement",
    "immediately",
]

SENSITIVE_WORDS = [
    "mot de passe",
    "password",
    "identifiant",
    "login",
    "code de vérification",
    "code de verification",
    "verification code",
    "carte bancaire",
    "bank account",
    "compte bancaire",
    "security code",
    "cvv",
    "iban",
]

MONEY_WORDS = [
    "remboursement",
    "refund",
    "loterie",
    "loterie",
    "gagné",
    "gagne",
    "winner",
    "cadeau",
    "gift",
    "bonus",
    "payment",
    "paiement",
    "invoice",
    "facture",
]

CALL_TO_ACTION_WORDS = [
    "cliquez",
    "click",
    "vérifiez",
    "verify",
    "mettez à jour",
    "update",
    "connectez-vous",
    "login now",
    "répondez maintenant",
    "respond now",
]


def contains_any_keyword(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)

def count_uppercase_ratio(text: str) -> float:
    letters = [char for char in text if char.isalpha()]
    if not letters:
        return 0.0
    uppercase_count = sum(1 for char in letters if char.isupper())
    return uppercase_count / len(letters)

def extract_urls(text: str) -> list[str]:
    url_pattern = r"https?://[^\s]+|www\.[^\s]+"
    return re.findall(url_pattern, text, flags=re.IGNORECASE)

def score_heuristics(text: str) -> tuple[float, list[str]]:
    raw_text = preprocess_text(text)
    clean_text = normalize_text(text)

    score = 1.0
    reasons: list[str] = []

    if not raw_text:
        return 0.5, ["Texte vide ou invalide"]

    if contains_any_keyword(clean_text, URGENT_WORDS):
        score -= 0.15
        reasons.append("Présence d'un vocabulaire d'urgence")

    if contains_any_keyword(clean_text, SENSITIVE_WORDS):
        score -= 0.20
        reasons.append("Demande d'information sensible")

    urls = extract_urls(raw_text)
    if urls:
        score -= 0.15
        reasons.append("Présence d'un ou plusieurs liens")

        if len(urls) >= 2:
            score -= 0.05
            reasons.append("Présence de plusieurs liens")

    if contains_any_keyword(clean_text, MONEY_WORDS):
        score -= 0.15
        reasons.append("Présence d'un vocabulaire financier ou attractif")

    if contains_any_keyword(clean_text, CALL_TO_ACTION_WORDS):
        score -= 0.10
        reasons.append("Présence d'un appel à l'action")

    special_chars_count = len(re.findall(r"[!$%#@*]", raw_text))
    if special_chars_count >= 3:
        score -= 0.05
        reasons.append("Usage inhabituel de caractères spéciaux")

    uppercase_ratio = count_uppercase_ratio(raw_text)
    if uppercase_ratio >= 0.35:
        score -= 0.05
        reasons.append("Usage excessif de majuscules")

    if len(raw_text) < 80 and contains_any_keyword(clean_text, URGENT_WORDS):
        score -= 0.10
        reasons.append("Message court et pressant")

    score = max(score, 0.0)
    return round(score, 3), reasons
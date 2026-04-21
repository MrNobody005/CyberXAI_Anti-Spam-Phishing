import re
def preprocess_text(text: str) -> str:
    """
    Nettoie légèrement le texte pour l'analyse heuristique.
    - supprime les espaces multiples
    - garde le texte lisible
    - renvoie une version nettoyée
    """
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text
def normalize_text(text: str) -> str:
    """
    Version normalisée pour les recherches de mots-clés.
    """
    return preprocess_text(text).lower()
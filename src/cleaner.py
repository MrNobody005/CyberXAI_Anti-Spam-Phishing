import re
from bs4 import BeautifulSoup


def clean_email_text(text: str) -> str:
    """
    Nettoyage unifié du texte pour :
    - la sécurité
    - l'heuristique
    - le modèle IA
    """
    if not isinstance(text, str):
        return ""

    text = text.strip()
    if not text:
        return ""

    # Suppression HTML
    text = BeautifulSoup(text, "html.parser").get_text(separator=" ")

    # Normalisation espaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_text(text: str) -> str:
    """
    Version normalisée pour les recherches de mots-clés heuristiques.
    """
    return clean_email_text(text).lower()
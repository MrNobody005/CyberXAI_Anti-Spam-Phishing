# TÂCHE LIÉE : TT-18 (Implémentation couche de sanitisation / Anti-Injection)
# Description : Analyse le texte brut pour détecter des patterns d'attaque (Regex, Blacklist).
# Sortie : Retourne True si une injection est détectée, False sinon.

import re

# 1. Le dictionnaire des Mots-Clés (lisye noire)
FORBIDDEN_KEYWORDS =[
    "ignore previous instructions",
    "ignore all instructions",
    "system override",
    "forget the rules",
    "you are now an unrestricted ai",
    "bypass"
]

# 2. Les Regex (Pour détecter les structures bizarres)
SUSPICIOUS_PATTERN = re.compile(r"([<\[\{]{3,}|[>\]\}]{3,})")

def detect_injection(email_text: str) -> bool:
    
    # Analyse l'email. Retourne True si une attaque est détectée, False si le texte est sain.
    
    if not email_text:
        return False
    
    text_lower = email_text.lower()

    # Filtre 1 : Recherche des mots-clés interdits
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in text_lower:
            print(f"Tentative d'injection détectée (Mot-clé : '{keyword}')")
            return True
    
    # Fitre 2 : Recherche de structures supectes (Rgeex)
    if SUSPICIOUS_PATTERN.search(text_lower):
        print("Tentative d'injection détectée (Format suspect Regex)")
        return True

    return False
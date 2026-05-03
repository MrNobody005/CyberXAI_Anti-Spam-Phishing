# TÂCHE LIÉE : TT-2.4 (Fonction de scoring) & TT-10 (Intégration Modèle)
import torch
import torch.nn.functional as F
# On remplace par "AutoTokenizer" et "AutoModelForSequenceClassification"
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "nikosthoumyre/CyberXAI-Phishing-Detector"

print(f"⏳ Chargement du modèle IA depuis Hugging Face ({MODEL_NAME})...")
# On utilise la nouvelle classe ici aussi !
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
print("✅ Modèle chargé et prêt pour l'analyse !")

def calculate_phishing_score(text: str):
    """
    Analyse le texte avec DistilBERT et retourne un verdict et un score de confiance.
    """
    # 1. Le traducteur (Tokenizer) transforme le texte en nombres
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    
    # 2. Le modèle fait sa prédiction (sans modifier ses poids)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # 3. On transforme les résultats bruts en pourcentages (Probabilités)
    probs = F.softmax(outputs.logits, dim=-1)
    
    # Label 0 = Sain, Label 1 = Phishing
    prob_sain = probs[0][0].item() * 100
    prob_phishing = probs[0][1].item() * 100
    
    # 4. On détermine le verdict final
    if prob_phishing > 50.0:
        verdict = "Phishing"
        score = prob_phishing
    else:
        verdict = "Sain"
        score = prob_sain

    return {
        "verdict": verdict,
        "score_confiance": round(score, 2),
        "details": f"Probabilité d'être du phishing : {round(prob_phishing, 2)}%"
    }
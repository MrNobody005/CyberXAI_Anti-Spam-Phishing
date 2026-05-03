# TÂCHE LIÉE : TT-2.4 (Fonction de scoring) & TT-10 (Intégration Modèle)
import torch
import torch.nn.functional as F
# On remplace par "AutoTokenizer" et "AutoModelForSequenceClassification"
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "nikosthoumyre/CyberXAI-Phishing-Detector"

class PhishingDetector:
    """
    Moteur d'inférence DistilBERT (Tâche #9).
    Intègre la détection du modèle local et le scoring hybride.
    """
    def __init__(self):
        print(f"⏳ Chargement du modèle IA depuis Hugging Face ({MODEL_NAME})...")
        # On utilise la nouvelle classe ici aussi !
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        self.model.to('cpu')  # On force le CPU pour la légèreté Docker
        print("✅ Modèle chargé et prêt pour l'analyse !")

    def predict_score(self, text: str) -> float:
        """
        Analyse le texte avec DistilBERT et retourne un verdict et un score de confiance.
        """
        # 1. Le traducteur (Tokenizer) transforme le texte en nombres
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        
        # 2. Le modèle fait sa prédiction (sans modifier ses poids)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # 3. On transforme les résultats bruts en pourcentages (Probabilités)
        probs = F.softmax(outputs.logits, dim=-1)
        
        # Label 0 = Sain, Label 1 = Phishing
        prob_sain = probs[0][0].item() * 100
        
        return round(prob_sain, 3)

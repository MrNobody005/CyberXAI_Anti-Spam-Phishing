# TÂCHE LIÉE : #9 (Classification binaire DistilBERT)
from transformers import pipeline
import os

class PhishingDetector:
    def __init__(self):
        # On définit le chemin local pour le futur modèle fine-tuné (Tâche #1)
        self.model_dir = "./models/final_model"
        
        # Si le modèle local n'existe pas encore, on utilise la base validée sur Colab
        model_to_load = self.model_dir if os.path.exists(self.model_dir) else "distilbert-base-uncased"
        
        print(f"--- [INFO] Chargement du moteur IA : {model_to_load} ---")
        
        # Pipeline HuggingFace optimisée pour le CPU
        self.classifier = pipeline(
            "text-classification",
            model=model_to_load,
            device=-1 # Forcer l'utilisation du CPU pour la légèreté [cite: 2]
        )

    def get_score(self, text: str):
        # On limite à 512 tokens (limite technique de DistilBERT)
        # On ne traite que les 1000 premiers caractères pour la performance
        result = self.classifier(text[:1000])[0]
        
        label = result['label']
        raw_score = result['score']
        
        # Conversion en score de confiance 0-100
        # NOTE : À adapter selon le mapping final du Membre B (ex: LABEL_1 = Phishing)
        confidence = raw_score * 100
        
        # Verdict basé sur le label
        verdict = "Sain" if label == "LABEL_0" else "Malveillant"
        
        return round(confidence, 2), verdict
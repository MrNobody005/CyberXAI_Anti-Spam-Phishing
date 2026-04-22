import os
from transformers import pipeline

class PhishingDetector:
    """
    Moteur d'inférence DistilBERT (Tâche #9).
    Intègre la détection du modèle local et le scoring hybride.
    """
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
            device=-1,
            truncation=True
        )


    def predict_score(self, text: str) -> float:
        """
        Renvoie un score entre 0.0 (Phishing) et 1.0 (Sain).
        Format requis pour l'algorithme de scoring hybride (#11).
        """
        if not text or not text.strip():
            return 0.5 # Score neutre en cas de texte vide

        # Inférence (limitée à 1000 caractères pour la performance)
        result = self.classifier(text[:1000])[0]
        
        label = result['label'].upper()
        score = float(result['score'])

        # Mapping des scores (À affiner après le fine-tuning de la Tâche #1)
        # Pour distilbert-base-uncased par défaut :
        # LABEL_1 est souvent interprété comme l'anomalie (Phishing)
        if label == "LABEL_1":
            # Si le modèle détecte une anomalie, le score "sain" diminue
            return round(1.0 - score, 3)
        
        return round(score, 3)

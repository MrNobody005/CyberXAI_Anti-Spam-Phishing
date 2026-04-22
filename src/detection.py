from typing import Optional

from transformers import pipeline


class PhishingDetector:
    """
    Détecteur ML basé sur un pipeline transformers.
    Renvoie un score de phishing entre 0.0 et 1.0
    """

    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        self.model_name = model_name
        self.pipeline = None

    def load(self) -> None:
        if self.pipeline is None:
            self.pipeline = pipeline(
                "text-classification",
                model=self.model_name,
                tokenizer=self.model_name,
                truncation=True,
            )

    def predict_phishing_score(self, text: str) -> float:
        """
        Score de phishing estimé entre 0 et 1.
        Ce mapping est provisoire tant qu'un modèle fine-tuné phishing
        n'est pas branché. Il permet d'intégrer le vrai pipeline DistilBERT.
        """
        if self.pipeline is None:
            raise RuntimeError("Le modèle n'est pas chargé.")

        if not text or not text.strip():
            return 0.5

        result = self.pipeline(text[:2000])[0]
        label = result["label"].upper()
        score = float(result["score"])

        # Mapping temporaire :
        # POSITIVE -> plutôt sûr
        # NEGATIVE -> plutôt suspect
        if label == "NEGATIVE":
            phishing_score = score
        else:
            phishing_score = 1.0 - score

        return round(min(max(phishing_score, 0.0), 1.0), 3)
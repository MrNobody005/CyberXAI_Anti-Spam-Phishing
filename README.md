# 🛡️ Système Hybride de Détection de Phishing

Ce projet propose une solution de détection de courriels frauduleux reposant sur une **architecture multi-modale**. Il combine des filtres de sécurité cyber, des heuristiques statistiques, un modèle de Deep Learning (DistilBERT) et une analyse sémantique par un modèle de langage réduit (SLM Phi-3).

---

## ⚖️ Disclaimer (Avertissement Légal)

> **[IMPORTANT] Cadre Éducatif et Non Professionnel**
> 
> Ce projet est réalisé par des **étudiants** dans un cadre strictement **pédagogique et non lucratif**. 
> * **Limites techniques** : Bien que le système affiche une résilience de 100% sur nos jeux de tests internes, il n'est pas conçu pour une utilisation en environnement de production critique.
> * **Responsabilité** : Les auteurs ne sauraient être tenus responsables des éventuels échecs de détection ou dommages liés à l'utilisation de cet outil.
> * **Données** : Ce logiciel traite des données textuelles. Aucune donnée n'est revendue ou utilisée en dehors du cadre de cette expérimentation scientifique.

---

## 🏛️ Architecture du Système

Le flux de données suit un pipeline de sécurité rigoureux pour garantir que l'IA ne soit pas manipulée par des attaques sémantiques.



1.  **Couche Cyber (Anti-Injection)** : Analyse du texte **brut** via des expressions régulières (Regex) et une liste noire pour bloquer les tentatives de *Prompt Injection* (ex: "Ignore instructions").
2.  **Couche Heuristique** : Recherche de signaux faibles (IBAN, mots d'urgence, majuscules excessives).
3.  **Couche ML (DistilBERT)** : Inférence rapide sur le texte nettoyé pour obtenir un premier score de probabilité.
4.  **Couche SLM (Phi-3)** : Analyse sémantique profonde via Ollama pour valider le verdict et fournir une explication.

---

## 📊 Méthodologie de Recherche et Données

### Sources de Données
*   **Kaggle** : Les données brutes proviennent de datasets publics de phishing (ex: `raw_mails.csv`).
*   **Traitement** : Le script `data_loader.py` normalise les labels (Sain vs Phishing) et nettoie les doublons.

### Entraînement (Google Colab & Hugging Face)
*   **Entraînement** : Le modèle a été fine-tuné sur **Google Colab** pour bénéficier de l'accélération GPU.
*   **Hébergement** : Le modèle final est hébergé sur **Hugging Face** (`nikosthoumyre/CyberXAI-Phishing-Detector`) et téléchargé dynamiquement par l'API.

---

## 💻 Structure du Répertoire

| Fichier / Dossier | Description |
| :--- | :--- |
| `src/main.py` | Point d'entrée FastAPI gérant l'orchestration des services. |
| `src/security.py` | Moteur de détection d'injections et sandbox de prompt. |
| `src/slm_analysis.py` | Interface de communication avec le modèle Phi-3 via Ollama. |
| `src/detection.py` | Chargeur du modèle DistilBERT depuis Hugging Face. |
| `src/scoring.py` | Logique de calcul du score final pondéré. |
| `src/pentest_report.py` | Script de test automatisé de la résilience cyber. |
| `notebooks/EDA_Analysis.ipynb` | Analyse exploratoire des données (longueur, répartition). |

---

## 🧪 Logique de Scoring

Le score de confiance final ($S_{final}$) est calculé selon une pondération hybride entre l'heuristique ($H$) et l'IA classique ($ML$) :

$$S_{final} = (0.4 \times H) + (0.6 \times ML)$$

Le verdict du **SLM Phi-3** intervient en complément sémantique pour confirmer le label final.

---

## 🚀 Installation et Utilisation

### Prérequis
*   Docker et Docker Compose.
*   Une connexion internet (pour le téléchargement initial du modèle Hugging Face).

### Lancement
1.  **Démarrer l'infrastructure** :
    ```bash
    docker compose up --build
    ```
2.  **Accéder à l'interface de test (Swagger)** :
    Rendez-vous sur `http://localhost:8000/docs`.

3.  **Lancer le Pentest** :
```bash
    python src/pentest_report.py
```

---

## 🛠️ Technologies Utilisées
*   **Backend** : FastAPI (Python 3.11).
*   **ML Frameworks** : Transformers (Hugging Face), PyTorch.
*   **LLM Runtime** : Ollama (Modèle Phi-3 Mini).
*   **Infrastucture** : Docker & Docker Compose.

---

## 📈 Résultats de Résilience
*   **Taux de détection des injections** : 100% sur le dataset `prompt_injections.csv`.
*   **Analyse Exploratoire** : Validée via le notebook EDA (répartition équilibrée des classes).

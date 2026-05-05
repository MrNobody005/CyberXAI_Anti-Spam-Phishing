# 🛡️ Système Hybride de Détection de Phishing

Ce projet propose une solution de détection de courriels frauduleux reposant sur une **architecture multi-modale**. Il combine des filtres de sécurité cyber, des heuristiques statistiques, un modèle de Deep Learning (DistilBERT) et une analyse sémantique par un modèle de langage réduit (SLM Phi-3).

---

## ⚖️ Disclaimer (Avertissement Légal)

> **[IMPORTANT] Cadre Éducatif et Non Professionnel**
>
> Ce projet est réalisé par des **étudiants** dans un cadre strictement **pédagogique et non lucratif**.
>
> Ce projet est réalisé par des **étudiants** dans un cadre strictement **pédagogique et non lucratif**.
>
> - **Limites techniques** : Ce prototype n'est pas conçu pour une utilisation en environnement de production critique.
> - **Responsabilité** : Les auteurs ne sauraient être tenus responsables des éventuels échecs de détection ou dommages liés à l'utilisation de cet outil.
> - **Données** : Aucune donnée traitée n'est conservée ou utilisée à des fins commerciales.

---

## 🏛️ Architecture du Système

Le système utilise un pipeline de détection à quatre niveaux :

1. **Couche Cyber (Anti-Injection)** : Analyse du texte **brut** via Regex pour bloquer les tentatives de manipulation du LLM (Jailbreak).
2. **Couche Heuristique** : Recherche de signaux faibles statistiques (IBAN, urgence, URLs).
3. **Couche ML (DistilBERT)** : Inférence rapide via un modèle fine-tuné sur Hugging Face (`nikosthoumyre/CyberXAI-Phishing-Detector`).
4. **Couche SLM (Phi-3 Mini)** : Analyse sémantique profonde via Ollama pour détecter les intentions malveillantes complexes.

---

## 📊 Méthodologie de Recherche et Données

### Entraînement et Données

- **Source** : Datasets publics Kaggle et Hugging Face (`zionia/phishing-emails`).
- **Entraînement** : Fine-tuning réalisé sur **Google Colab** (GPU T4) pour le modèle DistilBERT.

### Résultats de Résilience (Metrics)

- **Attaques par Injection** : **100%** de blocage sur le dataset de test interne.
- **Phishing Réel** : **~62%** de détection sémantique sur des échantillons externes complexes.
- **Faux Positifs** : Sécurité renforcée pour éviter de bloquer des termes communs (ex: "dans").

---

## 💻 Structure du Répertoire

| Fichier / Dossier              | Description                                                 |
| :----------------------------- | :---------------------------------------------------------- |
| `src/main.py`                  | Point d'entrée FastAPI gérant l'orchestration des services. |
| `src/security.py`              | Moteur de détection d'injections et sandbox de prompt.      |
| `src/slm_analysis.py`          | Interface de communication avec le modèle Phi-3 via Ollama. |
| `src/detection.py`             | Chargeur du modèle DistilBERT depuis Hugging Face.          |
| `src/scoring.py`               | Logique de calcul du score final pondéré.                   |
| `src/pentest_report.py`        | Script de test automatisé de la résilience cyber.           |
| `notebooks/EDA_Analysis.ipynb` | Analyse exploratoire des données (longueur, répartition).   |
| `src/resilience_evaluator.py`  | Stress test sur dataset réel (Hugging Face).                |

---

## 🧪 Logique de Scoring

Le score de confiance final ($S_{final}$) repose sur une décision multicritère :

$$S_{final} = (0.2 \times S_{Heuristique}) + (0.5 \times S_{DistilBERT}) + (0.3 \times S_{Phi3})$$

---

## 🚀 Installation et Utilisation

### Prérequis

- Docker et Docker Compose.
- Une connexion internet (pour le téléchargement initial du modèle Hugging Face).

### Lancement

1.  **Démarrer l'infrastructure** :
    ```bash
    docker compose up --build
    ```
2.  **Accéder à l'interface de test (Swagger)** :
    Rendez-vous sur `http://localhost:8000/docs`.

3.  **Lancer l'évaluation de résilience externe** :

```bash
    python3 src/resilience_evaluator.py
```

---

## 🛠️ Technologies Utilisées

- **Backend** : FastAPI (Python 3.11).
- **ML Frameworks** : Transformers (Hugging Face), PyTorch.
- **LLM Runtime** : Ollama (Modèle Phi-3 Mini).
- **Infrastucture** : Docker & Docker Compose.

---

## 📈 Résultats de Résilience

- **Taux de détection des injections** : 100% sur le dataset `prompt_injections.csv`.
- **Analyse Exploratoire** : Validée via le notebook EDA (répartition équilibrée des classes).

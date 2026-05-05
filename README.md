# 🛡️ Système de Détection de Phishing

Ce projet propose une infrastructure de détection multi-couches combinant la rapidité du Deep Learning (DistilBERT) et la profondeur sémantique des Small Language Models (SLM Phi-3) pour sécuriser les flux de messagerie contre le phishing et les injections de prompt.

---

## ⚖️ Disclaimer (Avertissement Légal)

> **[IMPORTANT] Cadre Éducatif et Non Professionnel**
>
> Ce projet est réalisé par des **étudiants** dans un cadre strictement **pédagogique et non lucratif**.
> - **Limites techniques** : Ce prototype n'est pas conçu pour une utilisation en environnement de production critique.
> - **Responsabilité** : Les auteurs ne sauraient être tenus responsables des éventuels échecs de détection ou dommages liés à l'utilisation de cet outil.
> - **Données** : Aucune donnée traitée n'est conservée ou utilisée à des fins commerciales.

---

## 🏛️ Architecture du Système

Le système utilise un pipeline de détection à quatre niveaux :

1. **Couche Cyber (Anti-Injection)** : Analyse du texte **brut** via Regex pour bloquer les tentatives de manipulation du LLM (Jailbreak).
2. **Couche Heuristique** : Recherche de signaux faibles statistiques (IBAN, urgence, URLs).
3. **Couche ML (DistilBERT)** : Inférence rapide via un modèle fine-tuné sur Hugging Face (`nikosthoumyre/CyberXAI-Phishing-Detector`).
4. **Couche SLM (Phi-3 Mini)** : Analyse sémantique profonde via Ollama pour valider le verdict et fournir une explication textuelle.

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

```text
mrnobody005-cyberxai_anti-spam-phishing/
├── data/
│   └── prompt_injections.csv   # Dataset d'attaques local pour l'audit
├── src/
│   ├── main.py                # Point d'entrée FastAPI gérant l'orchestration des services et Dashboard Web
│   ├── security.py            # Moteur de détection d'injections et sandbox de prompt.  
│   ├── slm_analysis.py        # Interface de communication avec le modèle Phi-3 via Ollama. 
│   ├── detection.py           # Chargeur du modèle DistilBERT depuis Hugging Face.
│   ├── scoring.py             # Logique de calcul du score final pondéré.   
│   ├── heuristic.py           # Analyse des signaux faibles
│   └── cleaner.py             # Nettoyage sémantique (HTML, SMTP)
├── templates/
│   └── index.html             # Interface visuelle du Dashboard
├── docker-compose.yaml        # Orchestration API + IA
├── Dockerfile                 # Environnement de conteneurisation
└── requirements.txt           # Dépendances Python
```

---

## 🧪 Logique de Scoring

Le score de confiance final ($S_{final}$) repose sur une décision multicritère :

$$S_{final} = (0.2 \times S_{Heuristique}) + (0.5 \times S_{DistilBERT}) + (0.3 \times S_{Phi3})$$

---

## 🚀 Installation et Utilisation

### Prérequis

- Docker et Docker Compose (obligatoire).
- **Python 3.11+** (optionnel, uniquement pour le développement local).

### 2. Lancement (Docker)
C'est la méthode recommandée. L'environnement complet est configuré automatiquement.
```bash
# Cloner le projet et lancer l'infrastructure
docker compose up --build
```
*Note : Le premier lancement télécharge les modèles IA (environ 2 Go).*

### 3. Accès au Dashboard
Une fois les conteneurs démarrés, ouvrez votre navigateur :
- **Dashboard Web** : `http://localhost:8000` (Interface interactive pour les tests)
- **Documentation API** : `http://localhost:8000/docs` (Swagger UI)

### Note sur l'environnement Virtuel (venv)
Si vous souhaitez travailler sur le code hors Docker (pour votre IDE) :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
```
*Cependant, pour que l'analyse fonctionne hors Docker, vous devrez avoir Ollama installé localement sur votre machine.*

---

## 🛠️ Technologies Utilisées

- **Backend** : FastAPI (Python 3.11).
- **IA/ML** : Transformers (Hugging Face), PyTorch, Ollama (Phi-3 Mini)
- **Frontend** : HTML5/CSS3 (Tailwind CSS), Jinja2
- **Infrastucture** : Docker & Docker Compose.

---

## 📈 Résultats de Résilience

- **Attaques par Injection** : **100%** de blocage (Audit Pentest interne)
- **Phishing Réel** : **~62%** de détection sur des échantillons complexes (Dataset Hugging Face).
- **Faux Positifs** : Filtres optimisés pour la langue française (gestion des mots courts comme "dans").


# TÂCHE LIÉE : TT-15 (Écrire le Dockerfile pour l'API)
# 1. Image de base légère
FROM python:3.11-slim-bookworm

# 2. Sécurité : Mise à jour des paquets système pour boucher les failles
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3. Correction des Warnings (Format KEY=VALUE)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 5. SÉCURITÉ CRUCIALE : Créer un utilisateur non-root
# Pour éviter qu'un attaquant n'ait les droits admin
RUN useradd -m cyberuser
USER cyberuser

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
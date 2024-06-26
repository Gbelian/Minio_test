#!/usr/bin/env bash
# Exit on error
set -o errexit


# Mettre à jour pip et installer les dépendances
python -m pip install --upgrade pip
pip install gunicorn
pip install -r requirements.txt

# Créer des migrations de base de données basées sur les modèles
python manage.py makemigrations

# Appliquer les migrations de base de données
python manage.py migrate

.\minio.exe server /data

# Collecte des fichiers statiques
python manage.py collectstatic --no-input

# Créer un superutilisateur (admin)
echo "from django.contrib.auth.models import User; User.objects.create_superuser('beninbmcn', 'BMCN.UAC@gmail.com', 'beninbmcn')" | python manage.py shell

# Lancer le serveur Gunicorn
gunicorn monprojet.wsgi:application --bind 0.0.0.0:$PORT --workers 4


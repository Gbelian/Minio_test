#!/usr/bin/env bash
# Exit on error
set -o errexit

# Mettre à jour pip et installer les dépendances
python -m pip install --upgrade pip
pip install gunicorn
pip install -r requirements.txt

# Télécharger et configurer MinIO Client (mc)
wget https://dl.min.io/client/mc/release/linux-amd64/mc -O /usr/local/bin/mc
chmod +x /usr/local/bin/mc

# Configurer et démarrer MinIO Server avec des identifiants par défaut
wget https://dl.min.io/server/minio/release/linux-amd64/minio -O /usr/local/bin/minio
chmod +x /usr/local/bin/minio
export MINIO_ACCESS_KEY=minioadmin
export MINIO_SECRET_KEY=minioadmin
nohup minio server /data &

# Attendre que MinIO démarre
sleep 10

# Vérifier si le port MinIO est ouvert
if nc -zv 127.0.0.1 9000; then
  echo "MinIO est en cours d'exécution sur le port 9000"
else
  echo "Erreur : MinIO n'a pas pu démarrer sur le port 9000"
  exit 1
fi

# Configurer MinIO Client (mc) avec les mêmes identifiants
mc alias set myminio http://127.0.0.1:9000 minioadmin minioadmin
mc mb myminio/data

# Créer des migrations de base de données basées sur les modèles
python manage.py makemigrations

# Appliquer les migrations de base de données
python manage.py migrate

# Collecte des fichiers statiques
python manage.py collectstatic --no-input

# Créez un superutilisateur (admin)
echo "from django.contrib.auth.models import User; User.objects.create_superuser('beninbmcn', 'BMCN.UAC@gmail.com', 'beninbmcn')" | python manage.py shell

# Définir le port Gunicorn explicitement
export PORT=${PORT:-8000}

# Lancez le serveur Gunicorn
gunicorn monprojet.wsgi:application --bind 0.0.0.0:$PORT --workers 4

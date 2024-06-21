#!/usr/bin/env bash
# exit on error
set -o errexit

# Mettre à jour pip et installer les dépendances
python -m pip install --upgrade pip
pip install gunicorn

pip install -r requirements.txt

# Create database migrations based on models
python manage.py makemigrations

# Apply the database migrations
python manage.py migrate

# Configurer et démarrer MinIO Server avec des identifiants par défaut
wget https://dl.min.io/server/minio/release/linux-amd64/minio -O /usr/local/bin/minio
chmod +x /usr/local/bin/minio
export MINIO_ACCESS_KEY=minioadmin
export MINIO_SECRET_KEY=minioadmin
nohup minio server /data &

# Télécharger et configurer MinIO Client (mc) avec les mêmes identifiants
wget https://dl.min.io/client/mc/release/linux-amd64/mc -O /usr/local/bin/mc
chmod +x /usr/local/bin/mc
mc alias set myminio http://localhost:9000 minioadmin minioadmin
mc mb myminio/your-bucket-name


# Collecte des fichiers statiques et migrations
python manage.py collectstatic --no-input
python manage.py migrate

# Créez un superutilisateur (admin)
echo "from django.contrib.auth.models import User; User.objects.create_superuser('beninbmcn', 'BMCN.UAC@gmail.com', 'beninbmcn')" | python manage.py shell

# Lancez le serveur Gunicorn
gunicorn monprojet.wsgi:application --bind 0.0.0.0:$PORT --workers 4
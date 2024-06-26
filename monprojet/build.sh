#!/usr/bin/env bash
# Exit on error
set -o errexit

# Mettre à jour pip et installer les dépendances Python
python -m pip install --upgrade pip
pip install gunicorn
pip install -r requirements.txt

# Télécharger et configurer MinIO Client (mc)
wget https://dl.min.io/client/mc/release/linux-amd64/mc -O /tmp/mc
chmod +x /tmp/mc

# Créer des migrations de base de données basées sur les modèles Django
python manage.py makemigrations

# Appliquer les migrations de base de données Django
python manage.py migrate

# Télécharger et configurer MinIO Server avec des identifiants par défaut
wget https://dl.min.io/server/minio/release/linux-amd64/minio -O /tmp/minio
chmod +x /tmp/minio

# Démarrer MinIO Server en arrière-plan avec les identifiants par défaut
export MINIO_ROOT_USER=minioadmin
export MINIO_ROOT_PASSWORD=minioadmin
nohup /tmp/minio server /data &

# Attendre que MinIO démarre (ajustez le temps d'attente si nécessaire)
sleep 10

# Configurer MinIO Client (mc) avec les mêmes identifiants pour interagir avec le serveur MinIO
/tmp/mc alias set myminio http://127.0.0.1:9000 minioadmin minioadmin
/tmp/mc mb myminio/data

# Collecter les fichiers statiques Django
python manage.py collectstatic --no-input

# Créer un superutilisateur Django (admin)
echo "from django.contrib.auth.models import User; User.objects.create_superuser('beninbmcn', 'BMCN.UAC@gmail.com', 'beninbmcn')" | python manage.py shell

# Lancer le serveur Gunicorn pour le projet Django
gunicorn monprojet.wsgi:application --bind 0.0.0.0:$PORT --workers 4

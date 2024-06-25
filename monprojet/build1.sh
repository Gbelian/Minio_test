#!/usr/bin/env bash
# Exit on error
set -o errexit

# Fonction pour afficher les messages de journalisation
log() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1"
}

log "Mise à jour de pip et installation des dépendances"
python -m pip install --upgrade pip
pip install gunicorn
pip install -r requirements.txt

log "Téléchargement et configuration de MinIO Client (mc)"
wget https://dl.min.io/client/mc/release/linux-amd64/mc -O /usr/local/bin/mc
chmod +x /usr/local/bin/mc

log "Configuration de MinIO Client (mc) avec les mêmes identifiants"
mc alias set myminio http://127.0.0.1:9000 minioadmin minioadmin || true
mc mb myminio/data || true

log "Téléchargement et démarrage de MinIO Server"
wget https://dl.min.io/server/minio/release/linux-amd64/minio -O /usr/local/bin/minio
chmod +x /usr/local/bin/minio
export MINIO_ACCESS_KEY=minioadmin
export MINIO_SECRET_KEY=minioadmin
nohup minio server /data &

log "Attendre que MinIO démarre"
sleep 10

log "Création des migrations de base de données"
python manage.py makemigrations

log "Application des migrations de base de données"
python manage.py migrate

log "Collecte des fichiers statiques"
python manage.py collectstatic --no-input

log "Création d'un superutilisateur (admin)"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('beninbmcn', 'BMCN.UAC@gmail.com', 'beninbmcn')" | python manage.py shell

log "Définition du port Gunicorn explicitement"
export PORT=${PORT:-8000}

log "Lancement du serveur Gunicorn"
gunicorn monprojet.wsgi:application --bind 0.0.0.0:$PORT --workers 4

log "Script terminé"

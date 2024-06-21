#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip to the latest version
python -m pip install --upgrade pip

pip install gunicorn

# Install required packages from requirements.txt
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Create database migrations based on models
python manage.py makemigrations

# Apply the database migrations
python manage.py migrate

# Create a superuser (admin)
echo "from django.contrib.auth.models import User; User.objects.create_superuser('beninbmcn', 'BMCN.UAC@gmail.com', 'beninbmcn')" | python manage.py shell

# Start the Gunicorn server
gunicorn monprojet.wsgi:application --bind 0.0.0.0:$PORT --workers 4

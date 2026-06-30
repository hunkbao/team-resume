#!/bin/bash
set -e

echo "=== Creating required directories ==="
mkdir -p /app/staticfiles
mkdir -p /app/media

echo "=== Running migrations ==="
python manage.py migrate --noinput 2>&1 || echo "WARNING: Migration failed, continuing..."

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput 2>&1 || echo "WARNING: Collectstatic failed, continuing..."

echo "=== Creating superuser if not exists ==="
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password=os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin2026')
    )
    print('Superuser created.')
else:
    print('Superuser already exists.')
" 2>&1 || echo "WARNING: Superuser creation failed, continuing..."

echo "=== Starting server on port $PORT ==="
exec gunicorn team_resume.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 120

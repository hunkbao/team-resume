#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if not exists..."
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
"

echo "Starting server..."
exec gunicorn team_resume.wsgi:application --bind 0.0.0.0:$PORT --workers 2

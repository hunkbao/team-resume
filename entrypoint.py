"""Railway entrypoint: migrate, collectstatic, create superuser, start gunicorn."""
import os
import subprocess
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_resume.settings')


def run(cmd):
    print(f"=== {cmd} ===")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"WARNING: command failed with code {result.returncode}, continuing...")


def main():
    # Create required directories
    os.makedirs('/app/staticfiles', exist_ok=True)
    os.makedirs('/app/media', exist_ok=True)
    print("=== Directories created ===")

    # Migrate database
    run('python manage.py migrate --noinput')

    # Collect static files
    run('python manage.py collectstatic --noinput')

    # Create superuser
    django.setup()
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password=os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin2026')
        )
        print('=== Superuser created ===')
    else:
        print('=== Superuser already exists ===')

    # Start gunicorn
    port = os.environ.get('PORT', '8080')
    print(f"=== Starting gunicorn on port {port} ===")
    os.execvp('gunicorn', [
        'gunicorn', 'team_resume.wsgi:application',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '2',
        '--timeout', '120',
    ])


if __name__ == '__main__':
    main()

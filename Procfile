release: python manage.py migrate
web: python manage.py collectstatic --no-input; gunicorn msnmatch.wsgi --preload --timeout 60

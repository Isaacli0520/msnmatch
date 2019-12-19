release: python manage.py migrate
web: python manage.py collectstatic --no-input; daphne msnmatch.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2

#!/bin/env

echo "Running migrations..."
python manage.py migrate
echo "Collect static files..."
python manage.py collectstatic --noinput

gunicorn --bind 0.0.0.0:8000 lendme_api.wsgi:application

exec "$@"
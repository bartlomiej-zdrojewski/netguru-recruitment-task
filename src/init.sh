#!/bin/bash

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

if [ "$DJANGO_DEBUG" = "False" ]; then
    echo "Starting server in production mode..."
    gunicorn --bind 0.0.0.0:8000 app.wsgi
else
    echo "Starting server in debug mode..."
    python manage.py runserver 0.0.0.0:8000
fi

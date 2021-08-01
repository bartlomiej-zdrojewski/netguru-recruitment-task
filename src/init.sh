#!/bin/bash

echo "INIT | Applying migrations..."
python manage.py migrate

echo "INIT | Collecting static files..."
python manage.py collectstatic --noinput

if [ "$DJANGO_TESTS" = "True" ]; then
    echo "INIT | Running tests..."
    python manage.py test
fi

if [ "$DJANGO_DEBUG" = "True" ]; then
    echo "INIT | Launching server in debug mode..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "INIT | Launching server in production mode..."
    gunicorn --bind 0.0.0.0:8000 app.wsgi
fi

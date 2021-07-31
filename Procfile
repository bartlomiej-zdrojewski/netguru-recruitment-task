release: python ./src/manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn --pythonpath src app.wsgi

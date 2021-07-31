# Netguru Recruitment Task

in debug mode runs as
python manage.py runserver

in production mode as
gunicorn app.wsgi

variables.env is example file. change its content in production enviorment

data in database is persistent. delete db_data to reset database.

## TODO

1. Add NGINX to serve static files.

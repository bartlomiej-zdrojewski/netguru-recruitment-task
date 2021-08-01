# Netguru Recruitment Task

in debug mode runs as
python manage.py runserver

in production mode as
gunicorn app.wsgi

to access shell
docker exec -ti netguru-recruitment-task_app_1 /bin/bash

variables.env is example file. change its content in production enviorment

data in database is persistent. delete db_data to reset database.

Admin
login: admin
password: zaq1@WSX

API
allows duplicates
if no rating for a car -> avg_rating = 0
popular returns top 5 cars

## TODO

1. Add NGINX to serve static files.
2. swagger on /

# Netguru Recruitment Task

## Launching

To launch the application, type:

```
docker-compose up
```

In debug mode it will execute `python manage.py runserver` command, so you can edit the source code while container is running. In production mode it will execute `gunicorn app.wsgi` without the live-reload.

To access the command line while container is running, type:

```
docker exec -ti netguru-recruitment-task_app_1 /bin/bash
```

## Configuration

The `variables.env` file contains parameters that change a behaviour of the application:

- `DJANGO_DEBUG` when set to `True` launches the server in debug mode; default is `False` and server launches in production mode;

- `DJANGO_TESTS` when set to `True` runs tests before launching the server; default is `True`;

- `DJANGO_SECRET_KEY` defines a secret key used by Django framework for cryptographic purposes; it should never ever be stored in a repository, but it is an example application, so it was kept for a covience;

The default port is `8000`. To change it, you have to edit the
`docker-compose.yaml` file.

## Creditentials

To access an admin site, use the following creditentials:

- login: `admin`

- password: `zaq1@WSX`

## Important details

endpoints must end in trailing slash `/`.

data in database is persistent. delete db_data to reset database.

API
allows duplicates
if no rating for a car -> avg_rating = 0
popular returns top 5 cars

added count parameter to GET /popular

validating car make is case-insensitive

## Further improvements

1. Implement a Swagger documentation accessible from `/` or `/docs` endpoint.

2. Configure NGINX to serve the static files. For now the static files are only accessible in debug mode.

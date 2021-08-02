# Netguru Recruitment Task

```
NOTE | Please see the "Important details" section for the list of assumptions.
```

## Launching

To launch the application, type:

```
docker-compose up
```

In debug mode it will execute `python manage.py runserver` command, so you can
edit the source code while the container is running. In production mode it will
execute `gunicorn app.wsgi` without the live-reload.

To access the command line while container is running, type:

```
docker exec -ti netguru-recruitment-task_app_1 /bin/bash
```

Assuming `netguru-recruitment-task_app_1` is the container's name.

Then, to launch the tests, type:

```
python manage.py test
```

## Configuration

The `variables.env` file contains parameters that change a behaviour of the
application:

- `DJANGO_DEBUG` when set to `True` launches the server in debug mode; the
default is `False` and server launches in production mode;

- `DJANGO_TESTS` when set to `True` runs tests before launching the server;
the default is `False`;

- `DJANGO_SECRET_KEY` defines a secret key used by Django framework for
cryptographic purposes; it should never ever be stored in a repository, but it
is an example application, so it was kept for a convenience;

The default port is `8000`. To change it, you have to edit the
`docker-compose.yaml` file.

## Important details

### API

While implementing the API, the following assumptions were made:

- all endpoints must end in a trailing slash `/`; it will not matter in `GET`
request but may return an error in `POST` and `DELETE` requests;

- `/cars` endpoint allows creating cars with the same mark and model;

- `/cars` endpoint, while creating a car, validates make using case-insensitive
comparison;

- `/cars` endpoint for a car with no rates returns it's `avg_rating` property
equal to 0;

- `/popular` endpoint returns **all** cars sorted by `rates_number` property;

- `/popular` endpoint takes a `count` parameter defining a maximum number of
results in the response; only the top results are listed;

### Docker

Database is stored in `db_data` named volume, so it will not be removed with
it's container. To remove the database, type:

```
docker volume rm netguru-recruitment-task_db_data
```

Assuming `netguru-recruitment-task_db_data` is the volume's name.

## Further improvements

1. Implement a Swagger documentation accessible from `/` or `/docs` endpoint.

2. Configure NGINX to serve static files. For now the static files are only
accessible in debug mode.

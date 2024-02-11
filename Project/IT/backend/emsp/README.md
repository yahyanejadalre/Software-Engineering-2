# emsp-back-end

## Running the application

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file emsp/settings/environments/.env up -d
```

Run the following command in the back-end container. to do that first you have to run this command:

```bash
docker exec -it emsp_backend /bin/bash
```

Then migrate the database:

```bash
python manage.py migrate
```

## Create default SuperUser

```bash
./manage.py createsuperuser --no-input
```

## Populate database

```bash
    ./manage.py faker --user [USERS COUNT] --station [USERS COUNT] --history [USERS COUNT]
```

or just leave it empty to populate with default values

```bash
    ./manage.py faker
```

It is not necessary to pass arguments to the command, if you do not pass arguments, the default values will be used.
If the database is not empty, the command will skipp populating.

## Environment variables Example

You have to create a .env file in the emsp/settings/environments folder with the following variables:

```
# The database configuration for Django and docker-compose setup
# If you are using docker-compose, host should be the name of the related container in the docker-compose.yml file
DEFAULT_DB_NAME=emsp
DEFAULT_DB_USER=emsp
DEFAULT_DB_PASSWORD=emsp
DEFAULT_DB_HOST=emsp_db
DEFAULT_DB_PORT=5432


DJANGO_SUPERUSER_PASSWORD=emsp
DJANGO_SUPERUSER_USERNAME=emsp
DJANGO_SUPERUSER_EMAIL=emsp@mail.com

MODE=development
```
# cpms-back-end

## Running the application

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file cpms/settings/environments/.env up -d
```

## Populate database

```bash
    ./manage.py faker --count [DSOs COUNT]
```

or just leave it empty to populate with default values

## Create default SuperUser

```bash
./manage.py createsuperuser --no-input
```


## Environment variables Example

You have to create a .env file in the cpms/settings/environments folder with the following variables:

```
# The database configuration for Django and docker-compose setup
# If you are using docker-compose, host should be the name of the related container in the docker-compose.yml file
DEFAULT_DB_NAME=cpms
DEFAULT_DB_USER=cpms
DEFAULT_DB_PASSWORD=cpms
DEFAULT_DB_HOST=localhost
DEFAULT_DB_PORT=5434


DJANGO_SUPERUSER_PASSWORD=cpms
DJANGO_SUPERUSER_USERNAME=cpms
DJANGO_SUPERUSER_EMAIL=cpms@mail.com

MODE=development

EMSP_URL=http://161.35.153.88:8000/api/
EMSP_USERNAME=emsp
EMSP_PASSWORD=emsp

```
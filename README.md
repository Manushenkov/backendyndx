Python api, enrollment task for yandex backend school

# What's inside?

The app is packed into docker containers and is run via docker-compose

# How to use it?

## How to start the service?

first build app image


    docker build -t flaskapp:latest .

Then start the app and database containers using docker-compose


    docker-compose up -d

# Development

## How to start development server?

Change SQLALCHEMY_DATABASE_URI in app.config in app to your database's URL and run


    pipenv install
    pipenv shell
    flask run --port=PORT

## How to run tests?

I added a 6 new tests testing ivalid imports, id's, dates and url's


    python3 unit_test.py

## Other

My local machine (m1 macbook) only supports psycopg2, but the remote linux machine only accepts psycopg2-binary. so be aware of it if you want to test it on your machine if it's a macbook too because you might need to change this dependency

for auto-restart upon system reboot i ran this script: https://techoverflow.net/2020/10/24/create-a-systemd-service-for-your-docker-compose-project-in-10-seconds/

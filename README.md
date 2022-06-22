# backendyndx

build app image:
docker build -t flaskapp:latest .

run containers with the app and database:
docker-compose up -d

My local machine (m1 macbook) only supports psycopg2, but the remote linux machine only accepts psycopg2-binary. so be aware of it if you want to test it on your machine if it's a macbook too because you might need to change this dependency

for auto-restart upon system reboot i ran this script:
https://techoverflow.net/2020/10/24/create-a-systemd-service-for-your-docker-compose-project-in-10-seconds/

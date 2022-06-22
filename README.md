# backendyndx

<!-- postgres:
docker run --name postgres -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres -->

app:
docker build -t flaskapp:latest .

<!-- docker run -p 0.0.0.0:80:80 flaskapp -->

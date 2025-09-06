# Testing - Locust

[Back](../../index.md)

---

- `docker-compose.yaml`

```yaml
services:
  master:
    container_name: master
    image: locustio/locust
    volumes:
      - ./:/mnt/locust
    ports:
      - "8089:8089"
    command: >
      -f /mnt/locust/locustfile.py
      --master
      --web-host 0.0.0.0
      --expect-workers 2

  worker:
    image: locustio/locust
    volumes:
      - ./:/mnt/locust
    command: >
      -f /mnt/locust/locustfile.py
      --worker
      --master-host master
    depends_on:
      - master
```

- `locustfile.py`

```py
from locust import HttpUser, task, between
import os

API_URLS = {
    "home": "https://trip.arguswatcher.net/",
    "bike": "https://trip.arguswatcher.net/prod/bike",
    "station": "https://trip.arguswatcher.net/prod/station",
    "top_station": "https://trip.arguswatcher.net/prod/top-station",
    "trip_month": "https://trip.arguswatcher.net/prod/trip-month",
    "trip_hour": "https://trip.arguswatcher.net/prod/trip-hour",
}


class APIUser(HttpUser):
    host = os.getenv("TARGET_HOST", "https://trip.arguswatcher.net")
    wait_time = between(0.5, 1.5)

    @task
    def home(self):
        self.client.get(API_URLS["home"])

    @task
    def bike(self):
        self.client.get(API_URLS["bike"])

    @task
    def station(self):
        self.client.get(API_URLS["station"])

    @task
    def top_station(self):
        self.client.get(API_URLS["top_station"])

    @task
    def trip_month(self):
        self.client.get(API_URLS["trip_month"])

    @task
    def trip_hour(self):
        self.client.get(API_URLS["trip_hour"])

```

- Start testing

```sh
cd locust
docker compose down && docker compose up -d --scale worker=2

# smoke Testing
docker compose exec -it master locust -f /mnt/locust/locustfile.py --headless --expect-workers 2 -u 2 -r 2 --host https://trip.arguswatcher.net --run-time 2m --html /mnt/locust/html/smoke.html --csv /mnt/locust/csv/smoke

# baseline Testing
docker compose exec -it master locust -f /mnt/locust/locustfile.py --headless --expect-workers 2 -u 50 -r 1 --host https://trip.arguswatcher.net --run-time 2m --html /mnt/locust/html/baseline.html --csv /mnt/locust/csv/baseline

# load Testing - VU 100
docker compose exec -it master locust -f /mnt/locust/locustfile.py --headless --expect-workers 2 -u 100 -r 5 --host https://trip.arguswatcher.net --run-time 5m --html /mnt/locust/html/load_100.html --csv /mnt/locust/csv/load_100


# load Testing - VU 300
docker compose exec -it master locust -f /mnt/locust/locustfile.py --headless --expect-workers 2 -u 300 -r 5 --host https://trip.arguswatcher.net --run-time 5m --html /mnt/locust/html/load_300.html --csv /mnt/locust/csv/load_300


# load Testing - VU 500
docker compose exec -it master locust -f /mnt/locust/locustfile.py --headless --expect-workers 2 -u 500 -r 5 --host https://trip.arguswatcher.net --run-time 5m --html /mnt/locust/html/load_500.html --csv /mnt/locust/csv/load_500


# Stress Testing - VU 1000
docker compose exec -it master locust -f /mnt/locust/locustfile.py --headless --expect-workers 2 -u 1000 -r 20 --host https://trip.arguswatcher.net --run-time 5m --html /mnt/locust/html/load_1000.html --csv /mnt/locust/csv/load_1000

# Soak Testing
docker compose exec -it master locust -f /mnt/locust/locustfile.py --headless --expect-workers 2 -u 200 -r 20 --host https://trip.arguswatcher.net --run-time 10m --html /mnt/locust/html/soak_200_10m.html --csv /mnt/locust/csv/soak_200_10m
```

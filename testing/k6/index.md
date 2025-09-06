# Testing - K6

[Back](../../index.md)

---

## Demo

- https://grafana.com/docs/k6/latest/get-started/running-k6/

```js
import http from "k6/http";
import { sleep } from "k6";

export const options = {
  iterations: 10,
};

export default function () {
  http.get("https://quickpizza.grafana.com");
  sleep(1);
}
```

```sh
docker run --rm -i grafana/k6 run --vus 10 --duration 30s - <demo.js
```

---

## K6 Cloud

- Using Docker

- `Dockerfile`

```dockerfile
FROM grafana/k6:latest
WORKDIR /app
CMD ["k6", "--version"]
```

- .env
  - no any quotation

```txt
K6_CLOUD_TOKEN=
K6_CLOUD_PROJECT_ID=
```

- `cloud_smoke.js`

```js
import http from "k6/http";
import { check, sleep } from "k6";

const HOME_URL = "https://trip.arguswatcher.net";
const BIKE_URL = "https://trip.arguswatcher.net/prod/bike";
const STATION_URL = "https://trip.arguswatcher.net/prod/station";
const TRIP_HOUR_URL = "https://trip.arguswatcher.net/prod/trip-hour";
const TRIP_MONTH_URL = "https://trip.arguswatcher.net/prod/trip-month";
const TOP_STATION_URL = "https://trip.arguswatcher.net/prod/top-station";

export const options = {
  vus: 2,
  duration: "10s",
  cloud: {
    name: "Smoke Testing",
  },
};

// Smoke testing
export default () => {
  // home
  const homeRes = http.get(HOME_URL);
  check(homeRes, { "status returned 200": (r) => r.status == 200 });

  // bike
  const bikeRes = http.get(BIKE_URL);
  check(bikeRes, { "status returned 200": (r) => r.status == 200 });

  // station
  const stationRes = http.get(STATION_URL);
  check(stationRes, { "status returned 200": (r) => r.status == 200 });

  // trip hour
  const tripHourRes = http.get(TRIP_HOUR_URL);
  check(tripHourRes, { "status returned 200": (r) => r.status == 200 });

  // trip month
  const tripMonthRes = http.get(TRIP_MONTH_URL);
  check(tripMonthRes, { "status returned 200": (r) => r.status == 200 });

  // top station
  const topStationRes = http.get(TOP_STATION_URL);
  check(topStationRes, { "status returned 200": (r) => r.status == 200 });

  sleep(1);
};
```

```sh
cd k6
docker build -t k6 .

# cloud run
docker run --rm --name k6_con --env-file ./.env -v ./script:/app k6 cloud run cloud_smoke.js
# export report
docker run --rm --name k6_con -e K6_WEB_DASHBOARD=true -e K6_WEB_DASHBOARD_EXPORT=stress_200.html -v ./script:/app k6 run local_stress_200.js
```

- Visualize testing in Grafana Cloud

  - https://grafana.com/products/cloud/

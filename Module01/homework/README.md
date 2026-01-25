# Docker & PostgresSQL

## Q1 Docker image
To check the version of pip in a `python:3.13` image, first run the python container in docker with an interactive terminal as entrypoint
```bash
docker run -it --rm --entrypoint=bash python:3.13
```
then check its version
```bash
pip --version
```
\> pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)

## Q2 Docker networking and docker-compose

In the following `docker-compose.yaml` file, `db` is the `hostname` for pgadmin to connect, as docker compose uses the **service name** at the top line for the services to reach each other, instead of the container_name.

`5432` is the `port` that pgadmin connects to. When run `docker-compose up`, docker compose automatically creates a single bridge network for the target project. Containers inside this network talk to each other directly on their **internal ports**.
```
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

## Q3 Counting short trips
For the trips in November 2025 (`lpep_pickup_datetime` between '2025-11-01' and '2025-12-01', exclusive of the upper bound), with a `trip_distance` of less than or equal to 1 mile, the total count was
```sql
SELECT COUNT(*) AS count
FROM green_taxi_data t
WHERE lpep_pickup_datetime >= DATE '2025-11-01'
	AND lpep_pickup_datetime < DATE '2025-12-01'
	AND trip_distance <= 1.0;
```
\> 8007

## Q4 Longest trip for each day
The pick up day with the longest trip distance was (only consider trips with `trip_distance` less than 100 miles to exclude data errors)
```sql
SELECT CAST(lpep_pickup_datetime AS DATE) AS date,
	trip_distance
FROM green_taxi_data
WHERE trip_distance = (
	SELECT MAX(trip_distance)
	FROM green_taxi_data
	WHERE trip_distance < 100.0
);
```
\> 2025-11-14

## Q5 Biggest pickup zone
The pickup zone with the largest `total_amount` (sum of all trips) on November 18th, 2025 was
```sql
SELECT zpu."Zone",
	SUM(t."total_amount") AS "amount"
FROM green_taxi_data t
LEFT JOIN
	zones zpu ON t."PULocationID" = zpu."LocationID"
WHERE CAST(t."lpep_pickup_datetime" AS DATE) = '2025-11-18 00:00:00'
GROUP BY
	zpu."Zone"
ORDER BY
	"amount" DESC
LIMIT 1;
```
\> East Harlem North

## Q6 Largest tip
For the passengers picked up in the zone named "East Harlem North" in November 2025, the drop off zone that had the largest tip was
```sql
SELECT zdo."Zone",
	MAX(t."tip_amount") AS tip
FROM green_taxi_data t
LEFT JOIN
	zones zpu ON t."PULocationID" = zpu."LocationID"
LEFT JOIN
	zones zdo ON t."DOLocationID" = zdo."LocationID"
WHERE t.lpep_pickup_datetime >= DATE '2025-11-01'
	AND t.lpep_pickup_datetime < DATE '2025-12-01'
	AND zpu."Zone" = 'East Harlem North'
GROUP BY
	zdo."Zone"
ORDER BY
	tip DESC
LIMIT 1;
```
\> Yorkville West
# Sensors API
Query Ruuvitag sensor measurements from InfluxDB.

## Setup environment variables
Create ".env" file to project root.

Variable name | Comments
--- | --- |
INFLUXDB_HOST | Address of the InfluxDB server
INFLUXDB_PORT | InfluxDB server port
INFLUXDB_DB | InfluxDB Database containing measurements
## Launch development server
`uvicorn main:app --reload`

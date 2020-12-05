# Sensors API
Query Ruuvitag sensor measurements from InfluxDB.

## Install Python requirements
`pip install requirements.txt`

## Setup environment variables
Create ".env" file to project root with following variables.

Variable name | Comments
--- | --- |
INFLUXDB_HOST | Address of the InfluxDB server
INFLUXDB_PORT | InfluxDB server port
INFLUXDB_DB | InfluxDB Database containing measurements
## Launch development server
`uvicorn main:app --reload`

## Documentation location
http://127.0.0.1:8000/redoc  
http://127.0.0.1:8000/docs

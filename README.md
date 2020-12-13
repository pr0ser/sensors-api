# Sensors API
Query Ruuvitag sensor measurements from InfluxDB.

## Install Python requirements
`pip install -r requirements.txt`

## Setup environment variables
Create ".env" file to project root with following variables.

Variable name | Comments
--- | --- |
INFLUXDB_HOST | Address of the InfluxDB server
INFLUXDB_PORT | InfluxDB server port
INFLUXDB_DB | InfluxDB Database containing measurements
SENSORS | Ruuvitag sensor names separated with comma
TEST_URL | Open API schema URL for running tests
## Launch development server
`uvicorn main:app --reload`

## Documentation location
http://127.0.0.1:8000/redoc  
http://127.0.0.1:8000/docs

## Run tests
`schemathesis run --stateful=links --checks all http://127.0.0.1:8000/openapi.json`

or

`pytest tests.py`

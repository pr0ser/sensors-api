from typing import List
from decouple import config

from aioinflux import InfluxDBClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title='Sensors API', description='Query Ruuvitag sensor measurements.')
influx = InfluxDBClient(
    host=config('INFLUXDB_HOST'),
    port=config('INFLUXDB_PORT'),
    database=config('INFLUXDB_DB')
)
sensors = ['olohuone', 'makuuhuone', 'piha', 'jääkaappi']


class Measurements(BaseModel):
    temperature: float
    humidity: float
    air_pressure: float


class Sensor(BaseModel):
    name: str
    measurements: Measurements


async def get_measurements(sensor: str) -> Measurements:
    resp = await influx.query(
        f"""
        select last(temperature) as temperature,
        last(humidity) as humidity,
        last(pressure) as air_pressure
        from ruuvitag
        where location = '{sensor}'
        """
    )
    values = resp['results'][0]['series'][0]['values'][0]
    measurements = Measurements(
        temperature=float(values[1]),
        humidity=float(values[2]),
        air_pressure=float(values[3])
    )
    return measurements


@app.get('/sensors', response_model=List[Sensor])
async def get_sensors() -> List[Sensor]:
    sensor_list = []
    for item in sensors:
        measurements = await get_measurements(item)
        sensor = Sensor(name=item, measurements=measurements)
        sensor_list.append(sensor)
    return sensor_list


@app.get('/sensors/{sensor_name}', response_model=Sensor)
async def get_sensor(sensor_name: str) -> Sensor:
    if sensor_name not in sensors:
        raise HTTPException(status_code=422, detail=f'Sensor with name {sensor_name} not found')
    measurements = await get_measurements(sensor_name)
    sensor = Sensor(name=sensor_name, measurements=measurements)
    return sensor

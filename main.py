from asyncio import gather
from typing import List, Union

from aioinflux import InfluxDBClient
from decouple import config, Csv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title='Sensors API', description='Query Ruuvitag sensor measurements.')
influx = InfluxDBClient(
    host=config('INFLUXDB_HOST'),
    port=config('INFLUXDB_PORT'),
    database=config('INFLUXDB_DB')
)
sensors = config('SENSORS', cast=Csv(str))


class Measurements(BaseModel):
    temperature: float
    humidity: float
    air_pressure: float
    battery_voltage: float


class Sensor(BaseModel):
    name: str
    measurements: Measurements


class Message(BaseModel):
    message: str


async def get_sensor_measurements(sensor: str) -> Sensor:
    resp = await influx.query(
        f"""
        select last(temperature) as temperature,
        last(humidity) as humidity,
        last(pressure) as air_pressure,
        last(batteryVoltage) as battery_voltage
        from ruuvitag
        where location = '{sensor}'
        """
    )
    values = resp['results'][0]['series'][0]['values'][0]
    measurements = Measurements(
        temperature=float(values[1]),
        humidity=float(values[2]),
        air_pressure=float(values[3]),
        battery_voltage=float(values[4])
    )
    sensor = Sensor(name=sensor, measurements=measurements)
    return sensor


@app.get('/sensors', response_model=List[Sensor])
async def get_sensors() -> List[Sensor]:
    sensor_list = []
    results = await gather(*map(get_sensor_measurements, sensors))
    for result in results:
        sensor_list.append(result)
    return sensor_list


@app.get('/sensors/{sensor_name}', response_model=Sensor, responses={404: {"model": Message}})
async def get_sensor(sensor_name: str) -> Union[Sensor, JSONResponse]:
    if sensor_name not in sensors:
        return JSONResponse(
            status_code=404,
            content={'message': f'Sensor with name {sensor_name} not found'}
        )
    sensor = await get_sensor_measurements(sensor_name)
    return sensor

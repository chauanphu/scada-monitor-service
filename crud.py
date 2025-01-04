from db import sensor_collection
from schemas import SensorDataCreate
from models import SensorModel

def create_sensor_data(data: SensorDataCreate) -> SensorModel:
    sensor = sensor_collection.insert_one(data.model_dump())
    return sensor_collection.find_one({"_id": sensor.inserted_id})
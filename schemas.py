# app/schemas.py

from pydantic import BaseModel
from datetime import datetime

class SensorDataBase(BaseModel):
    timestamp: datetime
    voltage: float
    current: float
    power: float
    power_factor: float
    total_energy: float
    mac: str

class SensorDataCreate(SensorDataBase):
    pass

class SensorDataResponse(SensorDataBase):
    hour_on: int
    hour_off: int
    minute_on: int
    minute_off: int
    
    class Config:
        from_attributes = True
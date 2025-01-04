from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, Field
from bson import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]

class SensorModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    mac: str
    timestamp: datetime
    voltage: float
    current: float
    power: float
    power_factor: float
    total_energy: float

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}  # Ensures ObjectId is serialized to a string
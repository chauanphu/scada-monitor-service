from paho.mqtt import client as mqtt_client

from enum import Enum
import pytz
from config import MQTT_BROKER, MQTT_PORT
import re
import json
import random
from datetime import datetime
import json

from models import SensorModel
from schemas import SensorDataCreate
from crud import create_sensor_data
from redis_client import client as redis_client
from websocket import manager

local_tz = pytz.timezone('Asia/Ho_Chi_Minh')  # Or your local timezone

def get_tz_datetime(timestamp: int | None = None) -> datetime:
    if not timestamp:
        # Get current time
        return datetime.now(pytz.UTC)
    else:   
        utc_dt = datetime.fromtimestamp(timestamp, pytz.UTC)
        time = utc_dt.replace(tzinfo=pytz.FixedOffset(420))
        return time
    
class Client(mqtt_client.Client):
    def __init__(self):
        self.ID = "monitoring-" + str(random.randint(100, 999))
        super().__init__(mqtt_client.CallbackAPIVersion.VERSION2, client_id=self.ID)
        self.HOST = MQTT_BROKER
        self.PORT = MQTT_PORT
        # self.ID = "monitoring-service" + str(random.randint(0, 1000))
        print("Initiating...")
        print(f"Host: {self.HOST}, Port: {self.PORT}")
        self.ttl = 60 * 5 # 5 minutes

    def connect(self, keepalive=60):
        super().connect(self.HOST, self.PORT, keepalive)

    def handle_status(self, unit_id, payload: dict):
        # Validate and parse data
        try:
            # Parse int "time" to datetime object "timestamp"
            payload["timestamp"] = get_tz_datetime(payload["time"]).timestamp()
            payload.pop("time")
            payload["mac"] = unit_id
            sensor_data = SensorDataCreate(**payload)
            # Cache latest device
            payload = json.dumps(payload) # Convert payload to JSON string
            key = f"device:{unit_id}"
            redis_client.set(key, payload)
            # Insert data to MongoDB
            create_sensor_data(sensor_data)

        except Exception as e:
            print(f"Data validation error: {e}")
            return
        

    def handle_connection(self, unit_id: int, payload):
        pass

    ## Override
    def on_connect(self, client, userdata, flags, reason_code, properties=None):
        print(f"Connected with result code {reason_code}")
        self.subscribe("unit/+/status")
        self.subscribe("unit/+/alive")

    def on_disconnect(self, client, userdata, flags, reason_code, properties=None):
        print(f"Disconnected with result code {reason_code}")

    def on_message(self, client, userdata, message):
        try:
            topic = message.topic
            match = re.match(r"unit/(\w+)/(status|alive)", topic)
            if match:
                mac_address, _type = match.groups()
                body = message.payload.decode("utf-8")
                if _type == "status":
                    payload = json.loads(body)
                    self.handle_status(mac_address, payload)
                elif _type == "alive":
                    payload = json.loads(body)
                    self.handle_connection(mac_address, payload)
            else:
                print("Invalid topic", topic)
        except json.JSONDecodeError:
            print("Failed to decode JSON payload")
        except KeyError as e:
            print(f"Missing key in payload: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


client = Client()
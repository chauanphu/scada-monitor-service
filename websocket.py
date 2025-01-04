from typing import List
from fastapi import WebSocket
import asyncio
from redis_client import client
from schemas import SensorDataResponse

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self.lock:
            self.active_connections.append(websocket)
        print("New connection added")

    async def disconnect(self, websocket: WebSocket):
        async with self.lock:
            self.active_connections.remove(websocket)
        print("Connection removed")

    async def broadcast(self, message: str):
        async with self.lock:
            connections = list(self.active_connections)
        try:
            for connection in connections:
                await connection.send_text(message)
        except Exception as e:
            print(f"Error: {e}")

    # Broadcast device data to all connected clients every 5 seconds
    async def broadcast_data(self):
        while True:
            # Get all device data from Redis: device:mac as list of objects
            async with self.lock:
                connections = list(self.active_connections)
            if not connections:
                await asyncio.sleep(5)
                continue
            devices = client.keys("device:*")
            response: List[SensorDataResponse] = []
            for device in devices:
                device: str
                device_data = client.get(device)
                if device_data:
                    response.append(device_data)
            await self.broadcast(str(response))
            await asyncio.sleep(5)

    # Start a new thread to broadcast data
    def loop(self):
        asyncio.create_task(self.broadcast_data())
        print("Broadcasting task started.")

manager = ConnectionManager()
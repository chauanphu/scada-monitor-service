import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from mqtt_client import client
from websocket import manager
from fastapi import FastAPI

app = FastAPI()

# Start MQTT client
client.connect()
client.loop_start()

# Loop to broadcast data to all connected clients
manager.loop()

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return status.HTTP_404_NOT_FOUND

# Health-check endpoint
@app.get("/health")
async def health_check():
    return {"status": "OK", "service": "monitor-service"}

# Websocket endpoint for real-time monitoring
@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        print(f"Error: {e}")
        await manager.disconnect(websocket)
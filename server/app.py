from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from server.health import router as health_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import asyncio
import json
from datetime import datetime
from typing import Dict
import threading
from core.payment_monitor import PaymentMonitor

app = FastAPI()
app.include_router(health_router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.lock = threading.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        with self.lock:
            self.active_connections[id(websocket)] = websocket

    def disconnect(self, websocket: WebSocket):
        with self.lock:
            self.active_connections.pop(id(websocket), None)

    async def broadcast(self, message: dict):
        with self.lock:
            for connection in self.active_connections.values():
                try:
                    await connection.send_json(message)
                except:
                    self.disconnect(connection)

manager = ConnectionManager()
monitor = PaymentMonitor()

@app.get("/")
async def get_dashboard():
    return templates.TemplateResponse("dashboard.html", {"request": {}})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(1)  # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

def run_monitor():
    monitor.run()

def generate_demo_data():
    """Generate sample data for dashboard"""
    return {
        "current_balance": 25.00,
        "last_payment": {
            "amount": 5.00,
            "timestamp": datetime.now().isoformat()
        },
        "recent_transactions": [
            {
                "amount": 5.00,
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            },
            {
                "amount": 5.00,
                "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
                "status": "completed"
            }
        ],
        "history": [
            {"date": (datetime.now() - timedelta(days=i)).isoformat(), "amount": 5*i}
            for i in range(7, 0, -1)
        ],
        "anomaly_detected": False
    }

async def broadcast_updates():
    while True:
        data = generate_demo_data()  # Replace with real data from monitor
        await manager.broadcast(data)
        await asyncio.sleep(5)  # Update every 5 seconds

@app.on_event("startup")
async def startup_event():
    # Start payment monitor in background thread
    monitor_thread = threading.Thread(target=run_monitor, daemon=True)
    monitor_thread.start()
    
    # Start broadcast task
    asyncio.create_task(broadcast_updates())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
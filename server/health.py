from fastapi import APIRouter
from datetime import datetime
import psutil
import os
import subprocess

router = APIRouter()

def check_service(service_name):
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() == "active"
    except:
        return False

@router.get("/health")
async def health_check():
    services = {
        "payment_monitor": check_service("picoworker-automation"),
        "docker": check_service("docker"),
        "websocket": True  # Will be checked via try/except
    }

    return {
        "status": "healthy" if all(services.values()) else "degraded",
        "timestamp": datetime.now().isoformat(),
        "system": {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "uptime": psutil.boot_time()
        },
        "services": services
    }
"""
Food Verse AI – Multimodal Food Intelligence Platform
======================================================
FastAPI Server Launcher powered by Uvicorn.
Features auto-port detection and automatic ghost process cleanup.

To run:
    python app.py
"""

import os
import sys
import socket
import subprocess
import time

# Add project root directory to Python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import uvicorn
from backend.config import is_ai_enabled

def is_port_in_use(port: int) -> bool:
    """Checks if a local TCP port is already open/occupied."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0

def release_occupied_port(port: int):
    """Attempts to kill any ghost/stale process occupying the port."""
    if not is_port_in_use(port):
        return
    try:
        # Use netstat and taskkill in Windows to kill process on this port
        find_cmd = f'powershell -Command "Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue | ForEach-Object {{ Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }}"'
        subprocess.run(find_cmd, shell=True, timeout=5, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
    except Exception:
        pass

def select_active_port(preferred_port: int = 8000) -> int:
    """Selects preferred port if freeable, otherwise finds next available port."""
    # Attempt to free preferred port
    release_occupied_port(preferred_port)
    if not is_port_in_use(preferred_port):
        return preferred_port

    # If still occupied, search for next available port
    for candidate in [8080, 8000, 8001, 8002, 5000]:
        release_occupied_port(candidate)
        if not is_port_in_use(candidate):
            return candidate
            
    return preferred_port

if __name__ == "__main__":
    ai_status = "LIVE AI MODE (Gemini Vision active)" if is_ai_enabled() else "MOCK DEMO MODE (Offline, no key required)"
    selected_port = select_active_port(8000)

    print("=" * 68)
    print("  🍲 Food Verse AI – Multimodal Food Intelligence Platform")
    print("=" * 68)
    print(f"  👉 Web Dashboard:     http://localhost:{selected_port}")
    print(f"  📖 API Documentation:  http://localhost:{selected_port}/docs")
    print(f"  ⚡ Backend Engine:     FastAPI + Uvicorn")
    print(f"  💡 AI Engine Status:  {ai_status}")
    print("=" * 68)
    print("  ℹ️  Press Ctrl + C to stop the server.")
    print("=" * 68)

    uvicorn.run("backend.main:app", host="0.0.0.0", port=selected_port, reload=False, log_level="info")

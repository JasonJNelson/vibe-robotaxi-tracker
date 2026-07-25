import asyncio
import websockets
import json
import random
import time
from datetime import datetime

vehicles = [
    {"id": "ZOX-LV-042", "provider": "Zoox", "status": "Active", "lat": 36.1147, "lng": -115.1728, "location": "Las Vegas Strip (Bellagio)", "last_updated": "Just now", "speed": 28, "trips": 312},
    {"id": "ZOX-LV-019", "provider": "Zoox", "status": "Charging", "lat": 36.0801, "lng": -115.1534, "location": "Harry Reid Airport Hub", "last_updated": "9 min ago", "speed": 0, "trips": 421},
    {"id": "ZOX-LV-023", "provider": "Zoox", "status": "Idle", "lat": 36.1953, "lng": -115.1214, "location": "North Las Vegas", "last_updated": "14 min ago", "speed": 0, "trips": 267},
    {"id": "ZOX-LV-066", "provider": "Zoox", "status": "Charging", "lat": 36.1584, "lng": -115.1452, "location": "Downtown Charging Station", "last_updated": "31 min ago", "speed": 0, "trips": 503},
    {"id": "ZOX-LV-078", "provider": "Zoox", "status": "Idle", "lat": 36.1402, "lng": -115.1321, "location": "Arts District", "last_updated": "22 min ago", "speed": 0, "trips": 76},
    {"id": "ZOX-LV-091", "provider": "Zoox", "status": "Active", "lat": 36.1523, "lng": -115.1498, "location": "Downtown Core", "last_updated": "Just now", "speed": 35, "trips": 142},
    {"id": "WAY-LV-007", "provider": "Waymo", "status": "Active", "lat": 36.1699, "lng": -115.1398, "location": "Downtown Fremont", "last_updated": "2 min ago", "speed": 22, "trips": 189},
    {"id": "WAY-LV-055", "provider": "Waymo", "status": "Active", "lat": 36.1335, "lng": -115.1649, "location": "The Sphere Area", "last_updated": "Just now", "speed": 31, "trips": 98},
    {"id": "WAY-LV-031", "provider": "Waymo", "status": "Active", "lat": 36.1028, "lng": -115.1812, "location": "Mandalay Bay", "last_updated": "4 min ago", "speed": 29, "trips": 154},
    {"id": "WAY-LV-014", "provider": "Waymo", "status": "Active", "lat": 36.1219, "lng": -115.1683, "location": "Planet Hollywood", "last_updated": "Just now", "speed": 18, "trips": 211},
    {"id": "WAY-LV-003", "provider": "Waymo", "status": "Active", "lat": 36.1758, "lng": -115.1187, "location": "Stratosphere Area", "last_updated": "6 min ago", "speed": 24, "trips": 389},
    {"id": "WAY-LV-112", "provider": "Waymo", "status": "Active", "lat": 36.0876, "lng": -115.1623, "location": "Near Airport", "last_updated": "3 min ago", "speed": 27, "trips": 267},
    {"id": "CYB-LV-001", "provider": "Cybercab", "status": "Active", "lat": 36.1205, "lng": -115.1752, "location": "Las Vegas Strip (Caesars)", "last_updated": "Just now", "speed": 32, "trips": 87},
    {"id": "CYB-LV-008", "provider": "Cybercab", "status": "Active", "lat": 36.1628, "lng": -115.1423, "location": "Downtown Las Vegas", "last_updated": "4 min ago", "speed": 19, "trips": 134},
    {"id": "CYB-LV-015", "provider": "Cybercab", "status": "Idle", "lat": 36.0854, "lng": -115.1489, "location": "Near Harry Reid Airport", "last_updated": "18 min ago", "speed": 0, "trips": 56},
    {"id": "CYB-LV-022", "provider": "Cybercab", "status": "Active", "lat": 36.1452, "lng": -115.1556, "location": "Arts District", "last_updated": "Just now", "speed": 27, "trips": 92}
]

async def handler(websocket):
    print("Client connected")
    try:
        while True:
            if random.random() < 0.7:
                vehicle = random.choice(vehicles)
                update = {
                    "type": "vehicle_update",
                    "id": vehicle["id"],
                    "lat": vehicle["lat"] + (random.random() - 0.5) * 0.005,
                    "lng": vehicle["lng"] + (random.random() - 0.5) * 0.005,
                    "speed": max(0, min(45, vehicle["speed"] + (random.random() - 0.5) * 8)) if vehicle["status"] == "Active" else 0,
                    "last_updated": "Just now",
                    "trips": vehicle["trips"] + (1 if random.random() < 0.3 else 0)
                }
                await websocket.send(json.dumps(update))
                for v in vehicles:
                    if v["id"] == vehicle["id"]:
                        v.update(update)
                        break
            await asyncio.sleep(3 + random.random() * 4)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(handler, "localhost", 8080):
        print("WebSocket server running on ws://localhost:8080")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

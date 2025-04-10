import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Optional

app = FastAPI()

# In-memory storage (in place of a database)
fake_db = {}

# Enum for device types
class deviceType(str):
    thermometer = "thermometer"
    humidity_sensor = "humidity_sensor"
    smart_light = "smart_light"
    camera = "camera"
    smart_doorbell = "smart_doorbell"

# Pydantic model to represent device data
class device(BaseModel):
    device_id: int
    name: str
    device_type: deviceType
    area: Optional[float] = None  # Optional area in square meters

    # Validator to ensure that the device type is one of the valid types
    @validator("device_type")
    def check_device_type(cls, value):
        if value not in [deviceType.thermometer, deviceType.humidity_sensor, deviceType.smart_light, deviceType.camera, deviceType.smart_doorbell]:
            raise ValueError("device type must be one of: 'thermometer', 'humidity_sensor', 'smart_light', 'camera', or 'smart_doorbell'")
        return value

# Pydantic model for the response of a single device
class deviceResponse(BaseModel):
    device_id: int
    name: str
    device_type: deviceType
    area: Optional[float] = None

    class Config:
        orm_mode = True

# Load the stub devices from the JSON file
with open("devices_stub.json") as f:
    devices_data = json.load(f)

# Initialize fake_db with stub devices
fake_db = {device['device_id']: device for device in devices_data['devices']}

# CRUD Operations

# Create a new device
@app.post("/devices/", response_model=deviceResponse)
async def create_device(device: device):
    if device.device_id in fake_db:
        raise HTTPException(status_code=400, detail="device ID already exists")
    fake_db[device.device_id] = device
    return device

# Read a device by device_id
@app.get("/devices/{device_id}", response_model=deviceResponse)
async def read_device(device_id: int):
    if device_id not in fake_db:
        raise HTTPException(status_code=404, detail="device not found")
    return fake_db[device_id]

# Read all devices
@app.get("/devices/", response_model=List[deviceResponse])
async def read_all_devices():
    return list(fake_db.values())

# Update a device by device_id
@app.put("/devices/{device_id}", response_model=deviceResponse)
async def update_device(device_id: int, device: device):
    if device_id not in fake_db:
        raise HTTPException(status_code=404, detail="device not found")
    # Update the device data
    fake_db[device_id] = device
    return device

# Delete a device by device_id
@app.delete("/devices/{device_id}")
async def delete_device(device_id: int):
    if device_id not in fake_db:
        raise HTTPException(status_code=404, detail="device not found")
    del fake_db[device_id]
    return {"message": "device deleted successfully"}

# Error handling for invalid device type
@app.exception_handler(ValueError)
async def validation_exception_handler(request, exc: ValueError):
    return HTTPException(status_code=400, detail=str(exc))

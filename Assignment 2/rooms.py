from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Optional

app = FastAPI()

# In-memory storage (in place of a database)
fake_db = {}

# Enum for room types
class RoomType(str):
    living_room = "living_room"
    kitchen = "kitchen"
    bedroom = "bedroom"
    bathroom = "bathroom"
    office = "office"

# Pydantic model to represent room data
class Room(BaseModel):
    room_id: int
    name: str
    room_type: RoomType
    area: Optional[float] = None  # Optional area in square meters

    # Validator to ensure that the room type is one of the valid types
    @validator("room_type")
    def check_room_type(cls, value):
        if value not in [RoomType.living_room, RoomType.kitchen, RoomType.bedroom, RoomType.bathroom, RoomType.office]:
            raise ValueError("Room type must be one of: 'living_room', 'kitchen', 'bedroom', 'bathroom', or 'office'")
        return value

# Pydantic model for the response of a single room
class RoomResponse(BaseModel):
    room_id: int
    name: str
    room_type: RoomType
    area: Optional[float] = None

    class Config:
        orm_mode = True

# CRUD Operations

# Create a new room
@app.post("/rooms/", response_model=RoomResponse)
async def create_room(room: Room):
    if room.room_id in fake_db:
        raise HTTPException(status_code=400, detail="Room ID already exists")
    fake_db[room.room_id] = room
    return room

# Read a room by room_id
@app.get("/rooms/{room_id}", response_model=RoomResponse)
async def read_room(room_id: int):
    if room_id not in fake_db:
        raise HTTPException(status_code=404, detail="Room not found")
    return fake_db[room_id]

# Read all rooms
@app.get("/rooms/", response_model=List[RoomResponse])
async def read_all_rooms():
    return list(fake_db.values())

# Update a room by room_id
@app.put("/rooms/{room_id}", response_model=RoomResponse)
async def update_room(room_id: int, room: Room):
    if room_id not in fake_db:
        raise HTTPException(status_code=404, detail="Room not found")
    # Update the room data
    fake_db[room_id] = room
    return room

# Delete a room by room_id
@app.delete("/rooms/{room_id}")
async def delete_room(room_id: int):
    if room_id not in fake_db:
        raise HTTPException(status_code=404, detail="Room not found")
    del fake_db[room_id]
    return {"message": "Room deleted successfully"}

# Error handling for invalid room type
@app.exception_handler(ValueError)
async def validation_exception_handler(request, exc: ValueError):
    return HTTPException(status_code=400, detail=str(exc))

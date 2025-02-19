from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, validator
from typing import List, Optional

app = FastAPI()

# In-memory storage (in place of a database)
fake_db = {}


# Pydantic model to represent house data
class House(BaseModel):
    house_id: int
    name: str
    address: Optional[str] = None

   from pydantic import BaseModel, validator, ValidationError
from typing import Optional
import re

# Pydantic Model for Address
class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: Optional[str] = None  # Optional, but if provided, should be valid

    # Validator for address fields
    @validator("street", "city", "country")
    def not_empty(cls, value, field):
        if not value or value.strip() == "":
            raise ValueError(f"{field.name.capitalize()} cannot be empty")
        return value

    # Validator for zip_code (if it's provided)
    @validator("zip_code")
    def validate_zip_code(cls, value):
        if value:
            # Basic US zip code validation (5 digits)
            zip_code_pattern = r"^\d{5}$"
            if not re.match(zip_code_pattern, value):
                raise ValueError("Zip code must be a 5-digit number")
        return value

# Pydantic model for User that includes an address
class UserWithAddress(BaseModel):
    user_id: int
    name: str
    address: Address  # Nested Address model

    class Config:
        orm_mode = True

# Example of how you would use this in your FastAPI app

from fastapi import FastAPI, HTTPException

app = FastAPI()

fake_db = {}

# Create a user with an address
@app.post("/users/")
async def create_user(user: UserWithAddress):
    if user.user_id in fake_db:
        raise HTTPException(status_code=400, detail="User ID already exists")
    fake_db[user.user_id] = user
    return user

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    return fake_db[user_id]


# Pydantic model for the response of a single house
class HouseResponse(BaseModel):
    house_id: int
    name: str
    role: Role
    email: Optional[str] = None

    class Config:
        orm_mode = True

# CRUD Operations

# Create a new house
@app.post("/houses/", response_model=HouseResponse)
async def create_house(house: House):
    if house.house_id in fake_db:
        raise HTTPException(status_code=400, detail="House ID already exists")
    fake_db[house.house_id] = house
    return house

# Read a house by house_id
@app.get("/houses/{house_id}", response_model=HouseResponse)
async def read_house(house_id: int):
    if house_id not in fake_db:
        raise HTTPException(status_code=404, detail="house not found")
    return fake_db[house_id]

# Read all houses
@app.get("/houses/", response_model=List[HouseResponse])
async def read_all_houses():
    return list(fake_db.values())

# Update a house by house_id
@app.put("/houses/{house_id}", response_model=HouseResponse)
async def update_house(house_id: int, house: House):
    if house_id not in fake_db:
        raise HTTPException(status_code=404, detail="house not found")
    # Update the house data
    fake_db[house_id] = house
    return house

# Delete a house by house_id
@app.delete("/houses/{house_id}")
async def delete_house(house_id: int):
    if house_id not in fake_db:
        raise HTTPException(status_code=404, detail="house not found")
    del fake_db[house_id]
    return {"message": "house deleted successfully"}


import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Optional

app = FastAPI()

# In-memory storage (in place of a database)
fake_db = {}

# Load the stub data
with open("houses_users_stub.json") as f:
    data = json.load(f)
    # Populate fake_db with houses and users data
    for house in data["houses"]:
        fake_db[house["house_id"]] = house
    for user in data["users"]:
        fake_db[user["user_id"]] = user


# Pydantic model to represent house data
class House(BaseModel):
    house_id: int
    name: str
    address: Optional[str] = None

class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: Optional[str] = None

    @validator("street", "city", "country")
    def not_empty(cls, value, field):
        if not value or value.strip() == "":
            raise ValueError(f"{field.name.capitalize()} cannot be empty")
        return value

    @validator("zip_code")
    def validate_zip_code(cls, value):
        if value:
            zip_code_pattern = r"^\d{5}$"
            if not re.match(zip_code_pattern, value):
                raise ValueError("Zip code must be a 5-digit number")
        return value

# Create a house
@app.post("/houses/", response_model=House)
async def create_house(house: House):
    if house.house_id in fake_db:
        raise HTTPException(status_code=400, detail="House ID already exists")
    fake_db[house.house_id] = house.dict()
    return house

# Read a house by house_id
@app.get("/houses/{house_id}", response_model=House)
async def read_house(house_id: int):
    if house_id not in fake_db:
        raise HTTPException(status_code=404, detail="House not found")
    return fake_db[house_id]

# Read all houses
@app.get("/houses/", response_model=List[House])
async def read_all_houses():
    return [house for house in fake_db.values() if "house_id" in house]

# Create a user with an address
@app.post("/users/")
async def create_user(user: UserWithAddress):
    if user.user_id in fake_db:
        raise HTTPException(status_code=400, detail="User ID already exists")
    fake_db[user.user_id] = user.dict()
    return user

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    return fake_db[user_id]

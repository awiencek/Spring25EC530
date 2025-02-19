import json
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, validator
from typing import List, Optional

app = FastAPI()

# In-memory storage (in place of a database)
fake_db = {}

# Enum for user roles
class Role(str):
    admin = "admin"
    manager = "manager"
    guest = "guest"

# Pydantic model to represent user data
class User(BaseModel):
    user_id: int
    name: str
    role: Role
    email: Optional[str] = None

    # Validator to ensure that the role is one of the valid roles
    @validator("role")
    def check_role(cls, value):
        if value not in [Role.admin, Role.manager, Role.guest]:
            raise ValueError("Role must be one of: 'admin', 'manager', or 'guest'")
        return value

# Pydantic model for the response of a single user
class UserResponse(BaseModel):
    user_id: int
    name: str
    role: Role
    email: Optional[str] = None

    class Config:
        orm_mode = True

# CRUD Operations

# Create a new user
@app.post("/users/", response_model=UserResponse)
async def create_user(user: User):
    if user.user_id in fake_db:
        raise HTTPException(status_code=400, detail="User ID already exists")
    fake_db[user.user_id] = user
    return user

# Read a user by user_id
@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    return fake_db[user_id]

# Read all users
@app.get("/users/", response_model=List[UserResponse])
async def read_all_users():
    return list(fake_db.values())

# Update a user by user_id
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: User):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    # Update the user data
    fake_db[user_id] = user
    return user

# Delete a user by user_id
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    del fake_db[user_id]
    return {"message": "User deleted successfully"}

# Error handling for invalid role
@app.exception_handler(ValueError)
async def validation_exception_handler(request, exc: ValueError):
    return HTTPException(status_code=400, detail=str(exc))

import json

# Load the stub users from the JSON file
with open("users_stub.json") as f:
    users_data = json.load(f)

# In-memory storage (in place of a database)
fake_db = {user['user_id']: user for user in users_data}


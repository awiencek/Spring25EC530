from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory storage for messages (simulating a basic message store)
messages = []

# Pydantic model for handling message data
class Message(BaseModel):
    sender: str
    message: str

@app.post("/send_message")
async def send_message(msg: Message):
    """API endpoint to send a message"""
    messages.append(msg.dict())  # Save message to the list
    return {"status": "Message sent successfully!"}

@app.get("/get_messages", response_model=List[Message])
async def get_messages():
    """API endpoint to get all messages"""
    return messages

if __name__ == "__main__":
    # Run the server using Uvicorn (not needed here since it's run separately)
    import os
    os.system("uvicorn server:app --reload")

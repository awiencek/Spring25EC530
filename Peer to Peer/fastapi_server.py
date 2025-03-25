from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import mysql.connector
from mysql.connector import Error

app = FastAPI()

# MySQL Database connection setup
def get_db_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Database host (localhost in this case)
            user="root",  # Database username
            password="",  # Database password
            database="messaging_db"  # Database name (as defined earlier)
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


# Pydantic model for handling message data
class Message(BaseModel):
    sender: str
    message: str

@app.post("/send_message")
async def send_message(msg: Message):
    """API endpoint to send a message."""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()

        # Insert message into the database
        query = """
            INSERT INTO messages (sender_ip, recipient_ip, message, status) 
            VALUES (%s, %s, %s, 'sent')
        """
        # For now, we assume the recipient IP is a placeholder ('receiver_ip_here') as we don't have that info
        cursor.execute(query, (msg.sender, 'receiver_ip_here', msg.message))
        connection.commit()

        cursor.close()
        connection.close()
        return {"status": "Message sent successfully!"}
    else:
        return {"error": "Database connection failed"}

@app.get("/get_messages", response_model=List[Message])
async def get_messages(recipient_ip: str):
    """API endpoint to get all messages."""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        
        # Fetch all messages that were sent to the recipient and are marked as 'sent' (offline messages)
        query = "SELECT sender_ip AS sender, message FROM messages WHERE recipient_ip = %s AND status = 'sent'"
        cursor.execute(query, (recipient_ip,))

        # Fetch messages from the database
        rows = cursor.fetchall()

        # Convert rows to Message Pydantic models
        messages = [Message(sender=row['sender'], message=row['message']) for row in rows]

        # Mark all fetched messages as 'delivered'
        cursor.execute(
            "UPDATE messages SET status = 'delivered' WHERE recipient_ip = %s AND status = 'sent'", 
            (recipient_ip,)
        )
        connection.commit()

        cursor.close()
        connection.close()

        return messages
    else:
        return {"error": "Database connection failed"}

if __name__ == "__main__":
    # Run the server using Uvicorn (not needed here since it's run separately)
    import os
    os.system("uvicorn fastapi_server:app --reload")

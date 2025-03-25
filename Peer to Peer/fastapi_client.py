import requests

# The FastAPI server's URL (assuming it's running locally)
SERVER_URL = "http://localhost:8000"

def send_message(message, sender):
    """Send a message to the FastAPI server."""
    url = f"{SERVER_URL}/send_message"
    data = {"message": message, "sender": sender}
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print(f"Message sent successfully!")
    else:
        print(f"Failed to send message: {response.json().get('error')}")

def get_messages():
    """Retrieve all messages from the server."""
    url = f"{SERVER_URL}/get_messages"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        messages = response.json()
        print("\nMessages:")
        for msg in messages:
            print(f"{msg['sender']}: {msg['message']}")
    else:
        print("Failed to retrieve messages.")

if __name__ == "__main__":
    while True:
        action = input("Choose action - (1) Send Message (2) View Messages (3) Exit: ")

        if action == "1":
            sender = input("Your name: ")
            message = input("Enter your message: ")
            send_message(message, sender)
        elif action == "2":
            get_messages()
        elif action == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose again.")

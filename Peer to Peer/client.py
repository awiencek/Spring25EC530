import socket
import mysql.connector
from time import sleep

def start_client(server_ip, server_port):
    # Connect to MySQL Database
    db_connection = mysql.connector.connect(
        host="localhost",   # Your MySQL server
        user="root",        # Your MySQL username
        password="",        # Your MySQL password
        database="messaging_db"
    )
    db_cursor = db_connection.cursor()

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")
    
    try:
        while True:
            # Send a message to the server
            message = input("You: ")
            client_socket.send(message.encode())
            
            # Save the message to the database as 'sent'
            db_cursor.execute(
                "INSERT INTO messages (sender_ip, recipient_ip, message) VALUES (%s, %s, %s)",
                ('client_ip_here', server_ip, message)
            )
            db_connection.commit()

            if message.lower() == 'exit':
                print("Connection closed.")
                break
            
            # Receive response from the server
            response = client_socket.recv(1024).decode()
            print(f"Server: {response}")
            if response.lower() == 'exit':
                print("Connection closed.")
                break
            
            # Save the server's response to the database as 'delivered'
            db_cursor.execute(
                "INSERT INTO messages (sender_ip, recipient_ip, message, status) VALUES (%s, %s, %s, 'delivered')",
                (server_ip, 'client_ip_here', response)
            )
            db_connection.commit()

    finally:
        client_socket.close()
        db_cursor.close()
        db_connection.close()

if __name__ == "__main__":
    server_ip = "192.168.1.2"  # Replace with the server's IP address
    server_port = 12345        # Should match the server's port
    start_client(server_ip, server_port)

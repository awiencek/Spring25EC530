import socket

def start_client(server_ip, server_port):
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
            if message.lower() == 'exit':
                print("Connection closed.")
                break
            
            # Receive response from the server
            response = client_socket.recv(1024).decode()
            print(f"Server: {response}")
            if response.lower() == 'exit':
                print("Connection closed.")
                break
    finally:
        client_socket.close()

if __name__ == "__main__":
    server_ip = "192.168.1.2"  # Replace with the server's IP address
    server_port = 12345        # Should match the server's port
    start_client(server_ip, server_port)

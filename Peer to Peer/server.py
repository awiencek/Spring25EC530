
import socket

def start_server(host, port):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the server to the specified host and port
    server_socket.bind((host, port))
    
    # Listen for incoming connections (maximum 1 connection in this case)
    server_socket.listen(1)
    print(f"Listening for incoming connections on {host}:{port}...")
    
    # Accept the incoming connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    
    try:
        while True:
            # Receive message from the client
            message = client_socket.recv(1024).decode()
            if message.lower() == 'exit':
                print("Connection closed.")
                break
            print(f"Client: {message}")
            
            # Send a response back to the client
            response = input("You: ")
            client_socket.send(response.encode())
            if response.lower() == 'exit':
                print("Connection closed.")
                break
    finally:
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    local_ip = "192.168.1.2"  # Replace with your local IP address
    port = 12345  # Choose an available port
    start_server(local_ip, port)

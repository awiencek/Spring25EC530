import unittest
import socket
from server import start_server

class TestServer(unittest.TestCase):
    
    def setUp(self):
        # Start the server on a random port (e.g., 12345)
        self.server_ip = "127.0.0.1"
        self.port = 12345
        self.server = start_server(self.server_ip, self.port)
        
    def test_server_can_listen(self):
        # Check if server is listening on the specified port
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = server_socket.connect_ex((self.server_ip, self.port))
        self.assertEqual(result, 0, "Server is not listening.")
    
    def test_server_message_handling(self):
        # Test message handling by server
        # Assume a message can be sent and received back from the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_ip, self.port))
        test_message = "Hello, Server!"
        client_socket.send(test_message.encode())
        response = client_socket.recv(1024).decode()
        self.assertEqual(response, "Goodbye!", "Server did not respond as expected.")
        client_socket.close()

if __name__ == "__main__":
    unittest.main()

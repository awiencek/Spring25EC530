import unittest
from unittest.mock import patch, MagicMock
from client import start_client
import socket

class TestClient(unittest.TestCase):
    
    @patch("client.mysql.connector.connect")
    @patch("client.socket.socket")
    def test_client_connection(self, mock_socket, mock_db_connection):
        # Mocking database connection
        mock_cursor = MagicMock()
        mock_db_connection.cursor.return_value = mock_cursor
        
        # Mocking socket connection
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        
        server_ip = "127.0.0.1"
        server_port = 12345
        
        # Simulating connection
        start_client(server_ip, server_port)
        
        # Test database query call for unread messages
        mock_cursor.execute.assert_called_with(
            "SELECT message, timestamp FROM messages WHERE recipient_ip = %s AND status = 'sent'",
            ('client_ip_here',)
        )
        
        # Test socket connection
        mock_socket_instance.connect.assert_called_with((server_ip, server_port))
        
    @patch("client.mysql.connector.connect")
    @patch("client.socket.socket")
    def test_send_message(self, mock_socket, mock_db_connection):
        # Mocking database connection
        mock_cursor = MagicMock()
        mock_db_connection.cursor.return_value = mock_cursor
        
        # Mocking socket connection
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        
        # Simulate user sending a message
        server_ip = "127.0.0.1"
        server_port = 12345
        start_client(server_ip, server_port)
        
        test_message = "Test Message"
        mock_socket_instance.send.assert_called_with(test_message.encode())
        
        # Check if the message is inserted into the database
        mock_cursor.execute.assert_called_with(
            "INSERT INTO messages (sender_ip, recipient_ip, message) VALUES (%s, %s, %s)",
            ('client_ip_here', server_ip, test_message)
        )

if __name__ == "__main__":
    unittest.main()

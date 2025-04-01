import unittest
from fastapi.testclient import TestClient
from fastapi_server import app

class TestFastAPIServer(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)

    def test_send_message(self):
        # Test sending a message
        response = self.client.post(
            "/send_message",
            json={"message": "Hello FastAPI", "sender": "sender_ip_here"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())

    def test_get_messages(self):
        # Test getting messages
        response = self.client.get("/get_messages?recipient_ip=client_ip_here")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertGreater(len(response.json()), 0)

if __name__ == "__main__":
    unittest.main()

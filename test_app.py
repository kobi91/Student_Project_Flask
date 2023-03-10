import unittest
import json
from flask import Flask

class FlaskTestApp(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client()
        
    def test_wrong_login(self):
        response = self.client.post("/user_login", data={'username': 'koko', 'password': '5555'})
        assert response.status_code == 404
          
if __name__ == "__main__":
    unittest.main()
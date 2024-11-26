import unittest
from flask import Flask
from files.user_auth import app, IntermediateServer  

class TestAuthenticationEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()  # Cliente de prueba de Flask
        cls.client.testing = True

    def test_login_success(self):
        # Prueba con credenciales válidas
        valid_credentials = {
            "username": "user1",
            "password": "password123"
        }
        response = self.client.post('/login', json=valid_credentials)
        self.assertEqual(response.status_code, 200)
        json_response = response.get_json()
        self.assertEqual(json_response["status"], "Login successful")

    def test_login_failure(self):
        # Prueba con credenciales inválidas
        invalid_credentials = {
            "username": "user1",
            "password": "wrong_password"
        }
        response = self.client.post('/login', json=invalid_credentials)
        self.assertEqual(response.status_code, 401)
        json_response = response.get_json()
        self.assertEqual(json_response["status"], "Login failed")

    def test_access_model_success(self):
        # Prueba de autorización con permisos válidos
        valid_request = {
            "username": "user2",
            "model_id": "model3"
        }
        response = self.client.post('/access_model', json=valid_request)
        self.assertEqual(response.status_code, 200)
        json_response = response.get_json()
        self.assertEqual(json_response["status"], "Access granted")
        self.assertEqual(json_response["model_id"], "model3")

    def test_access_model_failure(self):
        # Prueba de autorización con permisos no válidos
        invalid_request = {
            "username": "user1",
            "model_id": "model3"
        }
        response = self.client.post('/access_model', json=invalid_request)
        self.assertEqual(response.status_code, 200)
        json_response = response.get_json()
        self.assertEqual(json_response["status"], "Access denied")
        self.assertEqual(json_response["reason"], "Unauthorized")

    def test_authenticate_user(self):
        # Prueba directa de la función de autenticación
        server = IntermediateServer()
        self.assertTrue(server.authenticate_user("user1", "password123"))
        self.assertFalse(server.authenticate_user("user1", "wrong_password"))
        self.assertFalse(server.authenticate_user("nonexistent_user", "password"))

    def test_authorize_user(self):
        # Prueba directa de la función de autorización
        server = IntermediateServer()
        self.assertEqual(
            server.authorize_user("user2", "model2"),
            {"status": "Access granted", "model_id": "model2"}
        )
        self.assertEqual(
            server.authorize_user("user1", "model3"),
            {"status": "Access denied", "reason": "Unauthorized"}
        )

if __name__ == '__main__':
    unittest.main()

import unittest
from flask import Flask
from files.model_submission import app, IntermediateServer, HPCCluster  # Reemplaza 'your_module_name' por el nombre del archivo de tu código original

class TestIntermediateServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Crear una instancia de la aplicación Flask para usar el test client
        cls.client = app.test_client()
        cls.client.testing = True

    def test_submit_model_success(self):
        # Datos válidos para el test
        valid_model_data = {
            "structure": "some_structure",
            "elements": "some_elements"
        }
        
        # Enviar la solicitud POST al endpoint '/submit_model'
        response = self.client.post('/submit_model', json=valid_model_data)
        
        # Verificar el estado de la respuesta
        self.assertEqual(response.status_code, 200)
        json_response = response.get_json()
        self.assertEqual(json_response["status"], "Processing started")
        self.assertIn("processing_id", json_response)

    def test_submit_model_failure(self):
        # Datos inválidos para el test (faltan 'structure' o 'elements')
        invalid_model_data = {
            "structure": "some_structure"
        }
        
        # Enviar la solicitud POST al endpoint '/submit_model'
        response = self.client.post('/submit_model', json=invalid_model_data)
        
        # Verificar el estado de la respuesta
        self.assertEqual(response.status_code, 200)
        json_response = response.get_json()
        self.assertEqual(json_response["status"], "Validation failed")
        self.assertEqual(json_response["error"], "Invalid model format")

    def test_receive_model_valid_data(self):
        # Crear una instancia del servidor intermedio
        server = IntermediateServer()
        model_data = {
            "structure": "valid_structure",
            "elements": "valid_elements"
        }
        
        # Verificar que el método 'receive_model' devuelve el resultado correcto
        result = server.receive_model(model_data)
        self.assertEqual(result["status"], "Processing started")
        self.assertEqual(result["processing_id"], "unique_processing_id_12345")

    def test_receive_model_invalid_data(self):
        # Crear una instancia del servidor intermedio
        server = IntermediateServer()
        invalid_model_data = {
            "structure": "valid_structure"
        }
        
        # Verificar que el método 'receive_model' maneja los datos incorrectos
        result = server.receive_model(invalid_model_data)
        self.assertEqual(result["status"], "Validation failed")
        self.assertEqual(result["error"], "Invalid model format")

if __name__ == '__main__':
    unittest.main()

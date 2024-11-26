# Additional endpoints for authentication
from flask import Flask, request, jsonify

app = Flask(__name__)

class IntermediateServer:
    def __init__(self):
        self.user_data_store = {"user1": "password123", "user2": "password456"}
        self.user_permissions = {"user1": ["model1"], "user2": ["model2", "model3"]}

    def authenticate_user(self, username, password):
        return username in self.user_data_store and self.user_data_store[username] == password

    def authorize_user(self, username, model_id):
        if model_id in self.user_permissions.get(username, []):
            return {"status": "Access granted", "model_id": model_id}
        return {"status": "Access denied", "reason": "Unauthorized"}

intermediate_server = IntermediateServer()

@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()
    username, password = credentials.get('username'), credentials.get('password')
    if intermediate_server.authenticate_user(username, password):
        return jsonify({"status": "Login successful"})
    else:
        return jsonify({"status": "Login failed"}), 401

@app.route('/access_model', methods=['POST'])
def access_model():
    data = request.get_json()
    username, model_id = data.get('username'), data.get('model_id')
    result = intermediate_server.authorize_user(username, model_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

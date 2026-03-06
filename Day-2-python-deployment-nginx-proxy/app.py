from flask import Flask, jsonify, request

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "Welcome to the Flask Application!"

# API route
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Flask API"})

# POST example
@app.route('/api/add', methods=['POST'])
def add_numbers():
    data = request.get_json()
    num1 = data.get("num1")
    num2 = data.get("num2")

    result = num1 + num2
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

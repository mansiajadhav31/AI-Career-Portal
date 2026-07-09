from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"status": "ok", "message": "Backend running!"})

@app.route('/api/upload-resume', methods=['POST'])
def upload():
    return jsonify({"success": True, "match_score": 85})

@app.route('/api/login', methods=['POST'])
def login():
    return jsonify({"token": "test123"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
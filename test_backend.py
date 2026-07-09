from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'status': 'ok', 'message': 'Backend is working!'})

@app.route('/api/upload-resume', methods=['POST', 'OPTIONS'])
def upload():
    if request.method == 'OPTIONS':
        return '', 200
    
    print("📤 Upload received!")
    
    if 'resume' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['resume']
    print(f"File: {file.filename}")
    
    return jsonify({
        'success': True,
        'message': 'Upload successful!',
        'match_score': 85,
        'matched_skills': ['Python', 'Django', 'SQL']
    }), 200

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.json
    print(f"Login: {data.get('email')}")
    
    return jsonify({
        'token': 'test-token-123',
        'user': {'id': 1, 'name': 'Test User', 'email': data.get('email')}
    }), 200

@app.route('/api/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({'message': 'Registered!'}), 201

@app.route('/api/dashboard/stats', methods=['GET'])
def stats():
    return jsonify({
        'resume_score': 75,
        'total_interviews': 3,
        'total_coding_challenges': 5,
        'interview_scores': [70, 80, 85],
        'coding_scores': [65, 75, 80]
    }), 200

@app.route('/api/user/resumes', methods=['GET'])
def resumes():
    return jsonify({
        'resumes': [
            {'id': 1, 'file_path': 'resume1.pdf', 'match_score': 85, 'uploaded_at': '2026-05-20'},
            {'id': 2, 'file_path': 'resume2.pdf', 'match_score': 72, 'uploaded_at': '2026-05-25'}
        ]
    }), 200

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Test Backend Running")
    print("📍 http://localhost:5000")
    print("📡 Test: http://localhost:5000/api/test")
    print("=" * 50)
    app.run(debug=True, port=5000)
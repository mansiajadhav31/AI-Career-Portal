import os
from datetime import timedelta
import json
from werkzeug.utils import secure_filename

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Local imports - WITHOUT 'backend.' prefix (कारण आपण backend folder मध्येच आहोत)
from database import get_db_connection, init_database
from auth import register_user, authenticate_user, get_user_profile
from resume_matcher import extract_resume_text, calculate_match_score
from interview_ai import generate_interview_questions, evaluate_answers
from coding_questions import get_coding_questions, evaluate_code

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

jwt = JWTManager(app)

# Initialize database on startup
init_database()

# ============ STATIC ROUTES ============
@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

# ============ AUTH ROUTES ============
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    if not name or not email or not password:
        return jsonify({'error': 'All fields required'}), 400
    
    result = register_user(name, email, password)
    if result['success']:
        return jsonify({'message': result['message']}), 201
    else:
        return jsonify({'error': result['message']}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    user = authenticate_user(email, password)
    if user:
        access_token = create_access_token(identity=user['id'])
        return jsonify({
            'token': access_token,
            'user': user,
            'message': 'Login successful'
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    profile = get_user_profile(user_id)
    if profile:
        return jsonify(profile), 200
    return jsonify({'error': 'User not found'}), 404

# ============ RESUME ROUTES ============
@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    print("=" * 50)
    print("📤 UPLOAD REQUEST RECEIVED")
    
    # Temporary hardcoded user_id for testing
    user_id = 1
    
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['resume']
    job_description = request.form.get('job_description', '')
    
    print(f"📄 File: {file.filename}")
    print(f"📝 Job Desc: {job_description[:100] if job_description else 'None'}")
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are supported'}), 400
    
    try:
        filename = secure_filename(f"{user_id}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"💾 Saved: {filepath}")
        
        # Extract text and calculate score
        resume_text = extract_resume_text(filepath)
        print(f"📝 Text length: {len(resume_text)}")
        
        match_score, matched_skills = calculate_match_score(resume_text, job_description)
        print(f"🎯 Score: {match_score}%")
        print(f"✅ Skills: {matched_skills}")
        
        # Store in database
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO resumes (user_id, file_path, match_score) 
                    VALUES (%s, %s, %s)
                ''', (user_id, filepath, match_score))
                conn.commit()
                cursor.close()
                conn.close()
        except Exception as db_err:
            print(f"DB Error: {db_err}")
        
        # Clean up
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'message': 'Resume uploaded successfully',
            'match_score': match_score,
            'matched_skills': matched_skills,
            'filename': file.filename
        }), 200
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/match-score', methods=['POST'])
@jwt_required()
def get_match_score():
    data = request.json
    resume_text = data.get('resume_text', '')
    job_description = data.get('job_description', '')
    
    score, matched_skills = calculate_match_score(resume_text, job_description)
    
    return jsonify({
        'match_score': score,
        'matched_skills': matched_skills
    }), 200

# ============ DASHBOARD ROUTES ============
@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    # Temporary hardcoded - JWT काढल्यामुळे
    user_id = 1
    print(f"📊 Getting stats for user: {user_id}")
    
    resume_score = 0
    interview_count = 0
    coding_count = 0
    
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT match_score FROM resumes WHERE user_id = %s ORDER BY id DESC LIMIT 1', (user_id,))
            row = cursor.fetchone()
            resume_score = row[0] if row and row[0] else 0
            
            cursor.execute('SELECT COUNT(*) FROM interview_sessions WHERE user_id = %s', (user_id,))
            row = cursor.fetchone()
            interview_count = row[0] if row else 0
            
            cursor.execute('SELECT COUNT(*) FROM coding_submissions WHERE user_id = %s', (user_id,))
            row = cursor.fetchone()
            coding_count = row[0] if row else 0
            
            cursor.close()
            conn.close()
            
        print(f"✅ Stats: resume={resume_score}, interviews={interview_count}, coding={coding_count}")
        
    except Exception as e:
        print(f"❌ Stats error: {e}")
    
    return jsonify({
        'resume_score': resume_score,
        'interview_scores': [],
        'coding_scores': [],
        'total_interviews': interview_count,
        'total_coding_challenges': coding_count
    }), 200
@app.route('/api/user/resumes', methods=['GET'])
def get_user_resumes():
    # Temporary hardcoded - JWT काढल्यामुळे
    user_id = 1
    print(f"📋 Getting resumes for user: {user_id}")
    
    try:
        conn = get_db_connection()
        if not conn:
            print("❌ Database connection failed")
            return jsonify({'resumes': []}), 200
        
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, file_path, match_score, uploaded_at 
            FROM resumes 
            WHERE user_id = %s 
            ORDER BY id DESC
        ''', (user_id,))
        
        rows = cursor.fetchall()
        print(f"🔍 Found {len(rows)} resumes")
        
        resumes = []
        for row in rows:
            file_path = row[1] if row[1] else 'unknown.pdf'
            if '\\' in file_path:
                file_path = file_path.split('\\')[-1]
            if file_path.startswith(f"{user_id}_"):
                file_path = file_path[len(str(user_id)) + 1:]
            
            resumes.append({
                'id': row[0],
                'file_path': file_path,
                'match_score': row[2] if row[2] else 0,
                'uploaded_at': str(row[3]) if row[3] else None
            })
        
        cursor.close()
        conn.close()
        
        print(f"✅ Returning {len(resumes)} resumes")
        return jsonify({'resumes': resumes}), 200
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'resumes': []}), 200

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 AI Career Portal Backend Running")
    print("📍 http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
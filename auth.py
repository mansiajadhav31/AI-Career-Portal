from flask_bcrypt import Bcrypt
from database import get_db_connection

bcrypt = Bcrypt()

def register_user(name, email, password):
    conn = get_db_connection()
    if not conn:
        return {'success': False, 'message': 'Database connection failed'}
    
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute('SELECT id FROM users WHERE email = %s', (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return {'success': False, 'message': 'Email already registered'}
    
    # Hash password
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # Insert user
    cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)',
                   (name, email, hashed))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return {'success': True, 'message': 'Registration successful'}

def authenticate_user(email, password):
    conn = get_db_connection()
    if not conn:
        return None
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, name, email, password FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if user and bcrypt.check_password_hash(user['password'], password):
        return {
            'id': user['id'],
            'name': user['name'],
            'email': user['email']
        }
    return None

def get_user_profile(user_id):
    conn = get_db_connection()
    if not conn:
        return None
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, name, email, created_at FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return user
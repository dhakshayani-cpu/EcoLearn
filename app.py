from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
CORS(app)

# File to store users persistently
USERS_FILE = 'users.json'

# Configure file uploads
UPLOAD_FOLDER = 'challenge_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Store challenge submissions
challenge_submissions = []

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

# Load existing users or create demo users
users = load_users()

# Add demo users if no users exist
if not users:
    users = [
        {
            'id': 1,
            'name': 'Demo Student',
            'email': 'student@demo.com', 
            'password': 'demo123',  # Added password field
            'role': 'student',
            'school': 'Green Valley High School',
            'eco_points': 150
        },
        {
            'id': 2,
            'name': 'Demo Teacher',
            'email': 'teacher@demo.com',
            'password': 'demo123',  # Added password field
            'role': 'teacher', 
            'school': 'Eco Warriors Academy',
            'eco_points': 0
        }
    ]
    save_users(users)
    print("Created demo users")

print(f"Loaded {len(users)} users")
for user in users:
    print(f"  - {user['email']}")

@app.route('/')
def home():
    return jsonify({
        "message": "EcoLearn Backend is running!", 
        "users_count": len(users),
        "storage": "Persistent JSON storage",
        "challenge_uploads": len(challenge_submissions)
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print(f"📝 Registration attempt for: {data['email']}")
        
        # Check if user already exists
        if any(user['email'] == data['email'] for user in users):
            return jsonify({
                'success': False,
                'message': 'User already exists with this email'
            }), 400
        
        # Create new user
        new_user = {
            'id': len(users) + 1,
            'name': data['name'],
            'email': data['email'],
            'password': data['password'],  # Store password
            'role': data['role'],
            'school': data.get('school', 'Not specified'),
            'eco_points': 0
        }
        
        users.append(new_user)
        save_users(users)  # Save to file
        
        print(f"✅ New user registered: {new_user['email']}. Total users: {len(users)}")
        
        return jsonify({
            'success': True,
            'message': 'Registration successful!',
            'user': {k: v for k, v in new_user.items() if k != 'password'},  # Don't send password back
            'token': f"token-{new_user['id']}"
        })
        
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Registration error: {str(e)}'
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        
        print(f"🔐 Login attempt for: {email}")
        print(f"📊 Checking against {len(users)} users")
        
        # Find user by email AND password
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)
        
        if user:
            print(f"✅ Login successful for: {email}")
            # Return user data without password
            user_data = {k: v for k, v in user.items() if k != 'password'}
            return jsonify({
                'success': True,
                'message': 'Login successful!',
                'user': user_data,
                'token': f"token-{user['id']}"
            })
        else:
            print(f"❌ Login failed for: {email}")
            # More specific error message
            email_exists = any(u['email'] == email for u in users)
            if email_exists:
                return jsonify({
                    'success': False,
                    'message': 'Invalid password'
                }), 401
            else:
                return jsonify({
                    'success': False,
                    'message': 'User not found'
                }), 401
            
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Login error: {str(e)}'
        }), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    # Return users without passwords
    safe_users = [{k: v for k, v in user.items() if k != 'password'} for user in users]
    return jsonify({
        'success': True,
        'users': safe_users,
        'count': len(users)
    })

@app.route('/api/debug', methods=['GET'])
def debug():
    """Debug endpoint to see current users"""
    return jsonify({
        'users_count': len(users),
        'users': [{'email': u['email'], 'id': u['id']} for u in users],
        'storage_file': USERS_FILE,
        'file_exists': os.path.exists(USERS_FILE),
        'challenge_submissions': len(challenge_submissions)
    })

@app.route('/api/challenges', methods=['GET'])
def get_challenges():
    return jsonify({
        'success': True,
        'challenges': [
            {
                'id': 1,
                'title': 'Plant a Tree',
                'description': 'Plant a native tree species in your neighborhood or school campus.',
                'points': 50,
                'participants': 342
            },
            {
                'id': 2, 
                'title': 'Plastic-Free Day',
                'description': 'Go an entire day without using any single-use plastic items.',
                'points': 30,
                'participants': 521
            }
        ]
    })

# ==================== CHALLENGE SUBMISSIONS ====================

@app.route('/api/challenges/submit', methods=['POST'])
def submit_challenge():
    try:
        # Get form data
        challenge_id = request.form.get('challengeId')
        description = request.form.get('description')
        user_id = request.form.get('userId')
        
        print(f"📤 Challenge submission - User: {user_id}, Challenge: {challenge_id}")
        
        # Handle file upload
        file = request.files.get('evidence')
        filename = None
        
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{user_id}_{challenge_id}_{file.filename}")
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            print(f"💾 File saved: {filename}")
        
        # Create submission record
        submission = {
            'id': len(challenge_submissions) + 1,
            'challenge_id': challenge_id,
            'user_id': user_id,
            'description': description,
            'filename': filename,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        challenge_submissions.append(submission)
        print(f"✅ Submission recorded. Total submissions: {len(challenge_submissions)}")
        
        return jsonify({
            'success': True,
            'message': 'Challenge submitted successfully!',
            'submission': submission
        })
        
    except Exception as e:
        print(f"❌ Challenge submission error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Submission error: {str(e)}'
        }), 500

@app.route('/api/challenges/my-submissions', methods=['GET'])
def get_my_submissions():
    user_id = request.args.get('userId')
    user_subs = [s for s in challenge_submissions if s['user_id'] == user_id]
    return jsonify({
        'success': True,
        'submissions': user_subs
    })

@app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/debug/submissions', methods=['GET'])
def debug_submissions():
    return jsonify({
        'submissions_count': len(challenge_submissions),
        'submissions': challenge_submissions
    })

if __name__ == '__main__':
    print("=== 🌱 EcoLearn Backend Starting ===")
    print(f"📁 Persistent storage: {USERS_FILE}")
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"👥 Loaded {len(users)} users")
    print(f"📤 Challenge submissions: {len(challenge_submissions)}")
    print("🔑 Demo accounts:")
    print("   - student@demo.com / demo123")
    print("   - teacher@demo.com / demo123")
    print("🌐 Server running on: http://localhost:5000")
    print("=====================================")
    app.run(debug=True, port=5000)
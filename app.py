from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'ecolearn-super-secret-2023'
CORS(app)

print("🌱 STARTING ECOLEARN BACKEND WITH QUIZZES...")

users = []
challenges = []
lessons = []

# Sample challenges
challenges = [
    {
        'id': 1, 'title': 'Plant a Tree', 'description': 'Plant a native tree species.', 
        'category': 'biodiversity', 'points': 50, 'difficulty': 'medium', 'participants': 342,
        'is_active': True
    },
    {
        'id': 2, 'title': 'Plastic-Free Day', 'description': 'Go a day without plastic.', 
        'category': 'waste-management', 'points': 30, 'difficulty': 'easy', 'participants': 521,
        'is_active': True
    }
]

# Enhanced lessons with multiple quizzes
lessons = [
    {
        'id': 1,
        'title': 'Climate Change Fundamentals',
        'description': 'Understand the causes and effects of global warming.',
        'category': 'climate-change',
        'points': 20,
        'duration': 30,
        'is_published': True,
        'content': '''
        <div class="lesson-content">
            <h2>🌍 Climate Change Fundamentals</h2>
            
            <div class="video-container">
                <iframe width="100%" height="400" src="https://www.youtube.com/embed/G4H1N_yXBiA" 
                        frameborder="0" allowfullscreen></iframe>
            </div>
            
            <h3>Understanding Climate Change</h3>
            <p>Climate change refers to long-term shifts in temperatures and weather patterns...</p>
            
            <!-- QUIZ 1 -->
            <div class="quiz-section" style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3>📝 Quiz 1: Greenhouse Gases</h3>
                <p><strong>What is the main greenhouse gas responsible for climate change?</strong></p>
                <button class="quiz-btn correct" onclick="showAnswer(this, 'correct')" style="margin: 5px; padding: 10px; background: #2E8B57; color: white; border: none; border-radius: 5px;">Carbon Dioxide (CO2)</button>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">Oxygen</button>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">Nitrogen</button>
                <div class="answer-feedback" style="margin-top: 10px; display: none;"></div>
            </div>
            
            <!-- QUIZ 2 -->
            <div class="quiz-section" style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3>📝 Quiz 2: Climate Effects</h3>
                <p><strong>Which of these is NOT a effect of climate change?</strong></p>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">Rising sea levels</button>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">More extreme weather</button>
                <button class="quiz-btn correct" onclick="showAnswer(this, 'correct')" style="margin: 5px; padding: 10px; background: #2E8B57; color: white; border: none; border-radius: 5px;">Decreased temperatures</button>
                <div class="answer-feedback" style="margin-top: 10px; display: none;"></div>
            </div>
            
            <!-- QUIZ 3 -->
            <div class="quiz-section" style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3>📝 Quiz 3: Solutions</h3>
                <p><strong>What is the most effective way to reduce carbon emissions?</strong></p>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">Using more air conditioning</button>
                <button class="quiz-btn correct" onclick="showAnswer(this, 'correct')" style="margin: 5px; padding: 10px; background: #2E8B57; color: white; border: none; border-radius: 5px;">Using renewable energy</button>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">Driving more frequently</button>
                <div class="answer-feedback" style="margin-top: 10px; display: none;"></div>
            </div>
        </div>
        '''
    },
    {
        'id': 2,
        'title': 'Waste Management & Recycling',
        'description': 'Learn about recycling and waste segregation.',
        'category': 'waste-management',
        'points': 20,
        'duration': 25,
        'is_published': True,
        'content': '''
        <div class="lesson-content">
            <h2>♻️ Waste Management & Recycling</h2>
            
            <div class="video-container">
                <iframe width="100%" height="400" src="https://www.youtube.com/embed/OagTXWfaXEo" 
                        frameborder="0" allowfullscreen></iframe>
            </div>
            
            <h3>The 3Rs of Waste Management</h3>
            <p>Reduce, Reuse, Recycle - the three essential steps for effective waste management...</p>
            
            <!-- QUIZ 1 -->
            <div class="quiz-section" style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3>📝 Quiz 1: Recycling Symbols</h3>
                <p><strong>Which symbol represents recyclable plastic?</strong></p>
                <button class="quiz-btn correct" onclick="showAnswer(this, 'correct')" style="margin: 5px; padding: 10px; background: #2E8B57; color: white; border: none; border-radius: 5px;">♳ PETE Symbol</button>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">☢ Radiation Symbol</button>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">⚡ High Voltage</button>
                <div class="answer-feedback" style="margin-top: 10px; display: none;"></div>
            </div>
            
            <!-- QUIZ 2 -->
            <div class="quiz-section" style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3>📝 Quiz 2: Composting</h3>
                <p><strong>Which item CANNOT be composted?</strong></p>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">Fruit peels</button>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">Vegetable scraps</button>
                <button class="quiz-btn correct" onclick="showAnswer(this, 'correct')" style="margin: 5px; padding: 10px; background: #2E8B57; color: white; border: none; border-radius: 5px;">Plastic bags</button>
                <div class="answer-feedback" style="margin-top: 10px; display: none;"></div>
            </div>
            
            <!-- QUIZ 3 -->
            <div class="quiz-section" style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3>📝 Quiz 3: Waste Segregation</h3>
                <p><strong>Where should you dispose of used batteries?</strong></p>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">Regular trash</button>
                <button class="quiz-btn correct" onclick="showAnswer(this, 'correct')" style="margin: 5px; padding: 10px; background: #2E8B57; color: white; border: none; border-radius: 5px;">E-waste collection</button>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">Compost bin</button>
                <div class="answer-feedback" style="margin-top: 10px; display: none;"></div>
            </div>
        </div>
        '''
    },
    {
        'id': 3,
        'title': 'Biodiversity Conservation',
        'description': 'Discover the importance of ecosystems.',
        'category': 'biodiversity',
        'points': 20,
        'duration': 35,
        'is_published': True,
        'content': '''
        <div class="lesson-content">
            <h2>🌿 Biodiversity Conservation</h2>
            
            <div class="video-container">
                <iframe width="100%" height="400" src="https://www.youtube.com/embed/GK_vRtHJZu4" 
                        frameborder="0" allowfullscreen></iframe>
            </div>
            
            <h3>Protecting Our Natural World</h3>
            <p>Biodiversity is essential for ecosystem stability and human survival...</p>
            
            <!-- QUIZ 1 -->
            <div class="quiz-section" style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3>📝 Quiz 1: Endangered Species</h3>
                <p><strong>Which of these is an endangered species in India?</strong></p>
                <button class="quiz-btn correct" onclick="showAnswer(this, 'correct')" style="margin: 5px; padding: 10px; background: #2E8B57; color: white; border: none; border-radius: 5px;">Bengal Tiger</button>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">Domestic Cat</button>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">Common Crow</button>
                <div class="answer-feedback" style="margin-top: 10px; display: none;"></div>
            </div>
            
            <!-- QUIZ 2 -->
            <div class="quiz-section" style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3>📝 Quiz 2: Ecosystem Services</h3>
                <p><strong>What service do bees provide for biodiversity?</strong></p>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">Soil formation</button>
                <button class="quiz-btn correct" onclick="showAnswer(this, 'correct')" style="margin: 5px; padding: 10px; background: #2E8B57; color: white; border: none; border-radius: 5px;">Pollination</button>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">Water purification</button>
                <div class="answer-feedback" style="margin-top: 10px; display: none;"></div>
            </div>
            
            <!-- QUIZ 3 -->
            <div class="quiz-section" style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3>📝 Quiz 3: Conservation</h3>
                <p><strong>What is the best way to protect biodiversity?</strong></p>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">Build more cities</button>
                <button class="quiz-btn" onclick="showAnswer(this, 'wrong')" style="margin: 5px; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 5px;">Use more pesticides</button>
                <button class="quiz-btn correct" onclick="showAnswer(this, 'correct')" style="margin: 5px; padding: 10px; background: #2E8B57; color: white; border: none; border-radius: 5px;">Create protected areas</button>
                <div class="answer-feedback" style="margin-top: 10px; display: none;"></div>
            </div>
        </div>
        '''
    }
]

# Add this JavaScript function to your frontend script.js
quiz_javascript = '''
<script>
function showAnswer(button, result) {
    const feedback = button.parentElement.querySelector('.answer-feedback');
    
    if (result === 'correct') {
        button.style.background = '#28a745';
        feedback.innerHTML = '<div style="color: #28a745; font-weight: bold;">✅ Correct! Well done!</div>';
    } else {
        button.style.background = '#dc3545';
        feedback.innerHTML = '<div style="color: #dc3545; font-weight: bold;">❌ Incorrect. Try again!</div>';
    }
    
    feedback.style.display = 'block';
    
    // Disable all buttons in this quiz
    const buttons = button.parentElement.querySelectorAll('.quiz-btn');
    buttons.forEach(btn => {
        btn.disabled = true;
        btn.style.cursor = 'not-allowed';
    });
}
</script>
'''

def generate_token(user_id):
    payload = {'user_id': user_id, 'exp': datetime.utcnow() + timedelta(days=7)}
    return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')

def find_user_by_email(email):
    for user in users:
        if user['email'] == email:
            return user
    return None

@app.route('/')
def home():
    return jsonify({'message': 'EcoLearn Backend with Quizzes - Ready!', 'status': 'success'})

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        user_id = len(users) + 1
        new_user = {
            'id': user_id, 'name': data['name'], 'email': data['email'], 
            'password': data['password'], 'eco_points': 0, 'level': 1
        }
        users.append(new_user)
        token = generate_token(user_id)
        return jsonify({'success': True, 'message': 'Registered!', 'token': token, 'user': new_user}), 201
    except:
        return jsonify({'success': False, 'message': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = find_user_by_email(data['email'])
        if user and user['password'] == data['password']:
            token = generate_token(user['id'])
            return jsonify({'success': True, 'message': 'Login success!', 'token': token, 'user': user})
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    except:
        return jsonify({'success': False, 'message': 'Login failed'}), 500

@app.route('/api/lessons', methods=['GET'])
def get_lessons():
    return jsonify({'success': True, 'lessons': lessons})

@app.route('/api/lessons/<int:lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    lesson = lessons[lesson_id - 1] if 0 < lesson_id <= len(lessons) else None
    if lesson:
        # Add JavaScript to the lesson content
        lesson_with_js = lesson.copy()
        lesson_with_js['content'] = lesson['content'] + quiz_javascript
        return jsonify({'success': True, 'lesson': lesson_with_js})
    return jsonify({'success': False, 'message': 'Lesson not found'}), 404

if __name__ == '__main__':
    print("🚀 ECOLEARN BACKEND WITH INTERACTIVE QUIZZES!")
    print("📍 http://localhost:5000")
    print("🎯 Each lesson now has 3 interactive quizzes!")
    app.run(debug=True, port=5000)
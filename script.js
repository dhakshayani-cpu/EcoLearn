const API_BASE_URL = 'http://localhost:5000/api';

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation Toggle
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking on a link
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
    
    // Leaderboard Tabs
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to current button and content
            this.classList.add('active');
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });
    
    // Animate Progress Bars
    const progressBars = document.querySelectorAll('.progress-bar');
    
    function animateProgressBars() {
        progressBars.forEach(bar => {
            const progress = bar.getAttribute('data-progress');
            const fill = bar;
            if (fill.style.width === '0px' || fill.style.width === '') {
                fill.style.width = `${progress}%`;
            }
        });
    }
    
    // Initialize any progress bars that are already in view
    animateProgressBars();
    
    // Challenge Button Interactions
    const challengeBtns = document.querySelectorAll('.challenge-btn');
    
    challengeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const token = localStorage.getItem('token');
            if (!token) {
                // Show login modal if not logged in
                showAuthModal();
                return;
            }
            
            const challengeCard = this.closest('.challenge-card');
            const challengeId = Array.from(challengeCard.parentNode.children).indexOf(challengeCard) + 1;
            
            // Open file upload modal for challenge
            openChallengeModal(challengeId);
        });
    });
    
    function checkAnswer(button, type) {
        const quizSection = button.closest('.quiz-section');
        const feedback = quizSection.querySelector('.answer-feedback');
        
        // Prevent multiple answers
        if (quizSection.classList.contains('answered')) return;
        
        quizSection.classList.add('answered');
        
        if (type === 'correct') {
            feedback.textContent = '✅ Correct! Well done!';
            feedback.className = 'answer-feedback correct-answer';
        } else {
            feedback.textContent = '❌ Incorrect. Try again!';
            feedback.className = 'answer-feedback wrong-answer';
        }
        
        feedback.style.display = 'block';
        
        // Disable buttons after answering
        const buttons = quizSection.querySelectorAll('.quiz-btn');
        buttons.forEach(btn => {
            btn.style.cursor = 'not-allowed';
            btn.onclick = null;
        });
    }
    
    // Lesson Button Interactions
    const lessonBtns = document.querySelectorAll('.lesson-btn');
    
    lessonBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const lessonCard = this.closest('.lesson-card');
            const lessonId = Array.from(lessonCard.parentNode.children).indexOf(lessonCard) + 1;
            
            // Open lesson modal
            openLessonModal(lessonId);
        });
    });
    
    // Smooth Scrolling for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const headerHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Teacher Dashboard Access
    const teacherBtn = document.querySelector('.teacher-btn');
    const dashboardCta = document.querySelector('.dashboard-cta .btn');
    
    function showTeacherLogin() {
        alert('Teacher Dashboard Login\n\nIn the full application, this would redirect to a secure login page for educators.');
    }
    
    if (teacherBtn) {
        teacherBtn.addEventListener('click', showTeacherLogin);
    }
    
    if (dashboardCta) {
        dashboardCta.addEventListener('click', showTeacherLogin);
    }
    
    // Certificate Viewing
    const certificateBtns = document.querySelectorAll('.certificate-btn:not([disabled])');
    
    certificateBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const certificate = this.closest('.certificate');
            const certTitle = certificate.querySelector('h4').textContent;
            
            alert(`Viewing certificate: ${certTitle}\n\nIn the full application, this would open a printable certificate.`);
        });
    });
    
    // Create authentication modals
    createAuthModals();
    
    // Check if user is logged in on page load
    checkAuthStatus();
    
    // Load data from backend
    loadDataFromBackend();
});

// ==================== STAT MODAL FUNCTIONALITY ====================

// Function to show detailed information when stats are clicked
function showStatDetails(statType) {
    const messages = {
        'students': {
            title: 'Students Engaged',
            details: 'Over 5,000 students across India are actively participating in EcoLearn programs, making a real impact on environmental conservation.',
            icon: '👨‍🎓'
        },
        'schools': {
            title: 'Schools Participating', 
            details: 'More than 250 educational institutions have partnered with EcoLearn to integrate environmental education into their curriculum.',
            icon: '🏫'
        },
        'trees': {
            title: 'Trees Planted',
            details: 'Students have collectively planted over 10,000 trees, creating green spaces and contributing to carbon sequestration efforts.',
            icon: '🌳'
        }
    };

    const stat = messages[statType];
    
    // Create or update modal
    let modal = document.getElementById('statModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'statModal';
        modal.className = 'stat-modal';
        document.body.appendChild(modal);
        
        // Add CSS for modal
        const style = document.createElement('style');
        style.textContent = `
            .stat-modal {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                z-index: 1000;
                max-width: 400px;
                width: 90%;
                text-align: center;
            }
            .stat-modal-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.5);
                z-index: 999;
            }
            .stat-modal h3 {
                color: #2e8b57;
                margin-bottom: 1rem;
                font-size: 1.5rem;
            }
            .stat-modal .icon {
                font-size: 3rem;
                margin-bottom: 1rem;
            }
            .stat-modal p {
                margin-bottom: 1.5rem;
                line-height: 1.6;
            }
            .stat-modal .close-btn {
                background: #2e8b57;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1rem;
            }
        `;
        document.head.appendChild(style);
    }
    
    // Create overlay
    let overlay = document.querySelector('.stat-modal-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'stat-modal-overlay';
        document.body.appendChild(overlay);
    }
    
    // Update modal content
    modal.innerHTML = `
        <div class="icon">${stat.icon}</div>
        <h3>${stat.title}</h3>
        <p>${stat.details}</p>
        <button class="close-btn" onclick="closeStatModal()">Close</button>
    `;
    
    // Show modal and overlay
    modal.style.display = 'block';
    overlay.style.display = 'block';
}

function closeStatModal() {
    const modal = document.getElementById('statModal');
    const overlay = document.querySelector('.stat-modal-overlay');
    
    if (modal) modal.style.display = 'none';
    if (overlay) overlay.style.display = 'none';
}

// Close modal when clicking outside
document.addEventListener('click', function(event) {
    const modal = document.getElementById('statModal');
    const overlay = document.querySelector('.stat-modal-overlay');
    
    if (overlay && event.target === overlay) {
        closeStatModal();
    }
});

// ==================== AUTHENTICATION MODAL ====================

function createAuthModals() {
    const authHTML = `
    <div id="authModal" class="modal" style="display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5);">
        <div class="modal-content" style="background-color: white; margin: 15% auto; padding: 20px; border-radius: 10px; width: 90%; max-width: 400px; position: relative;">
            <span class="close" onclick="closeAuthModal()" style="position: absolute; right: 15px; top: 15px; font-size: 24px; cursor: pointer;">&times;</span>
            
            <div id="loginForm">
                <h2 style="color: #2E8B57; margin-bottom: 20px;">Login to EcoLearn</h2>
                <form id="loginFormElement">
                    <input type="email" id="loginEmail" placeholder="Email" required style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
                    <input type="password" id="loginPassword" placeholder="Password" required style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
                    <button type="submit" class="btn primary" style="width: 100%; margin-top: 10px;">Login</button>
                </form>
                <p style="text-align: center; margin-top: 15px;">Don't have an account? <a href="#" id="showRegister" style="color: #2E8B57;">Register here</a></p>
            </div>
            
            <div id="registerForm" style="display: none;">
                <h2 style="color: #2E8B57; margin-bottom: 20px;">Join EcoLearn</h2>
                <form id="registerFormElement">
                    <input type="text" id="registerName" placeholder="Full Name" required style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
                    <input type="email" id="registerEmail" placeholder="Email" required style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
                    <input type="password" id="registerPassword" placeholder="Password" required style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
                    <select id="registerRole" required style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
                        <option value="">Select Role</option>
                        <option value="student">Student</option>
                        <option value="teacher">Teacher</option>
                    </select>
                    <input type="text" id="registerSchool" placeholder="School (optional)" style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
                    <button type="submit" class="btn primary" style="width: 100%; margin-top: 10px;">Register</button>
                </form>
                <p style="text-align: center; margin-top: 15px;">Already have an account? <a href="#" id="showLogin" style="color: #2E8B57;">Login here</a></p>
            </div>
        </div>
    </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', authHTML);
    setupAuthHandlers();
}

function setupAuthHandlers() {
    const modal = document.getElementById('authModal');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const showRegister = document.getElementById('showRegister');
    const showLogin = document.getElementById('showLogin');
    
    // Get Started button handler
    const getStartedBtn = document.querySelector('.hero-buttons .btn.primary');
    if (getStartedBtn) {
        getStartedBtn.addEventListener('click', showAuthModal);
    }
    
    // Teacher button handler
    const teacherBtn = document.querySelector('.teacher-btn');
    if (teacherBtn) {
        teacherBtn.addEventListener('click', showAuthModal);
    }
    
    // Switch between login and register
    showRegister.addEventListener('click', (e) => {
        e.preventDefault();
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
    });
    
    showLogin.addEventListener('click', (e) => {
        e.preventDefault();
        registerForm.style.display = 'none';
        loginForm.style.display = 'block';
    });
    
    // Form submissions
    document.getElementById('loginFormElement').addEventListener('submit', handleLogin);
    document.getElementById('registerFormElement').addEventListener('submit', handleRegister);
}

function showAuthModal() {
    const modal = document.getElementById('authModal');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    modal.style.display = 'block';
    loginForm.style.display = 'block';
    registerForm.style.display = 'none';
}

function closeAuthModal() {
    const modal = document.getElementById('authModal');
    modal.style.display = 'none';
}

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    const modal = document.getElementById('authModal');
    if (e.target === modal) {
        closeAuthModal();
    }
});

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });
        
        const data = await response.json();
        
        if (data.success) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            closeAuthModal();
            alert('Login successful! 🎉');
            updateUIForLoggedInUser(data.user);
        } else {
            alert('Login failed: ' + data.message);
        }
    } catch (error) {
        alert('Login error: ' + error.message);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const userData = {
        name: document.getElementById('registerName').value,
        email: document.getElementById('registerEmail').value,
        password: document.getElementById('registerPassword').value,
        role: document.getElementById('registerRole').value,
        school: document.getElementById('registerSchool').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        });
        
        const data = await response.json();
        
        if (data.success) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            closeAuthModal();
            alert('Registration successful! 🎉 Welcome to EcoLearn!');
            updateUIForLoggedInUser(data.user);
        } else {
            alert('Registration failed: ' + data.message);
        }
    } catch (error) {
        alert('Registration error: ' + error.message);
    }
}

function updateUIForLoggedInUser(user) {
    // Update navigation to show user info
    const navMenu = document.querySelector('.nav-menu');
    const userHTML = `
        <li class="user-info" style="display: flex; flex-direction: column; align-items: center; padding: 10px;">
            <span style="font-weight: bold;">Welcome, ${user.name}</span>
            <span class="points-display" style="background: #FFD166; padding: 4px 12px; border-radius: 20px; font-weight: bold; margin-top: 5px;">${user.eco_points} pts</span>
        </li>
        <li><a href="#" id="logout" style="color: #2E8B57;">Logout</a></li>
    `;
    
    // Remove existing auth buttons and add user info
    const existingAuthItems = document.querySelector('.auth-items');
    if (existingAuthItems) {
        existingAuthItems.remove();
    }
    
    const authItems = document.createElement('div');
    authItems.className = 'auth-items';
    authItems.innerHTML = userHTML;
    navMenu.appendChild(authItems);
    
    // Add logout handler
    document.getElementById('logout').addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        location.reload();
    });
}

function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
        updateUIForLoggedInUser(JSON.parse(user));
    }
}

function updatePointsDisplay(points) {
    const pointsDisplay = document.querySelector('.points-display');
    if (pointsDisplay) {
        pointsDisplay.textContent = `${points} pts`;
    }
}

async function loadDataFromBackend() {
    try {
        // Load challenges from backend
        const response = await fetch(`${API_BASE_URL}/challenges`);
        const data = await response.json();
        
        if (data.success) {
            console.log('Loaded challenges from backend:', data.challenges);
        }
    } catch (error) {
        console.log('Using default frontend data');
    }
}

// ==================== LESSON MODAL ====================

function openLessonModal(lessonId) {
    // For now, use mock data. In real app, fetch from backend
    const lessons = [
        {
            id: 1,
            title: 'Climate Change Fundamentals',
            description: 'Understand the causes and effects of global warming.',
            content: `
            <div class="lesson-content">
                <h2>🌍 Climate Change Fundamentals</h2>
                
                <div class="video-container">
                    <iframe width="100%" height="400" src="https://www.youtube.com/embed/G4H1N_yXBiA" 
                            frameborder="0" allowfullscreen></iframe>
                </div>
                
                <h3>What is Climate Change?</h3>
                <p>Climate change refers to long-term shifts in temperatures and weather patterns...</p>
                
                <div class="quiz-section">
                    <h3>Quick Quiz</h3>
                    <p><strong>What is the main greenhouse gas?</strong></p>
                    <button class="btn primary" onclick="alert('Correct! ✅')">Carbon Dioxide</button>
                    <button class="btn secondary" onclick="alert('Try again! ❌')">Oxygen</button>
                </div>
            </div>
            `
        },
        {
            id: 2,
            title: 'Waste Management',
            description: 'Learn about recycling and waste segregation.',
            content: `
            <div class="lesson-content">
                <h2>♻️ Waste Management</h2>
                
                <div class="video-container">
                    <iframe width="100%" height="400" src="https://www.youtube.com/embed/OagTXWfaXEo" 
                            frameborder="0" allowfullscreen></iframe>
                </div>
                
                <h3>The 3Rs</h3>
                <p>Reduce, Reuse, Recycle - Learn how to manage waste effectively...</p>
            </div>
            `
        }
    ];
    
    const lesson = lessons[lessonId - 1] || lessons[0];
    
    const modalHTML = `
    <div id="lessonModal" class="modal" style="display: block; position: fixed; z-index: 1001; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); overflow-y: auto;">
        <div class="modal-content" style="background-color: white; margin: 2% auto; padding: 30px; border-radius: 10px; width: 90%; max-width: 900px; position: relative;">
            <span class="close" onclick="closeLessonModal()" style="position: absolute; right: 15px; top: 15px; font-size: 24px; cursor: pointer;">&times;</span>
            
            <h2 style="color: #2E8B57; margin-bottom: 10px;">${lesson.title}</h2>
            <p style="color: #666; margin-bottom: 30px;">${lesson.description}</p>
            
            <div class="lesson-content">
                ${lesson.content}
            </div>
            
            <div style="margin-top: 30px; text-align: center;">
                <button class="btn primary" onclick="completeLesson(${lessonId})">Mark as Completed</button>
                <button class="btn secondary" onclick="closeLessonModal()">Close</button>
            </div>
        </div>
    </div>
    `;
    
    // Remove any existing lesson modal
    const existingModal = document.getElementById('lessonModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

function closeLessonModal() {
    const modal = document.getElementById('lessonModal');
    if (modal) {
        modal.remove();
    }
}

function completeLesson(lessonId) {
    alert(`✅ Lesson ${lessonId} completed! +20 points earned!`);
    closeLessonModal();
}

// ==================== CHALLENGE MODAL ====================

function openChallengeModal(challengeId) {
    const modalHTML = `
    <div id="challengeModal" class="modal" style="display: block; position: fixed; z-index: 1001; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5);">
        <div class="modal-content" style="background-color: white; margin: 10% auto; padding: 30px; border-radius: 10px; width: 90%; max-width: 500px; position: relative;">
            <span class="close" onclick="closeChallengeModal()" style="position: absolute; right: 15px; top: 15px; font-size: 24px; cursor: pointer;">&times;</span>
            
            <h2 style="color: #2E8B57; margin-bottom: 20px;">Submit Challenge Evidence</h2>
            <p style="margin-bottom: 20px;">Upload a photo or video showing you completed the challenge:</p>
            
            <form id="challengeForm">
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: bold;">Upload Evidence:</label>
                    <input type="file" id="challengeEvidence" accept="image/*,video/*" style="width: 100%; padding: 10px; border: 2px dashed #2E8B57; border-radius: 5px;">
                </div>
                
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: bold;">Description:</label>
                    <textarea id="challengeDescription" placeholder="Describe how you completed the challenge..." style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; height: 100px;"></textarea>
                </div>
                
                <button type="submit" class="btn primary" style="width: 100%;">Submit Evidence & Earn Points</button>
            </form>
        </div>
    </div>
    `;
    
    // Remove any existing challenge modal
    const existingModal = document.getElementById('challengeModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    document.getElementById('challengeForm').addEventListener('submit', function(e) {
        e.preventDefault();
        submitChallengeEvidence(challengeId);
    });
}

function closeChallengeModal() {
    const modal = document.getElementById('challengeModal');
    if (modal) {
        modal.remove();
    }
}

async function submitChallengeEvidence(challengeId) {
    const fileInput = document.getElementById('challengeEvidence');
    const description = document.getElementById('challengeDescription').value;
    const token = localStorage.getItem('token');
    
    if (!fileInput.files[0]) {
        alert('Please upload evidence photo/video!');
        return;
    }
    
    // Simulate challenge completion
    alert(`✅ Challenge ${challengeId} completed! Evidence submitted successfully!`);
    closeChallengeModal();
}
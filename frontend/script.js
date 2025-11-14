const API_BASE_URL = 'http://127.0.0.1:8000';

// Health quotes for the floating widget
const healthQuotes = [
    "Your health is an investment, not an expense.",
    "The greatest wealth is health.",
    "Take care of your body. It's the only place you have to live.",
    "Health is a state of complete harmony of the body, mind and spirit.",
    "The first wealth is health.",
    "A healthy outside starts from the inside.",
    "Wellness is the complete integration of body, mind, and spirit.",
    "Keep your vitality. A life without health is like a river without water.",
    "He who has health has hope; and he who has hope has everything.",
    "To ensure good health: eat lightly, breathe deeply, live moderately, cultivate cheerfulness."
];

let currentQuoteIndex = 0;

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize floating quote widget
    initializeQuoteWidget();
    
    // Load health tips on homepage
    if (document.getElementById('healthTips')) {
        loadHealthTips();
    }
    
    // Set up form submissions
    setupFormSubmissions();
    
    // Set up symptom checker
    setupSymptomChecker();
    
    // Check auth status
    checkAuthStatus();
}

function initializeQuoteWidget() {
    const quoteWidget = document.getElementById('quoteWidget');
    if (quoteWidget) {
        updateQuoteWidget();
        setInterval(updateQuoteWidget, 10000); // Update every 10 seconds
    }
}

function updateQuoteWidget() {
    const quoteWidget = document.getElementById('quoteWidget');
    if (quoteWidget) {
        const quoteText = document.getElementById('quoteText');
        quoteText.textContent = healthQuotes[currentQuoteIndex];
        currentQuoteIndex = (currentQuoteIndex + 1) % healthQuotes.length;
        
        // Add fade animation
        quoteWidget.style.opacity = '0';
        setTimeout(() => {
            quoteWidget.style.opacity = '1';
        }, 500);
    }
}

async function loadHealthTips() {
    try {
        const response = await fetch(`${API_BASE_URL}/tips/random`);
        if (!response.ok) {
            throw new Error('Failed to fetch tips');
        }
        const tipData = await response.json();
        
        const tipsContainer = document.getElementById('healthTips');
        if (tipsContainer) {
            tipsContainer.innerHTML = `
                <div class="tip-card">
                    <h3>💡 Health Tip</h3>
                    <p>${tipData.tip}</p>
                    <small>Category: ${tipData.category}</small>
                </div>
            `;
        }
        
        // Also update tip of the day
        const tipOfDay = document.getElementById('tipOfDay');
        if (tipOfDay) {
            tipOfDay.textContent = tipData.tip;
        }
    } catch (error) {
        console.error('Error loading health tips:', error);
        const tipsContainer = document.getElementById('healthTips');
        if (tipsContainer) {
            tipsContainer.innerHTML = `
                <div class="tip-card">
                    <h3>💡 Health Tip</h3>
                    <p>Stay hydrated and maintain a balanced diet for optimal health.</p>
                    <small>Category: general</small>
                </div>
            `;
        }
    }
}

function setupFormSubmissions() {
    // Signup form
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
    }
    
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
}

function setupSymptomChecker() {
    const symptomForm = document.getElementById('symptomForm');
    if (symptomForm) {
        symptomForm.addEventListener('submit', analyzeSymptoms);
    }
}

async function handleSignup(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const userData = {
        username: formData.get('username'),
        email: formData.get('email'),
        password: formData.get('password')
    };
    
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    try {
        submitBtn.innerHTML = '<div class="loading"></div> Signing up...';
        submitBtn.disabled = true;
        
        const response = await fetch(`${API_BASE_URL}/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage('success', 'Account created successfully! Redirecting to login...');
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            showMessage('error', result.detail || 'Signup failed. Please try again.');
        }
    } catch (error) {
        showMessage('error', 'Network error. Please check if the backend server is running.');
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

async function handleLogin(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const loginData = {
        username: formData.get('username'),
        password: formData.get('password')
    };
    
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    try {
        submitBtn.innerHTML = '<div class="loading"></div> Logging in...';
        submitBtn.disabled = true;
        
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage('success', 'Login successful! Redirecting...');
            // Store token and user info
            localStorage.setItem('token', result.access_token);
            localStorage.setItem('user_id', result.user_id);
            localStorage.setItem('username', result.username);
            
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 1500);
        } else {
            showMessage('error', result.detail || 'Login failed. Please check your credentials.');
        }
    } catch (error) {
        showMessage('error', 'Network error. Please check if the backend server is running.');
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

async function analyzeSymptoms(event) {
    event.preventDefault();
    
    const symptoms = document.getElementById('symptoms').value;
    const userId = localStorage.getItem('user_id');
    const resultDiv = document.getElementById('analysisResult');
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    if (!symptoms.trim()) {
        showMessage('error', 'Please describe your symptoms.');
        return;
    }
    
    try {
        submitBtn.innerHTML = '<div class="loading"></div> Analyzing...';
        submitBtn.disabled = true;
        
        const response = await fetch(`${API_BASE_URL}/symptom/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                symptoms: symptoms,
                user_id: userId ? parseInt(userId) : null
            })
        });
        
        if (!response.ok) {
            throw new Error('Analysis failed');
        }
        
        const result = await response.json();
        
        resultDiv.innerHTML = `
            <div class="analysis-result severity-${result.severity}">
                <h3>🔍 Analysis Result</h3>
                <p><strong>Assessment:</strong> ${result.analysis}</p>
                <p><strong>Recommendation:</strong> ${result.recommendation}</p>
                <p><strong>Severity:</strong> <span class="severity-${result.severity}">${result.severity.charAt(0).toUpperCase() + result.severity.slice(1)}</span></p>
                <div class="disclaimer">
                    <small><em>Disclaimer: This is an AI-powered preliminary assessment and should not replace professional medical advice. Always consult a healthcare provider for accurate diagnosis.</em></small>
                </div>
            </div>
        `;
        resultDiv.classList.remove('hidden');
        
    } catch (error) {
        showMessage('error', 'Analysis failed. Please check if the backend server is running.');
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

function showMessage(type, message) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.success-message, .error-message');
    existingMessages.forEach(msg => msg.remove());
    
    const messageDiv = document.createElement('div');
    messageDiv.className = type === 'success' ? 'success-message' : 'error-message';
    messageDiv.textContent = message;
    
    // Insert message at the top of the form container
    const formContainer = document.querySelector('.form-container') || document.querySelector('.card') || document.body;
    formContainer.insertBefore(messageDiv, formContainer.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Check if user is logged in
function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const authLinks = document.getElementById('authLinks');
    const userLinks = document.getElementById('userLinks');
    
    if (token && authLinks && userLinks) {
        authLinks.style.display = 'none';
        userLinks.style.display = 'flex';
        const username = localStorage.getItem('username');
        document.getElementById('usernameDisplay').textContent = username;
    }
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    window.location.href = 'index.html';
}
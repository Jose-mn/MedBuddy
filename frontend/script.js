// Read API base URL from a global injected variable (set this in production),
// otherwise fall back to localhost for local development.
const API_BASE_URL = window.API_BASE_URL || 'https://medbuddy-ks9e.onrender.com';

if (!window.API_BASE_URL) {
    console.warn('API_BASE_URL not found on window. Using fallback:', API_BASE_URL);
}


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

// Test backend connectivity on page load
async function testBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✓ Backend is reachable');
        }
    } catch (error) {
        console.error('✗ Backend not reachable:', error);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    testBackendConnection();
    initializeApp();
});

function initializeApp() {
    initializeQuoteWidget();
    if (document.getElementById('healthTips')) {
        loadHealthTips();
    }
    setupFormSubmissions();
    setupSymptomChecker();
    checkAuthStatus();
}

function initializeQuoteWidget() {
    const quoteWidget = document.getElementById('quoteWidget');
    if (quoteWidget) {
        updateQuoteWidget();
        setInterval(updateQuoteWidget, 10000);
    }
}

function updateQuoteWidget() {
    const quoteWidget = document.getElementById('quoteWidget');
    if (quoteWidget) {
        const quoteText = document.getElementById('quoteText');
        quoteText.textContent = healthQuotes[currentQuoteIndex];
        currentQuoteIndex = (currentQuoteIndex + 1) % healthQuotes.length;
        quoteWidget.style.opacity = '0';
        setTimeout(() => quoteWidget.style.opacity = '1', 500);
    }
}

async function loadHealthTips() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/tips/random`);
        if (!response.ok) throw new Error('Failed to fetch tips');

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

    } catch (error) {
        console.error('Error loading health tips:', error);
    }
}

function setupFormSubmissions() {
    const signupForm = document.getElementById('signupForm');
    if (signupForm) signupForm.addEventListener('submit', handleSignup);

    const loginForm = document.getElementById('loginForm');
    if (loginForm) loginForm.addEventListener('submit', handleLogin);
}

function setupSymptomChecker() {
    const symptomForm = document.getElementById('symptomForm');
    if (symptomForm) symptomForm.addEventListener('submit', analyzeSymptoms);
}

// SIGNUP
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
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });

        const result = await response.json();

        if (response.ok) {
            showMessage('success', 'Account created! Redirecting...');
            setTimeout(() => window.location.href = 'login.html', 1500);
        } else {
            const errorDetail = result.detail || 'Signup failed';
            console.error('Signup error:', errorDetail);
            showMessage('error', errorDetail);
        }

    } catch (error) {
        console.error('Signup exception:', error);
        showMessage('error', 'Backend not reachable: ' + error.message);
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

// LOGIN
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
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(loginData)
        });

        const result = await response.json();

        if (response.ok) {
            localStorage.setItem('token', result.access_token);
            localStorage.setItem('user_id', result.user_id);
            localStorage.setItem('username', result.username);

            showMessage('success', 'Login successful! Redirecting...');
            setTimeout(() => window.location.href = 'index.html', 1500);
        } else {
            showMessage('error', result.detail || 'Invalid credentials.');
        }

    } catch (error) {
        showMessage('error', 'Backend not reachable.');
    }

    submitBtn.textContent = originalText;
    submitBtn.disabled = false;
}

// SYMPTOM CHECKER
async function analyzeSymptoms(event) {
    event.preventDefault();

    const symptoms = document.getElementById('symptoms').value;
    const userId = localStorage.getItem('user_id');

    if (!symptoms.trim()) {
        showMessage('error', 'Please enter your symptoms.');
        return;
    }

    const resultDiv = document.getElementById('analysisResult');
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;

    try {
        submitBtn.innerHTML = '<div class="loading"></div> Analyzing...';
        submitBtn.disabled = true;

        const response = await fetch(`${API_BASE_URL}/symptom/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                symptoms: symptoms,
                user_id: userId ? parseInt(userId) : null
            })
        });

        if (!response.ok) throw new Error('Analysis failed');

        const result = await response.json();

        resultDiv.innerHTML = `
            <div class="analysis-result severity-${result.severity}">
                <h3>🔍 Analysis Result</h3>
                <p><strong>Assessment:</strong> ${result.analysis}</p>
                <p><strong>Recommendation:</strong> ${result.recommendation}</p>
                <p><strong>Severity:</strong> ${result.severity}</p>
            </div>
        `;
        resultDiv.classList.remove('hidden');

    } catch (error) {
        showMessage('error', 'Backend not reachable.');
    }

    submitBtn.textContent = originalText;
    submitBtn.disabled = false;
}

function showMessage(type, message) {
    const existing = document.querySelectorAll('.success-message, .error-message');
    existing.forEach(e => e.remove());

    const div = document.createElement('div');
    div.className = type === 'success' ? 'success-message' : 'error-message';
    div.textContent = message;

    const container = document.querySelector('.form-container') || document.body;
    container.prepend(div);

    setTimeout(() => div.remove(), 5000);
}

// AUTH CHECK
function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const authLinks = document.getElementById('authLinks');
    const userLinks = document.getElementById('userLinks');

    if (token && authLinks && userLinks) {
        authLinks.style.display = 'none';
        userLinks.style.display = 'flex';
        document.getElementById('usernameDisplay').textContent =
            localStorage.getItem('username');
    }
}

function logout() {
    localStorage.clear();
    window.location.href = 'index.html';
}

// Card animations
function animateVisibleCards() {
    const cards = document.querySelectorAll(".plan-card");
    const triggerBottom = window.innerHeight * 0.9;
    cards.forEach(card => {
        if (card.getBoundingClientRect().top < triggerBottom) {
            card.classList.add("visible");
        }
    });
}

window.addEventListener("scroll", animateVisibleCards);
window.addEventListener("load", animateVisibleCards);



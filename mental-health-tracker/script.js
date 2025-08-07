const introScreen = document.getElementById('intro-screen');
const quizScreen = document.getElementById('quiz-screen');
const userNameInput = document.getElementById('user-name');
const startQuizBtn = document.getElementById('start-quiz-btn');

const quizContainer = document.getElementById('quiz-container');
const submitButton = document.getElementById('submit-btn');
const resultContainer = document.getElementById('result-container');

// Gamification elements
let userName = 'Fam'; // Default name
let quizHistory = JSON.parse(localStorage.getItem('vibeQuizHistory') || '[]');
let streak = getCurrentStreak(quizHistory);

// Add history and streak display to intro screen
let historyDiv = document.createElement('div');
historyDiv.id = 'history-streak';
introScreen.appendChild(historyDiv);

function showResults() {
    let score = 0;
    for (const key in userAnswers) {
        score += userAnswers[key];
    }

    // Save result to localStorage
    const today = new Date().toISOString().slice(0, 10);
    quizHistory.push({ date: today, score });
    // Keep only last 30 entries
    if (quizHistory.length > 30) quizHistory = quizHistory.slice(-30);
    localStorage.setItem('vibeQuizHistory', JSON.stringify(quizHistory));
    streak = getCurrentStreak(quizHistory);
    updateHistoryStreakDisplay();

    // POST result to backend (optional, non-blocking)
    fetch('http://localhost:3001/api/results', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: userName, date: today, score })
    }).catch(() => {/* ignore errors for offline/local use */});

    resultContainer.style.color = '#fff';
    let resultHTML = '';

    // Badges
    let badges = '';
    if (streak >= 7) {
        badges += `<span class="badge gold">🔥 7-Day Streak!</span> `;
    } else if (streak >= 3) {
        badges += `<span class="badge silver">✨ 3-Day Streak!</span> `;
    }
    if (quizHistory.length >= 10) {
        badges += `<span class="badge bronze">🏅 10+ Quizzes!</span> `;
    }

    if (score <= 4) {
        resultHTML = `<h3>Vibe Check: All Good, ${userName}! ✨</h3>`;
        resultHTML += `<p>Your score of ${score} means your mental game is strong. Keep that energy up, you're crushing it!</p>`;
        resultHTML += `<h4>Here are some tips to maintain your positive vibe:</h4>`;
        resultHTML += `<ul>`;
        resultHTML += `<li><strong>Keep moving:</strong> A little exercise can boost your mood, for real.</li>`;
        resultHTML += `<li><strong>Stay connected:</strong> Hang out with your squad who lift you up.</li>`;
        resultHTML += `<li><strong>Practice gratitude:</strong> Take a moment each day to appreciate the good things. You got this!</li>`;
        resultHTML += `</ul>`;
    } else if (score <= 8) {
        resultHTML = `<h3>Vibe Check: Time for some self-care, ${userName}, maybe? 💖</h3>`;
        resultHTML += `<p>Your score of ${score} means you might be feeling a bit off, and that's totally valid. Let's get you back to feeling your best.</p>`;
        resultHTML += `<h4>Here are some things you can try:</h4>`;
        resultHTML += `<ul>`;
        if (userAnswers.sleep > 1) {
            resultHTML += `<li><strong>Prioritize sleep:</strong> Try to get 7-9 hours of quality sleep. A consistent sleep schedule can make a big difference, trust.</li>`;
        }
        if (userAnswers.social > 1) {
            resultHTML += `<li><strong>Reach out:</strong> Connect with a friend or family member. A good chat can be really helpful.</li>`;
        }
        if (userAnswers.anxiety > 1) {
            resultHTML += `<li><strong>Try mindfulness:</strong> A few minutes of deep breathing or meditation can help calm your mind.</li>`;
        }
        resultHTML += `<li><strong>Do something you enjoy:</strong> Make time for a hobby or activity that makes you happy.</li>`;
        resultHTML += `</ul>`;
    } else {
        resultHTML = `<h3>Vibe Check: It's okay to not be okay, ${userName}, seriously. ❤️</h3>`;
        resultHTML += `<p>Your score of ${score} means you're going through a tough time. You're not alone, and reaching out is a sign of strength.</p>`;
        resultHTML += `<h4>It's important to talk to someone you trust. Here are some resources:</h4>`;
        resultHTML += `<ul>`;
        resultHTML += `<li><strong>Talk to a friend or family member.</strong></li>`;
        resultHTML += `<li><strong>Consider professional help:</strong> A therapist can provide you with tools and support to navigate what you're feeling.</li>`;
        resultHTML += `<li><strong>Crisis Helpline (India):</strong> Call 022-27546669 (AASRA) or 9152987821 (Vandrevala Foundation).</li>`;
        resultHTML += `<li><strong>Connect with a professional:</strong> Consider reaching out to a therapist or counselor. Platforms like Practo or YourDOST can help you find one.</li>`;
        resultHTML += `<li><strong>Talk to a trusted elder or friend.</strong></li>`;
        resultHTML += `</ul>`;
    }
    // Show badges and history
    resultHTML = badges + resultHTML + getHistoryHTML();
    resultContainer.innerHTML = resultHTML;
}

// Helper: Get current streak (days in a row)
function getCurrentStreak(history) {
    if (!history.length) return 0;
    let streak = 1;
    let prev = new Date(history[history.length - 1].date);
    for (let i = history.length - 2; i >= 0; i--) {
        let curr = new Date(history[i].date);
        let diff = (prev - curr) / (1000 * 60 * 60 * 24);
        if (diff === 1) {
            streak++;
            prev = curr;
        } else if (diff > 1) {
            break;
        }
    }
    return streak;
}

// Helper: Show quiz history and streak
function updateHistoryStreakDisplay() {
    let html = '';
    if (quizHistory.length) {
        html += `<div class="streak-info"><strong>Current Streak:</strong> ${streak} day(s)`;
        if (streak >= 7) html += ' <span class="badge gold">🔥</span>';
        else if (streak >= 3) html += ' <span class="badge silver">✨</span>';
        html += `</div>`;
        html += `<div class="history-info"><strong>Quiz History:</strong> ${quizHistory.length} taken</div>`;
    } else {
        html = '<div class="history-info">Take your first quiz to start your streak!</div>';
    }
    document.getElementById('history-streak').innerHTML = html;
}

// Helper: Get HTML for quiz history (last 5)
function getHistoryHTML() {
    if (!quizHistory.length) return '';
    let html = '<div class="recent-history"><h4>Recent Quizzes</h4><ul>';
    quizHistory.slice(-5).reverse().forEach(q => {
        html += `<li>${q.date}: Score ${q.score}</li>`;
    });
    html += '</ul></div>';
    return html;
}

// Initialize quiz
function startQuiz() {
    introScreen.style.display = 'none';
    quizScreen.style.display = 'block';
}

// Event listener for Start Quiz button
startQuizBtn.addEventListener('click', () => {
    const name = userNameInput.value.trim();
    if (name) {
        userName = name;
    }
    startQuiz();
    showQuestion(currentQuestionIndex);
});

// Add event listener for option selection to move to next question
quizContainer.addEventListener('change', (event) => {
    if (event.target.type === 'radio') {
        nextQuestion();
    }
});

// Initial setup: hide quiz screen
quizScreen.style.display = 'none';
// Add badge styles
const style = document.createElement('style');
style.innerHTML = `
.badge { display: inline-block; padding: 0.2em 0.7em; border-radius: 12px; font-size: 1em; margin-right: 0.5em; font-weight: bold; }
.badge.gold { background: linear-gradient(90deg,#ffd700,#fffbe6); color: #b8860b; border: 1px solid #ffd700; }
.badge.silver { background: linear-gradient(90deg,#e0e0e0,#f8f8f8); color: #555; border: 1px solid #aaa; }
.badge.bronze { background: linear-gradient(90deg,#cd7f32,#fff0e0); color: #7c4700; border: 1px solid #cd7f32; }
.recent-history { margin-top: 1.5em; }
.recent-history ul { padding-left: 1.2em; }
.streak-info, .history-info { margin: 0.5em 0; }
`;
document.head.appendChild(style);


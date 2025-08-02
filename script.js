// Mental Wellness Quiz - Complete Functionality
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

// Questions data
const questions = [
    {
        question: "How would you rate your overall mood lately?",
        key: "mood",
        options: [
            { text: "I'm feeling great, really positive! 😊", value: 0 },
            { text: "Pretty good, no major complaints 🙂", value: 1 },
            { text: "It's been okay, some ups and downs 😐", value: 2 },
            { text: "Not great, feeling pretty low 😔", value: 3 }
        ]
    },
    {
        question: "How's your sleep been?",
        key: "sleep",
        options: [
            { text: "Sleeping like a baby, 7-9 hours solid 😴", value: 0 },
            { text: "Pretty good, getting enough rest 🛌", value: 1 },
            { text: "It's been inconsistent, some good nights 😵", value: 2 },
            { text: "Terrible, barely getting any sleep 🥱", value: 3 }
        ]
    },
    {
        question: "How are you handling stress these days?",
        key: "stress",
        options: [
            { text: "I'm managing it really well 💪", value: 0 },
            { text: "It's under control most of the time 👍", value: 1 },
            { text: "Sometimes it gets overwhelming 😤", value: 2 },
            { text: "I'm really struggling to cope 😰", value: 3 }
        ]
    },
    {
        question: "How's your social life and connections?",
        key: "social",
        options: [
            { text: "Great! I feel connected to my friends/family 🤗", value: 0 },
            { text: "Good, I have people I can talk to 😊", value: 1 },
            { text: "It's okay, but I could use more connection 😕", value: 2 },
            { text: "I feel pretty isolated and lonely 😞", value: 3 }
        ]
    },
    {
        question: "How anxious or worried have you been feeling?",
        key: "anxiety",
        options: [
            { text: "Very calm and relaxed 😌", value: 0 },
            { text: "Occasionally anxious, but manageable 🙂", value: 1 },
            { text: "Worried quite a bit lately 😟", value: 2 },
            { text: "Really anxious, hard to control 😰", value: 3 }
        ]
    }
];

let currentQuestionIndex = 0;
let userAnswers = {};

// Helper: Get current streak (days in a row)
function getCurrentStreak(history) {
    if (!history.length) return 0;
    let streakCount = 1;
    let prev = new Date(history[history.length - 1].date);
    for (let i = history.length - 2; i >= 0; i--) {
        let curr = new Date(history[i].date);
        let diff = (prev - curr) / (1000 * 60 * 60 * 24);
        if (diff === 1) {
            streakCount++;
            prev = curr;
        } else if (diff > 1) {
            break;
        }
    }
    return streakCount;
}

let currentStreak = getCurrentStreak(quizHistory);

// Add history and streak display to intro screen if it exists
if (introScreen) {
    let historyDiv = document.createElement('div');
    historyDiv.id = 'history-streak';
    historyDiv.style.marginTop = '2rem';
    historyDiv.style.padding = '1rem';
    historyDiv.style.background = '#1e293b';
    historyDiv.style.borderRadius = '8px';
    historyDiv.style.border = '1px solid #334155';
    introScreen.appendChild(historyDiv);
    updateHistoryStreakDisplay();
}

function showQuestion(index) {
    if (index >= questions.length) {
        showSubmitButton();
        return;
    }

    const question = questions[index];
    quizContainer.innerHTML = '';

    const questionDiv = document.createElement('div');
    questionDiv.classList.add('question');
    questionDiv.innerHTML = `<h3>Question ${index + 1} of ${questions.length}</h3><h2>${question.question}</h2>`;

    const optionsDiv = document.createElement('div');
    optionsDiv.classList.add('options');

    question.options.forEach((option, optionIndex) => {
        const optionLabel = document.createElement('label');
        optionLabel.classList.add('option');
        
        const input = document.createElement('input');
        input.type = 'radio';
        input.name = `question${index}`;
        input.value = option.value;
        input.id = `question${index}-option${optionIndex}`;
        input.dataset.key = question.key;

        optionLabel.appendChild(input);
        optionLabel.appendChild(document.createTextNode(' ' + option.text));
        optionsDiv.appendChild(optionLabel);
    });

    questionDiv.appendChild(optionsDiv);
    quizContainer.appendChild(questionDiv);

    if (submitButton) {
        submitButton.style.display = 'none';
    }
}

function nextQuestion() {
    const currentQuestion = questions[currentQuestionIndex];
    const selectedOption = document.querySelector(`input[name="question${currentQuestionIndex}"]:checked`);
    
    if (selectedOption) {
        userAnswers[currentQuestion.key] = parseInt(selectedOption.value);
        currentQuestionIndex++;
        
        setTimeout(() => {
            showQuestion(currentQuestionIndex);
        }, 300);
    }
}

function showSubmitButton() {
    quizContainer.innerHTML = '<h3>All done! Ready to see your results?</h3>';
    if (submitButton) {
        submitButton.style.display = 'block';
        submitButton.onclick = showResults; // Use onclick instead of addEventListener to avoid duplicates
    }
}

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
    currentStreak = getCurrentStreak(quizHistory);
    if (introScreen) updateHistoryStreakDisplay();

    // POST result to backend (optional, non-blocking)
    fetch('http://localhost:3001/api/results', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: userName, date: today, score })
    }).catch(() => {/* ignore errors for offline/local use */});

    if (resultContainer) {
        resultContainer.style.color = '#fff';
        let resultHTML = '';

        // Badges
        let badges = '';
        if (currentStreak >= 7) {
            badges += `<span class="badge gold">🔥 7-Day Streak!</span> `;
        } else if (currentStreak >= 3) {
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
        
        // Add restart button
        resultHTML += `<div style="margin-top: 2rem;"><button onclick="restartQuiz()" style="background: #60a5fa; color: #1e293b; border: none; padding: 1rem 2rem; border-radius: 25px; cursor: pointer; font-size: 1rem; font-weight: 600;">Take Quiz Again</button></div>`;
        
        // Show badges and history
        resultHTML = badges + resultHTML + getHistoryHTML();
        resultContainer.innerHTML = resultHTML;
        
        // Hide submit button
        if (submitButton) submitButton.style.display = 'none';
    }
}

function restartQuiz() {
    currentQuestionIndex = 0;
    userAnswers = {};
    if (resultContainer) resultContainer.innerHTML = '';
    if (introScreen && quizScreen) {
        quizScreen.style.display = 'none';
        introScreen.style.display = 'block';
        updateHistoryStreakDisplay();
    } else {
        // If we're on a single page, just restart the quiz
        showQuestion(0);
    }
}

function updateHistoryStreakDisplay() {
    const historyElement = document.getElementById('history-streak');
    if (!historyElement) return;
    
    let html = '';
    if (quizHistory.length) {
        html += `<div class="streak-info"><strong>Current Streak:</strong> ${currentStreak} day(s)`;
        if (currentStreak >= 7) html += ' <span class="badge gold">🔥</span>';
        else if (currentStreak >= 3) html += ' <span class="badge silver">✨</span>';
        html += `</div>`;
        html += `<div class="history-info"><strong>Quiz History:</strong> ${quizHistory.length} taken</div>`;
    } else {
        html = '<div class="history-info">Take your first quiz to start your streak!</div>';
    }
    historyElement.innerHTML = html;
}

function getHistoryHTML() {
    if (!quizHistory.length) return '';
    let html = '<div class="recent-history"><h4>Recent Quizzes</h4><ul>';
    quizHistory.slice(-5).reverse().forEach(q => {
        html += `<li>${q.date}: Score ${q.score}</li>`;
    });
    html += '</ul></div>';
    return html;
}

// Event listeners
if (startQuizBtn) {
    startQuizBtn.addEventListener('click', function() {
        console.log('Start quiz button clicked!'); // Debug log
        
        if (userNameInput) {
            const name = userNameInput.value.trim();
            if (name) {
                userName = name;
            }
        }
        
        if (introScreen && quizScreen) {
            introScreen.style.display = 'none';
            quizScreen.style.display = 'block';
        }
        
        showQuestion(currentQuestionIndex);
    });
}

// Add event listener for option selection to move to next question
if (quizContainer) {
    quizContainer.addEventListener('change', function(event) {
        if (event.target.type === 'radio') {
            nextQuestion();
        }
    });
}

// Initial setup
if (quizScreen) {
    quizScreen.style.display = 'none';
}

// Add styles
const style = document.createElement('style');
style.innerHTML = `
.badge { display: inline-block; padding: 0.2em 0.7em; border-radius: 12px; font-size: 1em; margin-right: 0.5em; font-weight: bold; }
.badge.gold { background: linear-gradient(90deg,#ffd700,#fffbe6); color: #b8860b; border: 1px solid #ffd700; }
.badge.silver { background: linear-gradient(90deg,#e0e0e0,#f8f8f8); color: #555; border: 1px solid #aaa; }
.badge.bronze { background: linear-gradient(90deg,#cd7f32,#fff0e0); color: #7c4700; border: 1px solid #cd7f32; }
.recent-history { margin-top: 1.5em; }
.recent-history ul { padding-left: 1.2em; }
.streak-info, .history-info { margin: 0.5em 0; color: #94a3b8; }
.question { margin: 2rem 0; text-align: center; }
.question h3 { color: #60a5fa; margin-bottom: 0.5rem; }
.question h2 { color: #fff; margin-bottom: 1.5rem; }
.options { margin: 1rem 0; text-align: left; max-width: 600px; margin-left: auto; margin-right: auto; }
.option { 
    display: block; 
    margin: 0.8rem 0; 
    padding: 1rem; 
    background: #1e293b; 
    border: 2px solid #334155; 
    border-radius: 12px; 
    cursor: pointer; 
    transition: all 0.3s ease;
    color: #e2e8f0;
    font-size: 1rem;
}
.option:hover { 
    background: #334155; 
    border-color: #60a5fa; 
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(96, 165, 250, 0.2);
}
.option input[type="radio"] { 
    margin-right: 0.8rem;
    transform: scale(1.2);
}
.option input[type="radio"]:checked { 
    accent-color: #60a5fa;
}
.name-input-container { 
    margin: 2rem 0; 
    max-width: 400px;
    margin-left: auto;
    margin-right: auto;
}
.name-input-container label { 
    display: block; 
    margin-bottom: 0.8rem; 
    color: #94a3b8;
    font-size: 1.1rem;
}
.name-input-container input { 
    width: 100%; 
    padding: 1rem; 
    border: 2px solid #334155; 
    border-radius: 12px; 
    background: #1e293b; 
    color: #fff; 
    font-size: 1rem;
    transition: border-color 0.3s ease;
}
.name-input-container input:focus {
    border-color: #60a5fa;
    outline: none;
}
.name-input-container button { 
    margin-top: 1.5rem; 
    background: #60a5fa; 
    color: #1e293b; 
    border: none; 
    padding: 1rem 2.5rem; 
    border-radius: 25px; 
    cursor: pointer; 
    font-size: 1.1rem; 
    font-weight: 600; 
    transition: all 0.3s ease;
    width: 100%;
}
.name-input-container button:hover { 
    background: #3b82f6; 
    transform: translateY(-2px); 
    box-shadow: 0 4px 15px rgba(96, 165, 250, 0.3);
}
#submit-btn {
    background: #60a5fa;
    color: #1e293b;
    border: none;
    padding: 1rem 2.5rem;
    border-radius: 25px;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 600;
    margin: 2rem auto;
    display: block;
    transition: all 0.3s ease;
}
#submit-btn:hover {
    background: #3b82f6;
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(96, 165, 250, 0.3);
}
`;
document.head.appendChild(style);

console.log('Script loaded successfully!'); // Debug log

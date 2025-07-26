document.addEventListener('DOMContentLoaded', () => {
    const quizContainer = document.getElementById('quiz-container');
    const submitButton = document.getElementById('submit-btn');
    const resultContainer = document.getElementById('result-container');

    const questions = [
        {
            question: "Over the last 2 weeks, how often have you been bothered by feeling down, depressed, or hopeless?",
            options: [
                { text: "Not at all", value: 0 },
                { text: "Several days", value: 1 },
                { text: "More than half the days", value: 2 },
                { text: "Nearly every day", value: 3 }
            ],
            key: 'mood'
        },
        {
            question: "How would you rate your sleep quality over the past week?",
            options: [
                { text: "Very good", value: 0 },
                { text: "Fairly good", value: 1 },
                { text: "Fairly bad", value: 2 },
                { text: "Very bad", value: 3 }
            ],
            key: 'sleep'
        },
        {
            question: "How connected do you feel to other people right now?",
            options: [
                { text: "Very connected", value: 0 },
                { text: "Somewhat connected", value: 1 },
                { text: "Not very connected", value: 2 },
                { text: "Not at all connected", value: 3 }
            ],
            key: 'social'
        },
        {
            question: "How often have you been feeling nervous, anxious, or on edge?",
            options: [
                { text: "Not at all", value: 0 },
                { text: "Several days", value: 1 },
                { text: "More than half the days", value: 2 },
                { text: "Nearly every day", value: 3 }
            ],
            key: 'anxiety'
        },
        {
            question: "How would you describe your energy levels recently?",
            options: [
                { text: "Very high", value: 0 },
                { text: "About normal", value: 1 },
                { text: "Low", value: 2 },
                { text: "Very low", value: 3 }
            ],
            key: 'energy'
        }
    ];

    function buildQuiz() {
        questions.forEach((currentQuestion, questionNumber) => {
            const questionDiv = document.createElement('div');
            questionDiv.classList.add('question');

            const questionText = document.createElement('p');
            questionText.innerText = `${questionNumber + 1}. ${currentQuestion.question}`;
            questionDiv.appendChild(questionText);

            const optionsDiv = document.createElement('div');
            optionsDiv.classList.add('options');

            currentQuestion.options.forEach((option, index) => {
                const label = document.createElement('label');
                const input = document.createElement('input');
                input.type = 'radio';
                input.name = `question${questionNumber}`;
                input.value = option.value;
                // Store the key in the dataset
                input.dataset.key = currentQuestion.key;
                label.appendChild(input);
                label.append(` ${option.text}`);
                optionsDiv.appendChild(label);
            });

            questionDiv.appendChild(optionsDiv);
            quizContainer.appendChild(questionDiv);
        });
    }

    function showResults() {
        const answerContainers = quizContainer.querySelectorAll('.options');
        let score = 0;
        let allAnswered = true;
        const userAnswers = {};

        questions.forEach((currentQuestion, questionNumber) => {
            const answerContainer = answerContainers[questionNumber];
            const selector = `input[name=question${questionNumber}]:checked`;
            const userAnswer = (answerContainer.querySelector(selector) || {});
            
            if (userAnswer.value === undefined) {
                allAnswered = false;
                return;
            }
            score += parseInt(userAnswer.value);
            userAnswers[userAnswer.dataset.key] = parseInt(userAnswer.value);
        });

        if (!allAnswered) {
            resultContainer.innerHTML = "<p>Please answer all questions before submitting.</p>";
            resultContainer.style.color = 'red';
            return;
        }

        resultContainer.style.color = '#fff';
        let resultHTML = '';

        if (score <= 4) {
            resultHTML = `<h3>Vibe Check: You're doing great! ✨</h3>`;
            resultHTML += `<p>Your score of ${score} suggests you're in a good headspace. Keep shining!</p>`;
            resultHTML += `<h4>Here are some tips to maintain your positive vibe:</h4>`;
            resultHTML += `<ul>`;
            resultHTML += `<li><strong>Keep moving:</strong> A little exercise can boost your mood.</li>`;
            resultHTML += `<li><strong>Stay connected:</strong> Spend time with people who lift you up.</li>`;
            resultHTML += `<li><strong>Practice gratitude:</strong> Take a moment each day to appreciate the good things.</li>`;
            resultHTML += `</ul>`;
        } else if (score <= 8) {
            resultHTML = `<h3>Vibe Check: A little self-care could help. 💖</h3>`;
            resultHTML += `<p>Your score of ${score} suggests you might be feeling a bit off. That's okay, everyone has those days.</p>`;
            resultHTML += `<h4>Here are some things you can try:</h4>`;
            resultHTML += `<ul>`;
            if (userAnswers.sleep > 1) {
                resultHTML += `<li><strong>Prioritize sleep:</strong> Try to get 7-9 hours of quality sleep. A consistent sleep schedule can make a big difference.</li>`;
            }
            if (userAnswers.social > 1) {
                resultHTML += `<li><strong>Reach out:</strong> Connect with a friend or family member. A good conversation can be really helpful.</li>`;
            }
            if (userAnswers.anxiety > 1) {
                resultHTML += `<li><strong>Try mindfulness:</strong> A few minutes of deep breathing or meditation can help calm your mind.</li>`;
            }
            resultHTML += `<li><strong>Do something you enjoy:</strong> Make time for a hobby or activity that makes you happy.</li>`;
            resultHTML += `</ul>`;
        } else {
            resultHTML = `<h3>Vibe Check: It's okay to not be okay. Reach out. ❤️</h3>`;
            resultHTML += `<p>Your score of ${score} suggests you might be going through a tough time. Please know that you're not alone and help is available.</p>`;
            resultHTML += `<h4>It's important to talk to someone you trust. Here are some resources:</h4>`;
            resultHTML += `<ul>`;
            resultHTML += `<li><strong>Talk to a friend or family member.</strong></li>`;
            resultHTML += `<li><strong>Consider professional help:</strong> A therapist can provide you with tools and support to navigate what you're feeling.</li>`;
            resultHTML += `<li><strong>Crisis Text Line:</strong> Text HOME to 741741 from anywhere in the US, anytime, about any type of crisis.</li>`;
            resultHTML += `<li><strong>The Trevor Project:</strong> 1-866-488-7386</li>`;
            resultHTML += `</ul>`;
        }
        resultContainer.innerHTML = resultHTML;
    }

    buildQuiz();
    submitButton.addEventListener('click', showResults);
});

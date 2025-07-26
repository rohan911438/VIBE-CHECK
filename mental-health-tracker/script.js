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
                const input = document.createElement('input');
                input.type = 'radio';
                input.name = `question${questionNumber}`;
                input.value = option.value;
                input.id = `question${questionNumber}-option${index}`;
                input.dataset.key = currentQuestion.key;

                const label = document.createElement('label');
                label.htmlFor = `question${questionNumber}-option${index}`;
                label.textContent = option.text;

                optionsDiv.appendChild(input);
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
            resultHTML = `<h3>Vibe Check: All Good, Fam! ✨</h3>`;
            resultHTML += `<p>Your score of ${score} means your mental game is strong. Keep that energy up, you're crushing it!</p>`;
            resultHTML += `<h4>Here are some tips to maintain your positive vibe:</h4>`;
            resultHTML += `<ul>`;
            resultHTML += `<li><strong>Keep moving:</strong> A little exercise can boost your mood, for real.</li>`;
            resultHTML += `<li><strong>Stay connected:</strong> Hang out with your squad who lift you up.</li>`;
            resultHTML += `<li><strong>Practice gratitude:</strong> Take a moment each day to appreciate the good things. You got this!</li>`;
            resultHTML += `</ul>`;
        } else if (score <= 8) {
            resultHTML = `<h3>Vibe Check: Time for some self-care, maybe? 💖</h3>`;
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
            resultHTML = `<h3>Vibe Check: It's okay to not be okay, seriously. ❤️</h3>`;
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
        resultContainer.innerHTML = resultHTML;
    }

    buildQuiz();
    submitButton.addEventListener('click', showResults);
});

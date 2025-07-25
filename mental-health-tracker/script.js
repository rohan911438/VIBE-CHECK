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
            ]
        },
        {
            question: "How would you rate your sleep quality over the past week?",
            options: [
                { text: "Very good", value: 0 },
                { text: "Fairly good", value: 1 },
                { text: "Fairly bad", value: 2 },
                { text: "Very bad", value: 3 }
            ]
        },
        {
            question: "How connected do you feel to other people right now?",
            options: [
                { text: "Very connected", value: 0 },
                { text: "Somewhat connected", value: 1 },
                { text: "Not very connected", value: 2 },
                { text: "Not at all connected", value: 3 }
            ]
        },
        {
            question: "How often have you been feeling nervous, anxious, or on edge?",
            options: [
                { text: "Not at all", value: 0 },
                { text: "Several days", value: 1 },
                { text: "More than half the days", value: 2 },
                { text: "Nearly every day", value: 3 }
            ]
        },
        {
            question: "How would you describe your energy levels recently?",
            options: [
                { text: "Very high", value: 0 },
                { text: "About normal", value: 1 },
                { text: "Low", value: 2 },
                { text: "Very low", value: 3 }
            ]
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

        questions.forEach((currentQuestion, questionNumber) => {
            const answerContainer = answerContainers[questionNumber];
            const selector = `input[name=question${questionNumber}]:checked`;
            const userAnswer = (answerContainer.querySelector(selector) || {}).value;

            if (userAnswer === undefined) {
                allAnswered = false;
                return;
            }
            score += parseInt(userAnswer);
        });

        if (!allAnswered) {
            resultContainer.innerText = "Please answer all questions before submitting.";
            resultContainer.style.color = 'red';
            return;
        }

        resultContainer.style.color = '#333';
        if (score <= 4) {
            resultContainer.innerText = `Your result suggests your mental health is in a good place. Keep up the healthy habits! (Score: ${score})`;
        } else if (score <= 8) {
            resultContainer.innerText = `Your result suggests your mental health could use some attention. Consider talking to someone or practicing self-care. (Score: ${score})`;
        } else {
            resultContainer.innerText = `Your result suggests you may be struggling. It's strongly recommended to seek help from a mental health professional. (Score: ${score})`;
        }
    }

    buildQuiz();
    submitButton.addEventListener('click', showResults);
});

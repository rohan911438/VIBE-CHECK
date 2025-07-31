

# Vibe Check: Mental Wellness Platform

> **A modern, Gen Z-focused full-stack web and data science project for mental wellness assessment, stress prediction, and actionable self-care.**

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture & File Structure](#architecture--file-structure)
- [Setup & Usage](#setup--usage)
- [Backend API](#backend-api)
- [Technologies Used](#technologies-used)
- [Deployment](#deployment)
- [Future Plans](#future-plans)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

---

## Project Overview

**Vibe Check** is a comprehensive, full-stack mental wellness platform designed for Gen Z and young adults. It features:
- A stylish, privacy-first web application for instant mental health self-assessment
- Gamification: quiz history, streaks, and badges (all client-side)
- A Node.js/Express backend for storing quiz results and enabling future features like user accounts and analytics
- Data science scripts and models for stress prediction and feature analysis

The project aims to break the stigma around mental health by making check-ins fun, accessible, and data-driven.

**Disclaimer:** This tool is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. If you are experiencing mental health difficulties, please seek help from a qualified professional.

---

## Features


### Web Application (Frontend)
- **Landing Page:** Modern, mobile-friendly landing/about page (`landing.html`)
- **Personalized Welcome:** Users enter their name for a custom experience
- **Engaging Quiz:** 5-question interactive quiz covering mood, sleep, social connection, anxiety, and energy
- **Gamification:** Quiz history, daily streaks, and badges (tracked in localStorage)
- **Dynamic Design:** Black & blue Gen Z aesthetic, responsive for all devices
- **Instant Feedback:** Immediate results with clear, friendly messaging
- **Personalized Recommendations:** Tailored self-care tips and resources based on quiz results
- **Privacy-First:** 100% client-side, no data leaves your browser unless backend is enabled

### Backend (Node.js/Express)
- **REST API:** Store and retrieve quiz results (see [Backend API](#backend-api))
- **Simple JSON storage:** Easy to upgrade to a real database (MongoDB, PostgreSQL, etc.)
- **CORS enabled:** Ready for frontend-backend integration

### Data Science & Stress Prediction
- **Machine Learning Model:** Predicts stress levels from lifestyle/health data (see `models/` and `src/main/python/`)
- **Feature Analysis:** Tools for analyzing and backtesting model features
- **Preprocessed Datasets:** Cleaned and ready-to-use data for further research

### Extensible & Documented
- **Modular Codebase:** Easy to extend for new features (user accounts, gamification, etc.)
- **Detailed Roadmap:** See [`expectation.txt`](expectation.txt) for future plans
- **Well-Documented:** Inline comments and separate documentation in [`docs/`](docs/)

---

## Architecture & File Structure

```
VIBE-CHECK/
│
├── mental-health-tracker/         # Web app (HTML/CSS/JS)
│   ├── index.html                 # Main UI
│   ├── script.js                  # Quiz logic & recommendations
│   └── style.css                  # Modern, responsive styling
│
├── data/
│   ├── raw/                       # Original datasets
│   └── processed/                 # Cleaned/engineered data for ML
│
├── models/                        # Trained ML models & feature configs
│   ├── stress_prediction_model.pkl
│   ├── model_columns.pkl
│   └── feature_defaults.pkl
│
├── src/main/python/               # Data science & ML scripts
│   ├── train_stress_model.py      # Model training
│   ├── advanced_stress_predictor.py
│   ├── analyze_features.py        # Feature analysis
│   └── backtest_model.py          # Model validation
│
├── tests/                         # Unit tests for ML code
│   └── test_predictor.py
│
├── docs/                          # Documentation & enhancement plans
│   ├── README.md
│   └── future_enhancements.md
│
├── expectation.txt                # Detailed roadmap & requirements
├── requirements.txt               # Python dependencies
├── train_model.py                 # Script to train ML model
└── README.md                      # (This file)
```

---


## Setup & Usage

### 1. Web Application (Frontend)

**Quick Start:**
1. Clone or download this repository
2. Open `mental-health-tracker/landing.html` in your web browser (or deploy as a static site)
3. Click "Start the Quiz" to use the app

**No installation or server required for static mode!**

### 2. Backend Server (Optional, for full-stack features)

**Requirements:** Node.js 18+

**To run the backend locally:**
1. Open a terminal and navigate to `server/`
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the server:
   ```bash
   npm start
   ```
   The backend will run on [http://localhost:3001](http://localhost:3001)

### 3. Data Science & Stress Prediction

**Requirements:** Python 3.8+, see `requirements.txt`

**To train or use the stress prediction model:**
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run model training or prediction scripts in `src/main/python/` or `train_model.py`
3. Use the provided datasets in `data/` and models in `models/`

**Testing:**
Run unit tests with:
```bash
python -m unittest discover tests
```

---

## Backend API

The backend provides a simple REST API for quiz results:

- `GET /api/results` — Get all quiz results
- `POST /api/results` — Add a new quiz result (JSON: `{ name, date, score }`)

See `server/README.md` for more details.

---

---

## Technologies Used

### Web Frontend
- **HTML5**: Semantic, accessible markup
- **CSS3**: Responsive, modern styling (Poppins font, dark/blue theme)
- **JavaScript (ES6+)**: Quiz logic, dynamic UI, recommendations
- **Font Awesome**: Iconography
- **Google Fonts (Poppins)**: Typography

### Data Science & Backend
- **Python 3.8+**: Core language for ML
- **pandas, scikit-learn, numpy**: Data processing & machine learning
- **pickle**: Model serialization
- **Jupyter Notebook** (optional): For EDA and prototyping

---


## Deployment

### Static Frontend (Recommended for GitHub Pages, Vercel, Netlify)
- Deploy the contents of `mental-health-tracker/` as your site root
- Set `landing.html` as the entry point (rename to `index.html` if needed)
- All features except backend integration will work out-of-the-box

### Full-Stack (Backend + Frontend)
- Deploy the backend (Node.js/Express) to a cloud service (e.g., Render, Heroku, Railway, AWS, etc.)
- Update the frontend JS to point to your deployed backend API URL
- For production, use a real database (MongoDB, PostgreSQL, etc.) instead of the local JSON file

---

## Future Plans

See [`expectation.txt`](expectation.txt) for a detailed roadmap, including:
- User accounts & personalization (registration, login, quiz history sync)
- More dynamic/interactive quiz types (animations, sliders, drag-and-drop)
- Community & social features (anonymous sharing, forums, curated content)
- Gamification (streaks, badges, leaderboards, rewards)
- Integration with wearables/health apps (Google Fit, Apple Health)
- Multilingual support (Hindi, English, regional languages)
- Accessibility improvements
- Scalability, security, and performance enhancements
- Admin dashboard and analytics
- Mobile app version

---

---

## Contributing

Contributions are welcome! To suggest features, report bugs, or submit pull requests:
1. Fork the repository
2. Create a new branch for your feature/fix
3. Submit a pull request with a clear description

For major changes, please open an issue first to discuss what you would like to change.

---

## Author

- **Name:** Rohan Kumar
- **GitHub:** [rohan911438](https://github.com/rohan911438)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

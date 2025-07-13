# Advanced Stress & Well-being Monitor

## 1. Project Overview

This project provides a sophisticated, data-driven tool designed to help individuals monitor, understand, and manage their daily stress levels. It leverages a machine learning model to predict stress based on various physiological and lifestyle factors, offering personalized insights and actionable advice.

## 2. Key Features

*   **Machine Learning-Powered Stress Prediction:** Utilizes a Random Forest Regressor model, trained on comprehensive health and lifestyle data, to predict a numerical stress score (0-10) and a categorical stress level (Low, Medium, High, Very High).
*   **Personalized & Actionable Advice:** Generates descriptive and tailored recommendations based on the predicted stress level and specific user inputs, guiding users toward better well-being.
*   **Comprehensive Data Logging:** Systematically records daily user inputs and predicted stress outcomes into a structured CSV file (`stress_data.csv`), enabling continuous monitoring and future model refinement.
*   **Model Backtesting Capability:** Includes a dedicated script to evaluate the model's performance on historical data, ensuring reliability and consistency of predictions.
*   **Robust Error Handling & Logging:** Implements professional-grade error handling and logging mechanisms across all scripts, enhancing stability, maintainability, and ease of debugging.
*   **Modular and Professional Backend Structure:** Organized into a clear, scalable directory structure, separating source code, data, models, and documentation, suitable for larger projects.

## 3. Project Structure

The project follows a standard, organized directory layout:

```
Stress prediction/
├───src/                  # Source code for the application
│   ├───main/             # Main application logic
│   │   ├───python/       # Python source files
│   │   │   ├───advanced_stress_predictor.py  # Main script for daily stress prediction
│   │   │   ├───train_stress_model.py       # Script to train the stress prediction model
│   │   │   ├───backtest_model.py           # Script for backtesting the model
│   │   │   └───analyze_features.py         # Script to analyze model feature importances
├───data/                 # Data storage
│   ├───raw/              # Raw, untransformed datasets
│   │   ├───Sleep_health_and_lifestyle_dataset.csv
│   ├───processed/        # Processed or generated data (e.g., logged user data)
│   │   └───stress_data.csv
├───models/               # Trained machine learning models and related artifacts
│   ├───stress_prediction_model.pkl
│   │   ├───model_columns.pkl
│   │   └───feature_defaults.pkl
├───tests/                # Unit and integration tests
│   └───test_predictor.py
├───docs/                 # Project documentation
│   └───README.md         # This file
├───.gitignore            # Specifies intentionally untracked files to ignore
├───requirements.txt      # Python dependencies
```

## 4. Setup and Installation

To get this project up and running on your local machine, follow these steps:

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd "Stress prediction"
    ```
    (Replace `<repository_url>` with the actual URL of your repository.)

2.  **Install dependencies:**
    Navigate to the root directory of the cloned repository and install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## 5. Usage

### 5.1. Training the Stress Prediction Model

Before using the `advanced_stress_predictor.py` or `backtest_model.py`, you should train the model. This script will generate `stress_prediction_model.pkl`, `model_columns.pkl`, and `feature_defaults.pkl` in the `models/` directory.

```bash
python src/main/python/train_stress_model.py
```

### 5.2. Daily Stress Prediction

Run the main script to input your daily metrics and get a personalized stress analysis:

```bash
python src/main/python/advanced_stress_predictor.py
```

Follow the on-screen prompts to enter the required information.

### 5.3. Model Backtesting

To evaluate the model's performance on historical data (from `data/processed/stress_data.csv`):

```bash
python src/main/python/backtest_model.py
```

This will output a summary of predictions and advice for each entry in your logged data.

### 5.4. Analyzing Feature Importances

To understand which features contribute most to the model's predictions:

```bash
python src/main/python/analyze_features.py
```

## 6. User Input Requirements (for `advanced_stress_predictor.py`)

To generate your daily analysis, the script will prompt you for the following information. Please provide numerical answers where applicable.

| Input                      | Description                                                                 |
| :------------------------- | :-------------------------------------------------------------------------- |
| **Age**                    | Your current age (integer).                                                 |
| **Gender**                 | Your gender (Male/Female).                                                  |
| **Sleep Duration**         | How many hours you slept last night (float).                                |
| **Quality of Sleep (1-10)**| Your quality of sleep on a scale of 1-10 (integer).                         |
| **Sleep Disorder**         | Do you have a sleep disorder? (None, Sleep Apnea, Insomnia).                |
| **Physical Activity Level**| How many hours you spent exercising today (float).                          |
| **Heart Rate**             | Your average heart rate today in beats per minute (float).                  |
| **Daily Steps**            | Your daily steps count (integer).                                           |
| **Systolic BP**            | Your systolic blood pressure (e.g., 120 for 120/80) (float).                |
| **Diastolic BP**           | Your diastolic blood pressure (e.g., 80 for 120/80) (float).                |
| **BMI Category**           | Your BMI category (Normal, Overweight, Obese, Normal Weight).               |
| **Occupation**             | Your occupation (e.g., Software Engineer, Doctor).                          |

## 7. Output Description

After you provide your inputs, the `advanced_stress_predictor.py` script will produce the following:

1.  **Your Personalized Analysis:**
    *   **Predicted Stress Score:** A numerical score from 0 to 10, indicating your stress level.
    *   **Predicted Stress Level:** A categorical level (Low, Medium, High, or Very High) derived from the score.
    *   **Personalized Advice:** A detailed, actionable recommendation based on your predicted stress level and specific inputs, designed to help you manage or reduce stress.

2.  **Data Log Confirmation:**
    *   A confirmation message stating that your data for the day has been successfully saved to `data/processed/stress_data.csv`.

## 8. Logging

All scripts utilize Python's `logging` module to provide detailed information about their execution, including errors, warnings, and key operational steps. This output is printed to the console.

## 9. Contributing

Contributions are welcome! If you have suggestions for improvements, bug fixes, or new features, please feel free to open an issue or submit a pull request.
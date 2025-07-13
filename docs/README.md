# Advanced Stress & Well-being Monitor

## 1. The Core Idea

This project is a personalized, data-driven tool designed to help you monitor and understand your daily stress levels. It has evolved from a heuristic model to a more accurate **machine learning model** for predicting stress.

The primary goal is two-fold:
1.  **Immediate Insight:** To give you a daily snapshot of your stress level based on key physiological and lifestyle factors.
2.  **Continuous Improvement:** To systematically log your inputs into a `stress_data.csv` file, which can be used for future model retraining and even more accurate and personalized predictions.

---

## 2. How It Works

The script now uses a **machine learning model** (Random Forest Regressor) trained on a comprehensive dataset (`Sleep_health_and_lifestyle_dataset.csv`). This model predicts your stress level based on the inputs you provide.

- **Inputs:** It collects essential data points about your day, focusing on factors scientifically correlated with stress.
- **Machine Learning Prediction:** The trained model analyzes your inputs to generate a precise stress score.
-   **Data Logging:** Every entry is saved with a timestamp to `stress_data.csv`, creating a valuable personal dataset for future analysis and model refinement.

---

## 3. User Input Requirements

To generate your daily analysis, the script will prompt you for the following information. Please provide numerical answers where applicable.

| Input                      | Description                                             |
| :------------------------- | :------------------------------------------------------ |
| **Age**                    | Your current age.                                       |
| **Gender**                 | Your gender (Male/Female).                              |
| **Sleep hours**            | How many hours you slept last night.                    |
| **Sleep quality (1-10)**   | Your quality of sleep on a scale of 1-10.               |
| **Exercise hours**         | How many hours you spent exercising.                    |
| **Heart rate**             | Your average heart rate.                                |
| **Daily steps**            | Your daily steps count.                                 |
| **Systolic BP**            | Your systolic blood pressure (e.g., 120 for 120/80).    |
| **Diastolic BP**           | Your diastolic blood pressure (e.g., 80 for 120/80).    |
| **Occupation**             | Your occupation (e.g., Software Engineer, Doctor).      |
| **BMI category**           | Your BMI category (Normal, Overweight, Obese, Normal Weight). |
| **Sleep disorder**         | Do you have a sleep disorder? (None, Sleep Apnea, Insomnia). |

---

## 4. Desired Output

After you provide your inputs, the script will produce the following output:

1.  **Your Personalized Analysis:**
    -   **Predicted Stress Score:** A numerical score from 0 to 10.
    -   **Predicted Stress Level:** A categorical level (Low, Medium, High, or Very High).
    -   **Personalized Advice:** A brief, actionable recommendation based on your predicted stress level.

2.  **Data Log Confirmation:**
    -   A confirmation message stating that your data for the day has been successfully saved to `stress_data.csv`.

---

## 5. How to Run the Script

1.  Ensure you have Python installed.
2.  Open a terminal or command prompt.
3.  Navigate to the directory where the script is saved.
4.  Run the following command:
    ```sh
    python advanced_stress_predictor.py
    ```
5.  Follow the on-screen prompts to enter your daily metrics.
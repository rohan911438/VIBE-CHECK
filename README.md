
# Advanced Stress & Well-being Monitor

## 1. The Core Idea

This project is a personalized, data-driven tool designed to help you monitor and understand your daily stress levels. It moves beyond simple rules and uses a more realistic, weighted scoring system to provide a nuanced analysis of your well-being.

The primary goal is two-fold:
1.  **Immediate Insight:** To give you a daily snapshot of your stress level based on your activities and mood.
2.  **Long-Term Data Collection:** To systematically log your inputs into a `stress_data.csv` file. Over time, this data can be used to train a genuine machine learning model for even more accurate and personalized predictions.

---

## 2. How It Works

The script uses a **heuristic model** based on established well-being principles:

- **Inputs:** It collects multiple data points about your day, including sleep, work, exercise, and social habits.
- **Weighted Scoring:** Each input is assigned a weight based on its typical impact on stress. For example, lack of sleep has a heavier negative impact than high caffeine intake. Positive activities like exercise and socializing reduce the score.
- **Data Logging:** Every entry is saved with a timestamp to `stress_data.csv`, creating a valuable personal dataset for future analysis.

---

## 3. User Input Requirements

To generate your daily analysis, the script will prompt you for the following information. Please provide numerical answers for all inputs.

| Input                  | Description                                             | Example |
| ---------------------- | ------------------------------------------------------- | ------- |
| **Sleep Hours**        | How many hours you slept last night.                    | `8`       |
| **Work Hours**         | How many hours you worked today.                        | `7.5`     |
| **Exercise Hours**     | How many hours you spent exercising.                    | `1`       |
| **Caffeine (mg)**      | Your estimated caffeine intake in milligrams.           | `95`      |
| **Social Hours**       | Hours spent actively socializing with friends/family.   | `2`       |
| **Social Media Hours** | Hours spent on social media platforms.                  | `1.5`     |
| **Outing Hours**       | Hours spent on leisure activities or outings.           | `3`       |
| **Mood Rating**        | Your mood on a scale of 1-10, based on the list provided. | `8`       |

### Mood Scale Reference

- **10:** Excellent, very calm and positive
- **9:** Great, feeling very good
- **8:** Good, positive and capable
- **7:** Fine, generally okay
- **6:** Alright, slightly uneasy
- **5:** Neutral, neither good nor bad
- **4:** A bit down or irritable
- **3:** Stressed and somewhat overwhelmed
- **2:** Very stressed and anxious
- **1:** Extremely overwhelmed or upset

---

## 4. Desired Output

After you provide your inputs, the script will produce the following output:

1.  **Your Personalized Analysis:**
    - **Today's Mood:** The descriptive mood you selected (e.g., "Good, positive and capable").
    - **Calculated Stress Score:** A numerical score from 0 to 100.
    - **Predicted Stress Level:** A categorical level (Low, Medium, High, or Very High).
    - **Personalized Advice:** A brief, actionable recommendation based on your stress level.

2.  **Data Log Confirmation:**
    - A confirmation message stating that your data for the day has been successfully saved to `stress_data.csv`.

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

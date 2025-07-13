import csv
import os
import datetime
import joblib
import pandas as pd

DATA_FILE = 'stress_data.csv'
FILE_HEADERS = [
    'date', 'Age', 'Gender', 'Sleep Duration', 'Quality of Sleep', 'Sleep Disorder',
    'Physical Activity Level', 'Heart Rate', 'Daily Steps', 'Systolic_BP', 'Diastolic_BP',
    'BMI Category', 'Occupation', 'stress_score', 'stress_level'
]

# Load the trained model, columns, and feature defaults
try:
    model = joblib.load('stress_prediction_model.pkl')
    expected_model_columns = joblib.load('model_columns.pkl')
    feature_defaults = joblib.load(os.path.join('models', 'feature_defaults.pkl'))
except FileNotFoundError:
    print("Error: Required model files (stress_prediction_model.pkl, model_columns.pkl, or feature_defaults.pkl) not found. Please run train_stress_model.py first.")
    exit()
except Exception as e:
    print(f"An error occurred loading model files: {e}")
    exit()

def get_user_input():
    """Gathers daily metrics from the user in a conversational way."""
    print("\n--- Let's talk about your day to understand your stress level ---")
    try:
        age = int(input("First, what is your current age? "))
        gender = input("What is your gender? (Male/Female) ")

        print("\nNext, let's talk about your sleep.")
        sleep_hours = float(input("How many hours did you sleep last night? "))
        sleep_quality = int(input("And how would you rate the quality of that sleep on a scale from 1 to 10? "))
        sleep_disorder = input("Do you have a sleep disorder? (None, Sleep Apnea, Insomnia) ")

        print("\nNow, tell me about your physical health and daily activities.")
        exercise_hours = float(input("How many hours did you spend exercising today? "))
        heart_rate = float(input("What was your average heart rate today (beats per minute)? "))
        daily_steps = int(input("How many steps did you take today? "))
        systolic_bp = float(input("What was your systolic blood pressure (e.g., 120 for 120/80)? "))
        diastolic_bp = float(input("What was your diastolic blood pressure (e.g., 80 for 120/80)? "))
        bmi_category = input("What is your BMI category? (Normal, Overweight, Obese, Normal Weight) ")

        occupation = input("Finally, what is your current occupation or role? (e.g., Software Engineer, Doctor) ")

        inputs = {
            'Age': age,
            'Gender': gender,
            'Sleep Duration': sleep_hours,
            'Quality of Sleep': sleep_quality,
            'Sleep Disorder': sleep_disorder,
            'Physical Activity Level': exercise_hours,
            'Heart Rate': heart_rate,
            'Daily Steps': daily_steps,
            'Systolic_BP': systolic_bp,
            'Diastolic_BP': diastolic_bp,
            'BMI Category': bmi_category,
            'Occupation': occupation
        }
        return inputs
    except ValueError:
        print("\nError: Invalid input. Please ensure you enter numbers for age, hours, ratings, heart rate, steps, and blood pressure.")
        return None

def get_age_group(age):
    # Helper to determine age group, matching bins in train_stress_model.py
    if 0 <= age <= 9:
        return '0-9'
    elif 10 <= age <= 19:
        return '10-19'
    elif 20 <= age <= 29:
        return '20-29'
    elif 30 <= age <= 39:
        return '30-39'
    elif 40 <= age <= 49:
        return '40-49'
    elif 50 <= age <= 59:
        return '50-59'
    elif 60 <= age <= 69:
        return '60-69'
    elif 70 <= age <= 79:
        return '70-79'
    elif 80 <= age <= 89:
        return '80-89'
    else:
        return '90-99' # Or handle as an outlier/error

def prepare_input_for_prediction(user_inputs, expected_columns, feature_defaults):
    model_features = {}

    # Directly use user-provided inputs
    model_features['Age'] = user_inputs['Age']
    model_features['Gender'] = user_inputs['Gender']
    model_features['Sleep Duration'] = user_inputs['Sleep Duration']
    model_features['Quality of Sleep'] = user_inputs['Quality of Sleep']
    model_features['Physical Activity Level'] = user_inputs['Physical Activity Level']
    model_features['Heart Rate'] = user_inputs['Heart Rate']
    model_features['Daily Steps'] = user_inputs['Daily Steps']
    model_features['Systolic_BP'] = user_inputs['Systolic_BP']
    model_features['Diastolic_BP'] = user_inputs['Diastolic_BP']
    model_features['Occupation'] = user_inputs['Occupation']
    model_features['BMI Category'] = user_inputs['BMI Category']
    model_features['Sleep Disorder'] = user_inputs['Sleep Disorder']

    # Create a DataFrame from the collected features
    input_df = pd.DataFrame([model_features])

    # One-hot encode categorical features, ensuring drop_first=True matches training
    categorical_cols = ['Gender', 'Occupation', 'BMI Category', 'Sleep Disorder']
    input_df_encoded = pd.get_dummies(input_df, columns=categorical_cols, drop_first=True)

    # Align columns with the training data (expected_columns)
    # Add missing columns with 0
    for col in expected_columns:
        if col not in input_df_encoded.columns:
            input_df_encoded[col] = 0
    
    # Ensure the order of columns is the same as during training
    input_df_aligned = input_df_encoded[expected_columns]

    return input_df_aligned

def get_stress_level_and_advice(stress_score, user_inputs):
    """Determines stress level and provides tailored advice based on a numerical score and user inputs."""
    advice = []
    level = ""

    if stress_score >= 8:
        level = "Very High"
        advice.append("Your stress levels are very high. This indicates a critical need for immediate action. Consider taking a break, reaching out to a mental health professional, or delegating tasks to reduce your burden. Prioritize self-care above all else.")
    elif stress_score >= 6:
        level = "High"
        advice.append("You are experiencing a high level of stress. It's crucial to address this. Focus on stress-reducing activities like mindfulness, deep breathing exercises, or light physical activity. Ensure you're taking regular breaks throughout your day.")
    elif stress_score >= 4:
        level = "Medium"
        advice.append("Your stress levels are moderate. This is a good time to implement proactive strategies. Consider incorporating more relaxation into your routine, such as reading, listening to music, or spending time in nature. Evaluate your daily schedule for areas where you can reduce pressure.")
    else:
        level = "Low"
        advice.append("Your stress levels are low, which is great! You're managing well. Continue with your healthy habits, and perhaps explore new ways to maintain this balance, such as learning a new skill or engaging in a hobby.")

    # Personalized advice based on user inputs
    if user_inputs.get('Sleep Duration', 0) < 7:
        advice.append("You reported less than 7 hours of sleep. Insufficient sleep is a major contributor to stress. Aim for 7-9 hours of quality sleep per night. Establish a consistent sleep schedule, create a relaxing bedtime routine, and ensure your sleep environment is conducive to rest.")
    if user_inputs.get('Quality of Sleep', 0) < 5:
        advice.append("Your sleep quality is on the lower side. Poor sleep quality can significantly impact stress. Focus on improving your sleep hygiene, such as maintaining a consistent sleep schedule, creating a comfortable sleep environment, and avoiding caffeine before bed.")
    if user_inputs.get('Physical Activity Level', 0) == 0:
        advice.append("You reported no physical activity. Regular exercise is a powerful stress reliever. Even short walks can make a difference. Aim for at least 30 minutes of moderate exercise most days of the week.")
    
    return level, " ".join(advice)

def log_data(inputs, predicted_score, level):
    """Logs the daily entry to a CSV file."""
    file_exists = os.path.isfile(DATA_FILE)

    with open(DATA_FILE, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FILE_HEADERS)

        if not file_exists:
            writer.writeheader() # Write header only if file is new

        # Prepare data for logging, including original inputs and predicted values
        log_entry = {
            'date': datetime.date.today().isoformat(),
            'Age': inputs['Age'],
            'Gender': inputs['Gender'],
            'Sleep Duration': inputs['Sleep Duration'],
            'Quality of Sleep': inputs['Quality of Sleep'],
            'Sleep Disorder': inputs['Sleep Disorder'],
            'Physical Activity Level': inputs['Physical Activity Level'],
            'Heart Rate': inputs['Heart Rate'],
            'Daily Steps': inputs['Daily Steps'],
            'Systolic_BP': inputs['Systolic_BP'],
            'Diastolic_BP': inputs['Diastolic_BP'],
            'BMI Category': inputs['BMI Category'],
            'Occupation': inputs['Occupation'],
            'stress_score': f"{predicted_score:.2f}",
            'stress_level': level
        }
        writer.writerow(log_entry)
    print(f"\nSuccessfully logged your data to {DATA_FILE}")

def main():
    print("--- Advanced Stress & Well-being Monitor ---")
    print("This tool uses a machine learning model to predict your stress level.")

    user_inputs = get_user_input()

    if user_inputs:
        processed_input = prepare_input_for_prediction(user_inputs, expected_model_columns, feature_defaults)

        # Predict stress score using the loaded model
        predicted_stress_score = model.predict(processed_input)[0]

        # Determine stress level and advice based on the predicted score
        stress_level, advice = get_stress_level_and_advice(predicted_stress_score, user_inputs)

        print("\n--- Your Personalized Analysis ---")
        print(f"Predicted Stress Score: {predicted_stress_score:.2f} / 10") # Model predicts on a scale of 0-10
        print(f"Predicted Stress Level: {stress_level}")
        print(f"Personalized Advice: {advice}")
        print("-------------------------------------")

        # Log all original user inputs along with the predicted stress score and level
        log_data(user_inputs, predicted_stress_score, stress_level)


if __name__ == "__main__":
    main()
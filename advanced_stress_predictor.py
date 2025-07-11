import csv
import os
import datetime
import joblib
import pandas as pd

DATA_FILE = 'stress_data.csv'
FILE_HEADERS = [
    'date', 'sleep_hours', 'work_hours', 'exercise_hours', 'caffeine_mg',
    'social_hours', 'social_media_hours', 'outing_hours', 'mood_rating',
    'stress_score', 'stress_level'
]

# Load the trained model and the columns it was trained on
try:
    model = joblib.load('stress_prediction_model.pkl')
    expected_model_columns = joblib.load('model_columns.pkl')
except FileNotFoundError:
    print("Error: Required model files (stress_prediction_model.pkl or model_columns.pkl) not found. Please run train_stress_model.py first.")
    exit()
except Exception as e:
    print(f"An error occurred loading model files: {e}")
    exit()

def get_user_input():
    """Gathers detailed daily metrics from the user."""
    print("\n--- Please Enter Your Daily Metrics ---")
    try:
        inputs = {
            'Age': int(input("Enter your age: ")),
            'Gender': input("Enter your gender (Male/Female): "),
            'Sleep Duration': float(input("How many hours did you sleep? ")),
            'Quality of Sleep': int(input("On a scale of 1-10, how would you rate your quality of sleep? ")),
            'Physical Activity Level': float(input("How many hours did you exercise? ")),
            'Heart Rate': int(input("Enter your average heart rate: ")),
            'Daily Steps': int(input("Enter your daily steps: ")),
            'Systolic_BP': int(input("Enter your systolic blood pressure (e.g., 120 for 120/80): ")),
            'Diastolic_BP': int(input("Enter your diastolic blood pressure (e.g., 80 for 120/80): ")),
            'Occupation': input("Enter your occupation (e.g., Software Engineer, Doctor, Nurse, Salesperson, Teacher, Accountant, Engineer, Scientist, Manager): "),
            'BMI Category': input("Enter your BMI category (Normal, Overweight, Obese, Normal Weight): "),
            'Sleep Disorder': input("Do you have a sleep disorder? (None, Sleep Apnea, Insomnia): ")
        }
        # Additional inputs for logging, not directly used by the current ML model
        inputs['caffeine_mg'] = float(input("Estimated caffeine intake (in mg)? (1 cup of coffee approx 95mg): "))
        inputs['social_hours'] = float(input("How many hours did you spend socializing with friends/family? "))
        inputs['social_media_hours'] = float(input("How many hours did you spend on social media? "))
        inputs['outing_hours'] = float(input("How many hours did you spend on outings/leisure? "))
        inputs['mood_rating'] = int(input("On a scale of 1-10, how would you rate your mood today? "))

        return inputs
    except ValueError as e:
        print(f"\nError: Invalid input. {e}. Please ensure numerical inputs are numbers and others are text.")
        return None

def prepare_input_for_prediction(user_inputs, expected_columns):
    # Create a DataFrame from user inputs for the model's features
    model_input_data = {
        'Age': [user_inputs['Age']],
        'Sleep Duration': [user_inputs['Sleep Duration']],
        'Quality of Sleep': [user_inputs['Quality of Sleep']],
        'Physical Activity Level': [user_inputs['Physical Activity Level']],
        'Heart Rate': [user_inputs['Heart Rate']],
        'Daily Steps': [user_inputs['Daily Steps']],
        'Systolic_BP': [user_inputs['Systolic_BP']],
        'Diastolic_BP': [user_inputs['Diastolic_BP']],
        'Gender': [user_inputs['Gender']],
        'Occupation': [user_inputs['Occupation']],
        'BMI Category': [user_inputs['BMI Category']],
        'Sleep Disorder': [user_inputs['Sleep Disorder']]
    }
    input_df = pd.DataFrame(model_input_data)

    # One-hot encode categorical features
    categorical_cols = ['Gender', 'Occupation', 'BMI Category', 'Sleep Disorder']
    input_df_encoded = pd.get_dummies(input_df, columns=categorical_cols)

    # Align columns with the training data
    # Add missing columns with 0 and reorder to match expected_columns
    for col in expected_columns:
        if col not in input_df_encoded.columns:
            input_df_encoded[col] = 0
    
    # Ensure the order of feature columns matches the training set
    input_df_aligned = input_df_encoded[expected_columns]

    return input_df_aligned

def get_stress_level_and_advice(stress_score):
    """Determines stress level and provides tailored advice based on a numerical score."""
    # Adjust thresholds based on the model's output scale (0-10 for Stress Level in sleep_df)
    if stress_score >= 8:
        return "Very High", "Your stress levels seem very high. Prioritize rest, consider talking to someone, and reduce workload immediately."
    elif stress_score >= 6:
        return "High", "You are likely experiencing significant stress. Focus on improving sleep, exercise, and taking short breaks."
    elif stress_score >= 4:
        return "Medium", "You have a moderate level of stress. Small changes like a short walk or less caffeine can make a big difference."
    else:
        return "Low", "Your stress levels appear low. You are managing well. Keep up the healthy habits!"

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
            'sleep_hours': inputs['Sleep Duration'],
            'work_hours': inputs.get('work_hours', 0), # These are from original heuristic, not directly from sleep_df
            'exercise_hours': inputs['Physical Activity Level'],
            'caffeine_mg': inputs.get('caffeine_mg', 0),
            'social_hours': inputs.get('social_hours', 0),
            'social_media_hours': inputs.get('social_media_hours', 0),
            'outing_hours': inputs.get('outing_hours', 0),
            'mood_rating': inputs.get('mood_rating', 0),
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
        processed_input = prepare_input_for_prediction(user_inputs, expected_model_columns)

        # Predict stress score using the loaded model
        predicted_stress_score = model.predict(processed_input)[0]

        # Determine stress level and advice based on the predicted score
        stress_level, advice = get_stress_level_and_advice(predicted_stress_score)

        print("\n--- Your Personalized Analysis ---")
        print(f"Predicted Stress Score: {predicted_stress_score:.2f} / 10") # Model predicts on a scale of 0-10
        print(f"Predicted Stress Level: {stress_level}")
        print(f"Personalized Advice: {advice}")
        print("-------------------------------------")

        # Log all original user inputs along with the predicted stress score and level
        log_data(user_inputs, predicted_stress_score, stress_level)

if __name__ == "__main__":
    main()

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

# Load the trained model, columns, and feature defaults
try:
    model = joblib.load('stress_prediction_model.pkl')
    expected_model_columns = joblib.load('model_columns.pkl')
    feature_defaults = joblib.load('feature_defaults.pkl')
except FileNotFoundError:
    print("Error: Required model files (stress_prediction_model.pkl, model_columns.pkl, or feature_defaults.pkl) not found. Please run train_stress_model.py first.")
    exit()
except Exception as e:
    print(f"An error occurred loading model files: {e}")
    exit()

def get_user_input():
    """Gathers streamlined daily metrics from the user."""
    print("\n--- Please Enter Your Daily Metrics ---")
    try:
        inputs = {
            'Age': int(input("Age: ")),
            'Gender': input("Gender (Male/Female): "),
            'Sleep Duration': float(input("Sleep hours: ")),
            'Mood Rating': int(input("Mood rating (1-10): "))
        }
        return inputs
    except ValueError as e:
        print(f"\nError: Invalid input. {e}. Please ensure numerical inputs are numbers and others are text.")
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
    # Initialize a dictionary to hold all features for the model
    model_features = {}

    # Directly use user-provided inputs
    model_features['Age'] = user_inputs['Age']
    model_features['Sleep Duration'] = user_inputs['Sleep Duration']
    model_features['Quality of Sleep'] = user_inputs['Mood Rating'] # Using Mood Rating as a proxy for Quality of Sleep
    model_features['Gender'] = user_inputs['Gender'] # Add Gender to model_features

    # Determine age group for inferring defaults
    gender = user_inputs['Gender']
    age_group = get_age_group(user_inputs['Age'])

    # Infer other features using defaults based on Gender and Age_Group
    defaults = feature_defaults.get(gender, {}).get(age_group, {})

    # Populate remaining features, prioritizing defaults if available
    features_to_infer = [
        'Physical Activity Level', 'Heart Rate', 'Daily Steps',
        'Systolic_BP', 'Diastolic_BP', 'Occupation', 'BMI Category', 'Sleep Disorder'
    ]

    for feature in features_to_infer:
        if feature in defaults:
            model_features[feature] = defaults[feature]
        else:
            # Fallback if specific default not found (e.g., for a rare age/gender combo)
            if feature in ['Physical Activity Level', 'Heart Rate', 'Daily Steps', 'Systolic_BP', 'Diastolic_BP']:
                model_features[feature] = 0.0 # Global median or a sensible default
            else: # Categorical
                model_features[feature] = 'Unknown' # Global mode or a sensible default

    # Create a DataFrame from the collected/inferred features
    input_df = pd.DataFrame([model_features])

    # One-hot encode categorical features
    categorical_cols = ['Gender', 'Occupation', 'BMI Category', 'Sleep Disorder']
    input_df_encoded = pd.get_dummies(input_df, columns=categorical_cols)

    # Align columns with the training data
    for col in expected_columns:
        if col not in input_df_encoded.columns:
            input_df_encoded[col] = 0
    
    input_df_aligned = input_df_encoded[expected_columns]

    return input_df_aligned

def get_stress_level_and_advice(stress_score):
    """Determines stress level and provides tailored advice based on a numerical score."""
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
            'work_hours': inputs.get('work_hours', 0), # Defaulted if not asked
            'exercise_hours': inputs.get('Physical Activity Level', 0), # Defaulted if not asked
            'caffeine_mg': inputs.get('caffeine_mg', 0.0),
            'social_hours': inputs.get('social_hours', 0.0),
            'social_media_hours': inputs.get('social_media_hours', 0.0),
            'outing_hours': inputs.get('outing_hours', 0.0),
            'mood_rating': inputs['Mood Rating'],
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
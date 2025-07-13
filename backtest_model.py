import joblib
import pandas as pd
import numpy as np
import os

# Load the trained model, columns, and feature defaults
try:
    model = joblib.load('stress_prediction_model.pkl')
    expected_model_columns = joblib.load('model_columns.pkl')
    feature_defaults = joblib.load('feature_defaults.pkl')
except FileNotFoundError as e:
    print(f"Error: Required model files not found. Please ensure 'stress_prediction_model.pkl', 'model_columns.pkl', and 'feature_defaults.pkl' are in the same directory. Error: {e}")
    exit()
except Exception as e:
    print(f"An error occurred loading model files: {e}")
    exit()

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
        advice.append("You reported no physical activity. Regular physical activity is a powerful stress reliever. Even short walks can make a difference. Aim for at least 30 minutes of moderate exercise most days of the week.")
    
    return level, " ".join(advice)

def main():
    print("--- Backtesting Stress Prediction Model ---")

    # Load stress_data.csv
    try:
        # Create a dummy DataFrame with the new expected columns for backtesting
        # In a real scenario, you would populate this with actual historical data
        # that matches the new input requirements of advanced_stress_predictor.py
        data = {
            'date': ['2025-07-14', '2025-07-15'],
            'Age': [30, 25],
            'Gender': ['Male', 'Female'],
            'Sleep Duration': [6.5, 8.0],
            'Quality of Sleep': [4, 7],
            'Sleep Disorder': ['None', 'Insomnia'],
            'Physical Activity Level': [0.5, 1.0],
            'Heart Rate': [75, 68],
            'Daily Steps': [5000, 10000],
            'Systolic_BP': [120, 110],
            'Diastolic_BP': [80, 70],
            'BMI Category': ['Normal', 'Normal Weight'],
            'Occupation': ['Software Engineer', 'Doctor'],
            'stress_score': [0, 0], # Placeholder, will be overwritten
            'stress_level': ['', ''] # Placeholder, will be overwritten
        }
        stress_data_df = pd.DataFrame(data)

    except Exception as e:
        print(f"An error occurred creating dummy data for backtesting: {e}")
        exit()

    results = []
    for index, row in stress_data_df.iterrows():
        user_inputs = row.to_dict()

        processed_input = prepare_input_for_prediction(user_inputs, expected_model_columns, feature_defaults)
        
        # Predict stress score
        predicted_stress_score = model.predict(processed_input)[0]

        # Get stress level and advice
        stress_level, advice = get_stress_level_and_advice(predicted_stress_score, user_inputs)

        results.append({
            'date': user_inputs['date'],
            'original_stress_score': row['stress_score'],
            'new_predicted_stress_score': f"{predicted_stress_score:.2f}",
            'new_stress_level': stress_level,
            'new_advice': advice
        })

    results_df = pd.DataFrame(results)
    print("\n--- Backtesting Results ---")
    print(results_df.to_string())

    # Optional: Save results to a new CSV
    # results_df.to_csv('backtesting_results.csv', index=False)
    # print("\nBacktesting results saved to 'backtesting_results.csv'")

if __name__ == "__main__":
    main()
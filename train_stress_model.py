import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

# --- Delete stress_predictor.py ---
file_to_delete = "stress_predictor.py"
if os.path.exists(file_to_delete):
    try:
        os.remove(file_to_delete)
        print(f"Successfully deleted {file_to_delete}")
    except OSError as e:
        print(f"Error deleting file {file_to_delete}: {e}")
else:
    print(f"{file_to_delete} not found, no need to delete.")

# Load the datasets
sleep_df = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")

# --- Preprocessing sleep_df ---
# Fill missing 'Sleep Disorder' with 'None'
sleep_df['Sleep Disorder'] = sleep_df['Sleep Disorder'].fillna('None')

# Convert 'Blood Pressure' to numerical features
bp_split = sleep_df['Blood Pressure'].str.split('/', expand=True)
sleep_df['Systolic_BP'] = pd.to_numeric(bp_split[0])
sleep_df['Diastolic_BP'] = pd.to_numeric(bp_split[1])
sleep_df = sleep_df.drop(columns=['Blood Pressure', 'Person ID'])

# One-hot encode categorical features in sleep_df
sleep_df_encoded = pd.get_dummies(sleep_df, columns=['Gender', 'Occupation', 'BMI Category', 'Sleep Disorder'], drop_first=True)

# Define features (X) and target (y)
X = sleep_df_encoded.drop(columns=['Stress Level'])
y = sleep_df_encoded['Stress Level']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Hyperparameter Tuning ---
param_grid = {
    'n_estimators': [100, 200, 300],  # Number of trees in the forest
    'max_features': ['sqrt', 'log2'], # Corrected: removed 'auto' as it's deprecated/problematic
    'max_depth': [10, 20, 30, None], # Maximum number of levels in tree
    'min_samples_leaf': [1, 2, 4], # Minimum number of samples required at each leaf node
    'min_samples_split': [2, 5, 10] # Minimum number of samples required to split an internal node
}

# Initialize GridSearchCV
grid_search = GridSearchCV(estimator=RandomForestRegressor(random_state=42), param_grid=param_grid, 
                           cv=3, n_jobs=-1, verbose=2, scoring='r2')

# Fit GridSearchCV to the training data
grid_search.fit(X_train, y_train)

# Get the best model
best_model = grid_search.best_estimator_

print(f"\nBest Hyperparameters: {grid_search.best_params_}")

# Evaluate the best model
y_pred = best_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model Mean Absolute Error (tuned): {mae}")
print(f"Model R-squared (tuned): {r2}")

# Save the best trained model
joblib.dump(best_model, 'stress_prediction_model.pkl')
joblib.dump(X_train.columns.tolist(), 'model_columns.pkl')

print("Tuned model trained and saved as stress_prediction_model.pkl")
print("Model columns saved as model_columns.pkl")

# --- Print Feature Importances ---
if hasattr(best_model, 'feature_importances_'):
    importances = best_model.feature_importances_
    sorted_features = sorted(zip(importances, X_train.columns), reverse=True)

    print('\nFeature Importances (top 10):')
    for importance, feature in sorted_features[:10]:
        print(f'{feature}: {importance:.4f}')

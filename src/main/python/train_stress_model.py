import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_model():
    # Load the datasets
    try:
        sleep_df = pd.read_csv(os.path.join(os.getcwd(), 'data', 'raw', 'Sleep_health_and_lifestyle_dataset.csv'))
    except FileNotFoundError:
        logging.error("Sleep_health_and_lifestyle_dataset.csv not found. Please ensure the file is in the correct directory.")
        exit()
    except Exception as e:
        logging.error(f"Error loading Sleep_health_and_lifestyle_dataset.csv: {e}")
        exit()

    # --- Preprocessing sleep_df ---
    # Fill missing 'Sleep Disorder' with 'None'
    sleep_df['Sleep Disorder'] = sleep_df['Sleep Disorder'].fillna('None')

    # Convert 'Blood Pressure' to numerical features
    bp_split = sleep_df['Blood Pressure'].str.split('/', expand=True)
    sleep_df['Systolic_BP'] = pd.to_numeric(bp_split[0])
    sleep_df['Diastolic_BP'] = pd.to_numeric(bp_split[1])
    sleep_df = sleep_df.drop(columns=['Blood Pressure', 'Person ID'])

    # Create Age_Group for inference defaults
    bins = [10*i for i in range(10)] # Age groups like 0-9, 10-19, ..., 90-99
    labels = [f'{i}-{i+9}' for i in bins[:-1]] # Corrected f-string for labels
    sleep_df['Age_Group'] = pd.cut(sleep_df['Age'], bins=bins, labels=labels, right=False, include_lowest=True)

    # Calculate and save feature defaults based on Gender and Age_Group
    feature_defaults = {}
    for gender in sleep_df['Gender'].unique():
        feature_defaults[gender] = {}
        for age_group in sleep_df['Age_Group'].unique():
            subset = sleep_df[(sleep_df['Gender'] == gender) & (sleep_df['Age_Group'] == age_group)]
            if not subset.empty:
                feature_defaults[gender][age_group] = {}
                for col in sleep_df.columns.drop(['Gender', 'Age', 'Age_Group', 'Stress Level']):
                    if pd.api.types.is_numeric_dtype(subset[col]):
                        feature_defaults[gender][age_group][col] = subset[col].median()
                    else:
                        feature_defaults[gender][age_group][col] = subset[col].mode()[0]

    try:
        joblib.dump(feature_defaults, os.path.join(os.getcwd(), 'models', 'feature_defaults.pkl'))
        logging.info("Feature defaults saved.")
    except Exception as e:
        logging.error(f"Error saving feature_defaults.pkl: {e}")
        exit()

    # One-hot encode categorical features in sleep_df for model training
    sleep_df_encoded = pd.get_dummies(sleep_df, columns=['Gender', 'Occupation', 'BMI Category', 'Sleep Disorder'], drop_first=True)

    # Define features (X) and target (y)
    X = sleep_df_encoded.drop(columns=['Stress Level', 'Age_Group'])
    y = sleep_df_encoded['Stress Level']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- Hyperparameter Tuning ---
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_features': ['sqrt', 'log2'],
        'max_depth': [10, 20, 30, None],
        'min_samples_leaf': [1, 2, 4],
        'min_samples_split': [2, 5, 10]
    }

    grid_search = GridSearchCV(estimator=RandomForestRegressor(random_state=42), param_grid=param_grid,
                               cv=3, n_jobs=-1, verbose=0, scoring='r2') # Set verbose to 0 to reduce output

    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_

    logging.info(f"Best Hyperparameters: {grid_search.best_params_}")

    # Evaluate the best model
    y_pred = best_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    logging.info(f"Model Mean Absolute Error (tuned): {mae}")
    logging.info(f"Model R-squared (tuned): {r2}")

    # Save the best trained model
    try:
        joblib.dump(best_model, os.path.join(os.getcwd(), 'models', 'stress_prediction_model.pkl'))
        logging.info("Tuned model trained and saved.")
    except Exception as e:
        logging.error(f"Error saving stress_prediction_model.pkl: {e}")
        exit()

    try:
        joblib.dump(X_train.columns.tolist(), os.path.join(os.getcwd(), 'models', 'model_columns.pkl'))
        logging.info("Model columns saved.")
    except Exception as e:
        logging.error(f"Error saving model_columns.pkl: {e}")
        exit()

    # --- Print Feature Importances ---
    if hasattr(best_model, 'feature_importances_'):
        importances = best_model.feature_importances_
        sorted_features = sorted(zip(importances, X_train.columns), reverse=True)

        logging.info('Feature Importances (top 10):')
        for importance, feature in sorted_features[:10]:
            logging.info(f'{feature}: {importance:.4f}')

if __name__ == "__main__":
    train_model()
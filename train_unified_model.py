import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Load the datasets
try:
    sleep_health_df = pd.read_csv('Sleep_health_and_lifestyle_dataset.csv')
    mental_health_df = pd.read_csv('mental_health_analysis.csv')
except FileNotFoundError as e:
    print(f"Error loading data: {e}. Please ensure the CSV files are in the correct directory.")
    exit()

# --- Data Unification and Preprocessing ---

# 1. Standardize column names for merging
sleep_health_df.rename(columns={
    'Sleep Duration': 'Sleep_Hours',
    'Quality of Sleep': 'Sleep_Quality',
    'Physical Activity Level': 'Exercise_Hours',
    'Stress Level': 'Stress_Score',
    'Blood Pressure': 'Blood_Pressure'
}, inplace=True)

mental_health_df.rename(columns={
    'Sleep_Hours': 'Sleep_Hours',
    'Exercise_Hours': 'Exercise_Hours',
    'Survey_Stress_Score': 'Stress_Score'
}, inplace=True)

# 2. Select and align columns
common_features = ['Gender', 'Age', 'Sleep_Hours', 'Exercise_Hours', 'Stress_Score']
sleep_health_subset = sleep_health_df[common_features + ['Occupation', 'BMI Category', 'Heart Rate', 'Daily Steps', 'Sleep Disorder', 'Blood_Pressure']]
mental_health_subset = mental_health_df[common_features + ['Social_Media_Hours', 'Screen_Time_Hours']]

# Convert merge key columns to the same data type
sleep_health_subset['Age'] = sleep_health_subset['Age'].astype(int)
mental_health_subset['Age'] = mental_health_subset['Age'].astype(int)
sleep_health_subset['Sleep_Hours'] = sleep_health_subset['Sleep_Hours'].astype(float)
mental_health_subset['Sleep_Hours'] = mental_health_subset['Sleep_Hours'].astype(float)
sleep_health_subset['Exercise_Hours'] = sleep_health_subset['Exercise_Hours'].astype(float)
mental_health_subset['Exercise_Hours'] = mental_health_subset['Exercise_Hours'].astype(float)

# 3. Merge datasets
unified_df = pd.merge(sleep_health_subset, mental_health_subset, on=common_features, how='outer')

# 4. Feature Engineering: Split Blood Pressure
unified_df[['Systolic_BP', 'Diastolic_BP']] = unified_df['Blood_Pressure'].str.split('/', expand=True).astype(float)
unified_df.drop(columns=['Blood_Pressure'], inplace=True)

# --- Model Training ---

# Define features (X) and target (y)
X = unified_df.drop('Stress_Score', axis=1)
y = unified_df['Stress_Score']

# Identify categorical and numerical features
categorical_features = ['Gender', 'Occupation', 'BMI Category', 'Sleep Disorder']
numerical_features = X.select_dtypes(include=['int64', 'float64', 'int32']).columns.tolist()

# Create preprocessing pipelines for numerical and categorical features
numerical_transformer = SimpleImputer(strategy='median')
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Create a preprocessor object using ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ],
    remainder='passthrough' # Keep other columns (if any)
)

# Define the model
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)

# Create the full pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('regressor', model)])

# Split data and train the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

# --- Save Artifacts ---

# 1. Save the trained model pipeline
joblib.dump(pipeline, 'unified_stress_model.pkl')

# 2. Save the columns used for training
ohe_feature_names = pipeline.named_steps['preprocessor'].named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(categorical_features)
model_columns = numerical_features + list(ohe_feature_names)
joblib.dump(model_columns, 'unified_model_columns.pkl')

# 3. Save feature defaults for prediction
feature_defaults = {}
for col in numerical_features:
    feature_defaults[col] = X_train[col].median()
for col in categorical_features:
    feature_defaults[col] = X_train[col].mode()[0]

joblib.dump(feature_defaults, 'unified_feature_defaults.pkl')

print("Unified model, columns, and feature defaults have been trained and saved successfully!")
print(f"Model accuracy (R^2 score): {pipeline.score(X_test, y_test):.2f}")
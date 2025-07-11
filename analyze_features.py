import joblib

try:
    model = joblib.load('stress_prediction_model.pkl')
    columns = joblib.load('model_columns.pkl')

    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        sorted_features = sorted(zip(importances, columns), reverse=True)

        print('Feature Importances (top 10):')
        for importance, feature in sorted_features[:10]:
            print(f'{feature}: {importance:.4f}')
    else:
        print("The loaded model does not have 'feature_importances_' attribute.")

except FileNotFoundError:
    print("Error: Model files (stress_prediction_model.pkl or model_columns.pkl) not found. Please run train_stress_model.py first.")
except Exception as e:
    print(f"An error occurred: {e}")

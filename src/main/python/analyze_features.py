import joblib
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    model = joblib.load(os.path.join(os.getcwd(), 'models', 'stress_prediction_model.pkl'))
    columns = joblib.load(os.path.join(os.getcwd(), 'models', 'model_columns.pkl'))

    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        sorted_features = sorted(zip(importances, columns), reverse=True)

        logging.info('Feature Importances (top 10):')
        for importance, feature in sorted_features[:10]:
            logging.info(f'{feature}: {importance:.4f}')
    else:
        logging.warning("The loaded model does not have 'feature_importances_' attribute.")

except FileNotFoundError:
    logging.error("Error: Model files (stress_prediction_model.pkl or model_columns.pkl) not found. Please run train_stress_model.py first.")
except Exception as e:
    logging.error(f"An error occurred: {e}")
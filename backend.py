from flask import Flask, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load model and columns
def load_model():
    model_path = os.path.join('models', 'stress_prediction_model.pkl')
    columns_path = os.path.join('models', 'model_columns.pkl')
    defaults_path = os.path.join('models', 'feature_defaults.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(columns_path, 'rb') as f:
        columns = pickle.load(f)
    with open(defaults_path, 'rb') as f:
        defaults = pickle.load(f)
    return model, columns, defaults

model, model_columns, feature_defaults = load_model()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Prepare input in the correct order
    input_features = []
    for col in model_columns:
        input_features.append(data.get(col, feature_defaults.get(col, 0)))
    X = np.array([input_features])
    prediction = model.predict(X)[0]
    return jsonify({'stress_prediction': int(prediction)})

@app.route('/')
def home():
    return 'Vibe Check API is running.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

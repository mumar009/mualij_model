from flask import Flask, request, jsonify
import numpy as np
import onnxruntime as ort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for Flutter app

# Load the ONNX model
session = ort.InferenceSession("model.onnx")
input_name = session.get_inputs()[0].name  # e.g., "float_input"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Extract features in the order expected by the model
    features = np.array([
        data['gender'],
        data['height'],
        data['weight'],
        data['ap_hi'],
        data['ap_lo'],
        data['cholesterol'],
        data['gluc'],
        data['smoke'],
        data['alco'],
        data['active'],
        data['age_years'],
        data['bmi']
    ], dtype=np.float32).reshape(1, -1)  # Shape (1, 12) for batch inference

    # Run inference
    result = session.run(None, {input_name: features})
    prediction = result[0].item()  # Assuming binary classification
    probability = result[1][0].tolist()  # Adjust based on your model's output

    return jsonify({
        "prediction": int(prediction),
        "probability": probability
    })

if __name__ == '__main__':
    app.run(debug=False)
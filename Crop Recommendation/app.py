from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load the pre-trained model
model = joblib.load("random_forest_model.pkl")

# Crop label mapping dictionary
label_mapping = {
    0: 'apple', 1: 'banana', 2: 'blackgram', 3: 'chickpea',
    4: 'coconut', 5: 'coffee', 6: 'cotton', 7: 'grapes',
    8: 'jute', 9: 'kidneybeans', 10: 'lentil', 11: 'maize',
    12: 'mango', 13: 'mothbeans', 14: 'mungbean', 15: 'muskmelon',
    16: 'orange', 17: 'papaya', 18: 'pigeonpeas', 19: 'pomegranate',
    20: 'rice', 21: 'watermelon'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Retrieve form data and convert to float
        nitrogen = float(request.form.get('Nitrogen'))
        phosphorus = float(request.form.get('Phosphorus'))
        potassium = float(request.form.get('Potassium'))
        temperature = float(request.form.get('temperature'))
        humidity = float(request.form.get('humidity'))
        ph_value = float(request.form.get('ph'))
        rainfall = float(request.form.get('rainfall'))
    except Exception as e:
        return f"Invalid input: {str(e)}"

    # Arrange input data in the required order
    input_features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph_value, rainfall]])
    
    # Predict crop label and map to its corresponding crop name
    prediction = model.predict(input_features)[0]
    predicted_crop = label_mapping.get(prediction, "Unknown")
    
    return render_template('index.html', prediction_text=f'Predicted Crop: {predicted_crop}')

if __name__ == "__main__":
    app.run(debug=True)

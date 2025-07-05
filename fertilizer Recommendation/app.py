import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from flask import Flask, render_template, request, jsonify

# Load and preprocess the data
df = pd.read_csv("fertilizer/fertilizer complet dataset final.csv")  # Ensure this is the correct path
df.drop(df[df['Fertilizer'] == "10/10/2010"].index, inplace=True)

# Label Encoding
le_soil_color = LabelEncoder()
le_crop = LabelEncoder()
le_fertilizer = LabelEncoder()

df['Soil_color'] = le_soil_color.fit_transform(df['Soil_color'])
df['Crop'] = le_crop.fit_transform(df['Crop'])
df['Fertilizer'] = le_fertilizer.fit_transform(df['Fertilizer'])

# Prepare features and target
x = df.iloc[:, :-1]
y = df['Fertilizer']

# Split the data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Scale the features
st = StandardScaler()
x_train = st.fit_transform(x_train)
x_test = st.transform(x_test)

# Train the model
model = XGBClassifier(max_depth=50, n_estimators=500, reg_lambda=4, reg_alpha=0.1, learning_rate=0.4)
model.fit(x_train, y_train)

# Flask App
app = Flask(__name__)

@app.route('/')
def index():
    # Get unique values for dropdowns
    soil_colors = le_soil_color.classes_
    crops = le_crop.classes_
    
    return render_template('index.html', 
                           soil_colors=soil_colors, 
                           crops=crops)

@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from form
    temperature = float(request.form['temperature'])
    soil_color = request.form['soil_color']
    crop = request.form['crop']
    nitrogen = float(request.form['nitrogen'])
    phosphorus = float(request.form['phosphorus'])
    potassium = float(request.form['potassium'])
    
    # Transform categorical variables
    soil_color_encoded = le_soil_color.transform([soil_color])[0]
    crop_encoded = le_crop.transform([crop])[0]
    
    # Prepare input for model
    input_data = np.array([[
        temperature, 
        soil_color_encoded, 
        crop_encoded, 
        nitrogen, 
        phosphorus, 
        potassium
    ]])
    
    # Scale input
    input_data_scaled = st.transform(input_data)
    
    # Predict
    prediction = model.predict(input_data_scaled)
    predicted_fertilizer = le_fertilizer.inverse_transform(prediction)[0]
    
    return jsonify({'fertilizer': predicted_fertilizer})

if __name__ == '__main__':
    app.run(debug=True)
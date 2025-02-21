from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the model (you'll need to train and save your model first)
try:
    with open('stroke_model.pkl', 'rb') as file:
        model = pickle.load(file)
except:
    model = None  # Handle the case where model isn't available

@app.route('/')
def home():
    return render_template('stroke.html')

@app.route('/predict_stroke', methods=['POST'])
def predict_stroke():
    if request.method == 'POST':
        # Get values from the form
        gender = request.form['gender']
        age = float(request.form['age'])
        hypertension = int(request.form['hypertension'])
        heart_disease = int(request.form['heart_disease'])
        residence = request.form['residence']
        glucose = float(request.form['glucose'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        smoking_status = request.form['smoking_status']

        # Calculate BMI
        bmi = weight / ((height/100) ** 2)

        # Prepare the features (you'll need to match this with your model's expectations)
        features = np.array([[
            1 if gender == 'male' else 0,  # Gender encoding
            age,
            hypertension,
            heart_disease,
            1 if residence == 'urban' else 0,  # Residence encoding
            glucose,
            bmi,
            # Smoking status encoding - adjust according to your model's expectations
            1 if smoking_status == 'smokes' else 0  
        ]])

        # Make prediction if model is available
        if model:
            prediction = model.predict(features)[0]
        else:
            # For demonstration without a model
            prediction = 0 if age < 50 and bmi < 30 and glucose < 140 else 1

        return render_template('stroke.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
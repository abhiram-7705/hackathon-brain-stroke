from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle
import joblib

app = Flask(__name__)
try:
    model = joblib.load('stroke_model.joblib')
except:
    print("Model file not found. Please train and save the model first.")
    model = None

@app.route('/')
def home():
    return render_template('stroke.html')
@app.route('/predict_stroke', methods=['POST'])
def predict_stroke():
    if request.method == 'POST':
        try:
            gender = 1 if request.form['gender'] == 'female' else 0
            age = float(request.form['age'])
            hypertension = int(request.form['hypertension'])
            heart_disease = int(request.form['heart_disease'])
            avg_glucose_level = float(request.form['glucose'])
            bmi = float(request.form['bmi'])
            input_data = pd.DataFrame({
                'gender': [gender],
                'age': [age],
                'hypertension': [hypertension],
                'heart_disease': [heart_disease],
                'avg_glucose_level': [avg_glucose_level],
                'bmi': [bmi]
            })
            residence_type = request.form['residence']
            input_data['Residence_type_Rural'] = 1 if residence_type == 'rural' else 0
            input_data['Residence_type_Urban'] = 1 if residence_type == 'urban' else 0
            smoking_status = request.form['smoking_status']
            input_data['smoking_status_Unknown'] = 1 if smoking_status == 'unknown' else 0
            input_data['smoking_status_formerly smoked'] = 1 if smoking_status == 'formerly_smoked' else 0
            input_data['smoking_status_never smoked'] = 1 if smoking_status == 'never_smoked' else 0
            input_data['smoking_status_smokes'] = 1 if smoking_status == 'smokes' else 0
            expected_columns = [
                'gender', 'age', 'hypertension', 'heart_disease', 'avg_glucose_level', 
                'bmi', 'Residence_type_Rural', 'Residence_type_Urban',
                'smoking_status_Unknown', 'smoking_status_formerly smoked',
                'smoking_status_never smoked', 'smoking_status_smokes'
            ]
            input_data = input_data[expected_columns]
            if model:
                prediction = model.predict(input_data)[0]
            else:
                raise Exception("Model not loaded")

            return render_template('stroke.html', prediction=prediction)

        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            return render_template('stroke.html', error="An error occurred during prediction. Please try again.")

if __name__ == '__main__':
    app.run(debug=True)
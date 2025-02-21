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
            age = float(request.form['age'])
            if age < 3:
                return render_template('stroke.html', error="Age must be greater than 3 years")

            glucose = float(request.form['glucose'])
            if glucose <= 0:
                return render_template('stroke.html', error="Glucose level must be greater than 0")
            
            glucose = round(glucose, 2)

            height = float(request.form['height'])
            weight = float(request.form['weight'])
            
            if height <= 0 or weight <= 0:
                return render_template('stroke.html', error="Height and weight must be greater than 0")
            
            height_m = height / 100 
            bmi = weight / (height_m ** 2)
            bmi = round(bmi, 2)

            gender = 1 if request.form['gender'] == 'female' else 0
            hypertension = int(request.form['hypertension'])
            heart_disease = int(request.form['heart_disease'])
            residence_type = request.form['residence']
            smoking_status = request.form['smoking_status']

            input_data = pd.DataFrame({
                'gender': [gender],
                'age': [age],
                'hypertension': [hypertension],
                'heart_disease': [heart_disease],
                'avg_glucose_level': [glucose],
                'bmi': [bmi]
            })

            input_data['Residence_type_Rural'] = 1 if residence_type == 'rural' else 0
            input_data['Residence_type_Urban'] = 1 if residence_type == 'urban' else 0

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

            return render_template('stroke.html', 
                                prediction=prediction, 
                                bmi=bmi, 
                                input_data=request.form)  
        except ValueError as ve:
            print(f"Validation error: {str(ve)}")
            return render_template('stroke.html', 
                                error="Please check your input values. All numbers must be valid and positive.")
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            return render_template('stroke.html', 
                                error="An error occurred during prediction. Please try again.")

if __name__ == '__main__':
    app.run(debug=True)
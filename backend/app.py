from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os
import random
import google.generativeai as genai

app = Flask(__name__)

# --- ⚠️ IMPORTANT: PASTE YOUR KEY HERE ---
GEMINI_API_KEY = "AIzaSyAwUkVRg3EMlMA1g81e3UzgIP0dVw48tH0"
genai.configure(api_key=GEMINI_API_KEY)

# Global variables
model = None
encoders = {}
TARGET_COLUMN = 'risk_level' 
FEATURE_COLUMNS = ['age', 'weight', 'height', 'exercise', 'sleep', 
                   'sugar_intake', 'smoking', 'alcohol', 'married', 'profession', 'bmi']

# DATA GENERATION 
def generate_realistic_data(n_samples=500):
    print(f"⚡ Generating {n_samples} rows of realistic training data...")
    data = []
    for _ in range(n_samples):
        age = random.randint(20, 80)
        height = random.randint(150, 200)
        weight = random.randint(50, 120)
        bmi = weight / ((height / 100) ** 2)
        exercise = random.choice(['none', 'low', 'medium', 'high'])
        sugar = random.choice(['low', 'medium', 'high'])
        smoking = random.choice(['no', 'yes'])
        alcohol = random.choice(['no', 'yes'])
        sleep = random.randint(4, 10)
        
        score = 0
        if bmi > 30: score += 2
        if smoking == 'yes': score += 2
        if exercise == 'none': score += 2
        if age > 60: score += 1
        
        if score >= 4: risk = 'High'
        elif score >= 2: risk = 'Medium'
        else: risk = 'Low'
            
        data.append([age, weight, height, exercise, sleep, sugar, smoking, alcohol, 'no', 'other', bmi, risk])
        
    df = pd.DataFrame(data, columns=['age', 'weight', 'height', 'exercise', 'sleep', 
                                     'sugar_intake', 'smoking', 'alcohol', 'married', 'profession', 'bmi', 'risk_level'])
    return df

#  TRAINING 
def train_model():
    global model, encoders, TARGET_COLUMN
    print("⏳ Training Model...")
    
    df = generate_realistic_data(500)

    categorical_cols = ['exercise', 'sugar_intake', 'smoking', 'alcohol', 'married', 'profession']
    for col in categorical_cols:
        le = LabelEncoder()
        vals = df[col].astype(str).unique().tolist() + ['unknown']
        le.fit(vals)
        df[col] = le.transform(df[col].astype(str))
        encoders[col] = le

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    print("✅ Model Trained Successfully!")

def preprocess_input(data):
    w = float(data.get('weight', 70))
    h = float(data.get('height', 170))
    bmi = w / ((h/100)**2)
    
    input_dict = {
        'age': [data.get('age', 30)],
        'weight': [w],
        'height': [h],
        'exercise': [data.get('exercise', 'medium')],
        'sleep': [data.get('sleep', 7)],
        'sugar_intake': [data.get('sugarIntake', 'medium')],
        'smoking': [data.get('smoking', 'no')],
        'alcohol': [data.get('alcohol', 'no')],
        'married': [data.get('married', 'no')],
        'profession': [data.get('profession', 'other')],
        'bmi': [bmi]
    }
    df_input = pd.DataFrame(input_dict)
    for col, le in encoders.items():
        val = str(df_input[col].iloc[0])
        if val not in le.classes_: val = 'unknown'
        df_input[col] = le.transform([val])
    return df_input

# GEMINI HELPER GEMINI 2.0
def get_gemini_advice(user_data, risk_level):
    candidate_models = ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-flash-latest"]
    
    smoker_text = "smokes" if user_data.get('smoking') == 'yes' else "does not smoke"
    prompt = (
        f"You are a compassionate health advisor. "
        f"A user has this profile: Age {user_data.get('age')}, "
        f"BMI {round(user_data.get('bmi', 0), 1)}, "
        f"Activity: {user_data.get('exercise')}, "
        f"Habit: {smoker_text}. "
        f"Their Predicted Risk is {risk_level}. "
        f"Give 2 short, specific sentences of advice for them. No markdown."
    )

    for model_name in candidate_models:
        try:
            print(f"🤖 Asking {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            
            clean_text = response.text.replace('*', '').strip()
            return clean_text
            
        except Exception as e:
            print(f"⚠️ {model_name} failed: {e}")
            continue 
            
    return "Focus on a balanced diet and regular exercise. (AI Service Busy)"

# API ENDPOINT 
@app.route('/predict', methods=['POST'])
def predict():
    if model is None: return jsonify({"risk_level": "Medium"})

    try:
        data = request.json
        print(f"📥 Received: {data}")
        
        X_new = preprocess_input(data)
        prediction = model.predict(X_new)[0]
        print(f"🔮 Prediction: {prediction}")

        print("🤖 Calling Gemini for advice...")
        
        w = float(data.get('weight', 70))
        h = float(data.get('height', 170))
        data['bmi'] = w / ((h/100)**2)
        
        advice = get_gemini_advice(data, prediction)
        print(f"💬 Gemini said: {advice}")

        return jsonify({
            "risk_level": prediction, 
            "gemini_advice": advice
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"risk_level": "Medium", "gemini_advice": "Error"})

train_model()

if __name__ == '__main__':
    app.run(port=5000, debug=True)

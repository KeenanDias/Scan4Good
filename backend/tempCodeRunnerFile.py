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



# --- 1. DATA GENERATION ---
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

# --- 2. TRAINING ---
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
# # --- 3. GEMINI HELPER (EMERGENCY SIMULATION MODE) ---
# def get_gemini_advice(user_data, risk_level):
#     # CRITICAL: Hackathon Deadline Backup Plan
    
#     age = user_data.get('age')
#     smoker = user_data.get('smoking')
#     exercise = user_data.get('exercise')
    
#     if risk_level == "High":
#         if smoker == "yes":
#             return f"As a {age}-year-old smoker, your immediate priority is quitting to lower heart risks. Combine this with light daily walks to improve your lung capacity safely."
#         elif exercise == "none":
#              return f"At {age}, a sedentary lifestyle is your biggest risk factor. Start with just 10 minutes of walking a day to significantly lower your risk score."
#         else:
#             return f"Your BMI and age ({age}) indicate elevated risk. Please consult a specialist, as diet changes alone may not be enough."
            
#     elif risk_level == "Medium":
#         if exercise == "none" or exercise == "low":
#             return f"You are close to a healthy range, but your activity level is too low. Increasing exercise to 30 mins/day would likely drop you to Low Risk."
#         else:
#             return f"Maintain your current activity, but monitor your diet. Small adjustments to sugar intake could help lower your risk profile further."
            
#     else: # Low
#         return f"Great job! Your profile for a {age}-year-old is excellent. Keep maintaining your {exercise} exercise routine to stay in this green zone."
    
#--- 3. GEMINI HELPER (ROBUST VERSION) ---
def get_gemini_advice(user_data, risk_level):
    # Try multiple model names in case one is deprecated or unavailable
    candidate_models = ["gemini-1.5-flash", "gemini-pro", "gemini-1.0-pro"]
    
    prompt = (
        f"You are a health advisor. User Profile: "
        f"Age {user_data.get('age')}, BMI {round(user_data.get('bmi', 0), 1)}, "
        f"Smokes: {user_data.get('smoking')}. "
        f"Predicted Risk: {risk_level}. "
        f"Give 2 short, specific sentences of advice."
    )

    for model_name in candidate_models:
        try:
            print(f"🤖 Attempting to use model: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"⚠️ Failed with {model_name}: {e}")
            continue # Try the next model in the list
            
    return "Focus on balanced diet and exercise. (AI Connection Failed)"

# --- 4. API ENDPOINT ---
@app.route('/predict', methods=['POST'])
def predict():
    if model is None: return jsonify({"risk_level": "Medium"})

    try:
        data = request.json
        print(f"📥 Received: {data}")
        
        # A. Predict Risk
        X_new = preprocess_input(data)
        prediction = model.predict(X_new)[0]
        print(f"🔮 Prediction: {prediction}")

        # B. Get Gemini Advice
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
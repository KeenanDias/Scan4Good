from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# ---------------------------------------------------------
# HACKATHON SHORTCUT: Dummy Model Logic
# In real life, you load a model: model = pickle.load(open('model.pkl', 'rb'))
# Here, we simulate the logic so you can build the UI/Backend first.
# ---------------------------------------------------------
def simple_heuristic_model(data):
    # Example logic: If BMI > 30 or smoker, High Risk
    bmi = data.get('weight') / ((data.get('height')/100) ** 2)
    if data.get('smoker') == 'yes' or bmi > 30:
        return "High"
    elif bmi > 25:
        return "Medium"
    else:
        return "Low"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    risk_level = simple_heuristic_model(data)
    return jsonify({"risk_level": risk_level})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
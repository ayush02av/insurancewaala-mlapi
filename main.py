from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

model_charges = pickle.load(open('model_charges.pkl', 'rb'))
model_region = pickle.load(open('model_region.pkl', 'rb'))

@app.route('/', methods = ['POST'])
def predict():
    data = request.get_json()
    data_keys = data.keys()
    errors = []
    
    validators = [
        'age',
        'female',
        'bmi',
        'children',
        'smoker'
    ]
    for validator in validators:
        if validator not in data_keys or data[validator] == None:
            errors.append(f"{validator} is required")
    
    if len(errors) > 0:
        return jsonify({
            'success': 0,
            'errors': errors
        })
    
    if 'region' not in data_keys:
        data['region'] = model_region.predict([
                [
                    data['age'],
                    data['female'],
                    data['bmi'],
                    data['children'],
                    data['smoker']
                ]
            ]).tolist()[0]
    
    prediction = round(model_charges.predict([
            [
                data['age'],
                data['female'],
                data['bmi'],
                data['children'],
                data['smoker'],
                data['region'],
            ]
        ]).tolist()[0], 2)

    if prediction < 100:
        return jsonify({
            'success': 0,
            'errors': [
                'Our Model does not serve to your request',
                'Try increasing your age or bmi'
            ]
        })
    
    return jsonify({
        'success': 1,
        'input': data,
        'output' : prediction
    })

if __name__ == "__main__":
    app.run(debug = True, port = 80)
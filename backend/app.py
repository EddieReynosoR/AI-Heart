from flask import Flask, request, jsonify
import pandas as pd
import tensorflow as tf
import joblib
from flask_cors import CORS
from utils.db import get_db
from bson import ObjectId
import numpy as np

app = Flask(__name__)
CORS(app)

# Cargar modelo y escalador una vez
model = tf.keras.models.load_model("heart_model.keras")
scaler = joblib.load("scaler.pkl")

def get_pacientes_collection():
    return get_db()["pacientes"]

def get_predictions_collection():
    return get_db()["predictions"]

def serialize_doc(doc):
    if isinstance(doc, dict):
        return {k: serialize_doc(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [serialize_doc(i) for i in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    else:
        return doc

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')

        features = pd.DataFrame([[age, data['sex'], data['cp'], data['trestbps'], data['chol'],
                                  data['fbs'], data['restecg'], data['thalach'], data['exang'],
                                  data['oldpeak'], data['slope'], data['ca'], data['thal']]],
                                columns=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                                         'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'])

        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0][0]
        prediction = int(prediction >= 0.5)

        prediction_entry = {
            "age": age,
            "sex": data['sex'],
            "cp": data['cp'],
            "trestbps": data['trestbps'],
            "chol": data['chol'],
            "fbs": data['fbs'],
            "restecg": data['restecg'],
            "thalach": data['thalach'],
            "exang": data['exang'],
            "oldpeak": data['oldpeak'],
            "slope": data['slope'],
            "ca": data['ca'],
            "thal": data['thal'],
            "prediction": prediction
        }

        get_predictions_collection().insert_one(prediction_entry)
        pacientes_col = get_pacientes_collection()
        paciente = pacientes_col.find_one({"name": name})

        if paciente:
            pacientes_col.update_one({"name": name}, {"$push": {"history": prediction_entry}})
        else:
            pacientes_col.insert_one({
                "name": name,
                "age": age,
                "history": [prediction_entry]
            })

        message = "Posible arritmia detectada. Consultar con un médico." if prediction == 1 else "No se detectaron problemas graves."
        return jsonify({'message': message})

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 400

@app.route("/pacientes", methods=["GET"])
def get_pacientes():
    pacientes = list(get_pacientes_collection().find())
    return jsonify([serialize_doc(p) for p in pacientes]), 200

@app.route("/predictions", methods=["GET"])
def get_predictions():
    predictions = list(get_predictions_collection().find())
    return jsonify([serialize_doc(p) for p in predictions]), 200

if __name__ == "__main__":
    app.run(debug=True)

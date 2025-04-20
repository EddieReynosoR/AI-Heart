from flask import Flask, request, jsonify
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from flask_cors import CORS
from utils.db import get_db
from bson import ObjectId

app = Flask(__name__)
CORS(app)

# Entrenamiento del modelo
df = pd.read_csv('heart.csv')
x, y = df.drop('target', axis=1), df['target']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.8, random_state=0)
model = GradientBoostingClassifier()
model.fit(x_train, y_train)

# Obtener colecciones de MongoDB
def get_pacientes_collection():
    return get_db()["pacientes"]

def get_predictions_collection():
    return get_db()["predictions"]

# Función auxiliar para convertir ObjectId y otros tipos no serializables
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

        # Datos personales
        name = data.get('name')
        age = data.get('age')

        # Variables del modelo
        sex = data['sex']
        cp = data['cp']
        trestbps = data['trestbps']
        chol = data['chol']
        fbs = data['fbs']
        restecg = data['restecg']
        thalach = data['thalach']
        exang = data['exang']
        oldpeak = data['oldpeak']
        slope = data['slope']
        ca = data['ca']
        thal = data['thal']

        features = pd.DataFrame([[age, sex, cp, trestbps, chol, fbs, restecg,
                                  thalach, exang, oldpeak, slope, ca, thal]],
            columns=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                     'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'])

        prediction = model.predict(features)[0]

        prediction_entry = {
            "age": age,
            "sex": sex,
            "cp": cp,
            "trestbps": trestbps,
            "chol": chol,
            "fbs": fbs,
            "restecg": restecg,
            "thalach": thalach,
            "exang": exang,
            "oldpeak": oldpeak,
            "slope": slope,
            "ca": ca,
            "thal": thal,
            "prediction": int(prediction)
        }

        predictions_col = get_predictions_collection()
        predictions_col.insert_one(prediction_entry)

        pacientes_col = get_pacientes_collection()
        paciente = pacientes_col.find_one({"name": name})
        if paciente:
            pacientes_col.update_one({"name": name}, {"$push": {"history": prediction_entry}})
        else:
            new_paciente = {
                "name": name,
                "age": age,
                "history": [prediction_entry]
            }
            pacientes_col.insert_one(new_paciente)

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

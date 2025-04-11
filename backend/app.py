from flask import Flask, request, jsonify
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

from flask_cors import CORS  # Importa CORS

app = Flask(__name__)
CORS(app)

# Cargar modelo
df = pd.read_csv('heart.csv')
x, y = df.drop('target', axis=1), df['target']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.8, random_state=0)

model = GradientBoostingClassifier()
model.fit(x_train, y_train)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    features = [data[key] for key in ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]]
    
    prediction = model.predict([features])[0]
    
    result = "Estás saludable" if prediction == 0 else "No estás saludable"
    return jsonify({"message": result}),200

if __name__ == "__main__":
    app.run(debug=True)

import pandas as pd
import tensorflow as tf
import joblib
from sklearn.preprocessing import StandardScaler

# Cargar modelo y escalador existentes
model = tf.keras.models.load_model("heart_model.keras")
scaler = joblib.load("scaler.pkl")

# Nuevos datos
df = pd.read_csv("heart.csv")  # o apunta a nuevos datos
X = df.drop("target", axis=1)
y = df["target"]

X_scaled = scaler.transform(X)

# Reentrenar (ajuste fino)
model.fit(X_scaled, y, epochs=5)

# Guardar modelo actualizado
model.save("heart_model.keras")

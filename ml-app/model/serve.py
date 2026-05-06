from flask import Flask, request, jsonify
import joblib, numpy as np

app = Flask(__name__)
model = joblib.load("model.pkl")
SPECIES = ["setosa", "versicolor", "virginica"]

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json["features"]
    pred = model.predict(np.array(data).reshape(1, -1))[0]
    return jsonify({"species": SPECIES[pred]})

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

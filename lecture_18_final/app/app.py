import joblib
from flask import Flask, jsonify, request, render_template
from app.util import extract_face, load_cv2_from_base64, load_cv2_from_file


app = Flask(__name__)

model_knn = joblib.load("models/model_knn.pkl")
model_svc = joblib.load("models/model_svc.pkl")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict/knn", methods=["GET", "POST"])
def predict_knn():
    if request.method == "GET":
        return render_template("knn.html")

    file = request.files.get("picture")
    if file:
        img = load_cv2_from_file(file)
    else:
        img = load_cv2_from_base64(request.get_json()["image"])

    face, marked_img  = extract_face(img)
    if face is None:
        return jsonify({"message": "No face detected"})

    pred = model_knn.predict(face)
    pred_label = "happy" if pred[0] == 0 else "sad"
    return jsonify({"message": pred_label, "marking": marked_img})


@app.route("/predict/svc", methods=["GET", "POST"])
def predict_svc():
    if request.method == "GET":
        return render_template("svc.html")
    
    file = request.files.get("picture")
    if file:
        img = load_cv2_from_file(file)
    else:
        img = load_cv2_from_base64(request.get_json()["image"])

    face, marked_img = extract_face(img)
    if face is None:
        return jsonify({"message": "No face detected"})

    pred = model_svc.predict(face)
    pred_label = "happy" if pred[0] == 0 else "sad"
    return jsonify({"message": pred_label, "marking": marked_img})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug = False)

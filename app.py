from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import os

app = Flask(__name__)
model = load_model("cancer_detector.h5")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", prediction="No file uploaded.")

        file = request.files["file"]
        if file.filename == "":
            return render_template("index.html", prediction="No file selected.")

        if file:
            if not os.path.exists("static"):
                os.makedirs("static")

            filepath = os.path.join("static", file.filename)
            file.save(filepath)

            img = load_img(filepath, target_size=(50, 50))
            img = img_to_array(img) / 255.0
            img = np.expand_dims(img, axis=0)

            result = model.predict(img)
            confidence = float(result[0][0])
            prediction = "Cancerous" if confidence > 0.5 else "Non-Cancerous"
            if prediction == "Cancerous":
                explanation = "This image shows characteristics commonly associated with cancerous breast tissue. Please consult a medical professional for further diagnosis."
            else:
                explanation = "This image does not show features typically associated with invasive ductal carcinoma. However, this is not a substitute for medical advice."



            confidence_pct = round(confidence * 100, 2) if prediction == "Cancerous" else round((1 - confidence) * 100, 2)
            return render_template("index.html", prediction=prediction, confidence=confidence_pct, image_url=filepath, explanation=explanation)
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)


from flask import Flask
from flask import render_template , request 
from PIL import Image
import numpy as np
from pathlib import Path
import tensorflow as tf
import json
from flask import jsonify

app = Flask(__name__)

# Récupérer le dossier racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Construire le chemin vers le modèle
MODEL_PATH = BASE_DIR / "models" / "resnet50_best.keras"
CLASS_NAMES_PATH = BASE_DIR / "models" / "class_names.json"
model = tf.keras.models.load_model(MODEL_PATH)
print("Modèle chargé avec succès depuis :")

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    class_names = json.load(f)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    #Vérifie si le fichier "image" existe dans request.files.
    if 'image' not in request.files:
        return "No image received", 400
    image= request.files['image']

    if image.filename == '':
        return "No selected file", 400
    

    img =Image.open(image.stream)
    img = img.convert("RGB")
    img = img.resize((224,224))
    print(img.size)
    print(img.mode)

    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)

    print(img_array.shape)

    predictions = model.predict(img_array, verbose=0)
    print(predictions)

    predicted_index = np.argmax(predictions[0])
    confidence = np.max(predictions[0])
    predicted_class = class_names[predicted_index].split(".")[1] # Récupère le nom de la classe après le point
    print("Indice prédit :", predicted_index)
    print("Score maximal :", confidence)
    print("Objet reconnu :", predicted_class)
 
    confidence_score = float(confidence)

    

    return jsonify({
            "predicted_class": predicted_class,
            "confidence_score": confidence_score,
        })


   


if __name__ == '__main__':
    app.run(debug=True)


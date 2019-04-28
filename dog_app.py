import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
load_dotenv()
import os
from PIL import Image
import io
from test import prediction_on_image
from util.util import format_prediction

#IMAGE params
PATH_TO_IMAGE = os.getenv("PATH_TO_IMAGE")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DEBUG = os.getenv("DEBUG")


app = Flask(__name__)
CORS(app)
@app.route('/')
def hello_world():
    return 'Hello, World!'



@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        if request.files.get("image"):
            image = request.files["image"].read()
            image = Image.open(io.BytesIO(image))
            print("first type")
            print(type(image))
            pred = prediction_on_image(image)
            top1 = format_prediction(str(pred[0][1]))
            acc = str(pred[0][2])
            return jsonify(prediction=top1, accuracy=acc), 200

        return jsonify(tussar="liten")
    elif request.method == 'GET':
        return jsonify(response="NEED TO DO POST"), 200

@app.route('/test', methods=['GET','POST'])
def test():
    if request.method == 'POST':
        img = Image.open(request.files['file'])
        return 'Success'
    elif request.method == 'GET':
        return jsonify(response="NEED TO DO POST ON TEST"), 400

if __name__ == '__main__':
    app.run(host=HOST,
            debug=DEBUG,
            port=PORT)

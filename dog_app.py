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

##oskar
import os
from keras import backend as K
import logging
import json
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from keras.applications import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing import image
from keras.models import load_model
from glob import glob
import pickle
import tensorflow as tf
##oskar

##### OSKAR
class ParseJsonResult:
    def toJSON(self):
        return json.dumps(self,default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
class NeuralNetwork:
    def __init__(self,modelfile,classfile):
        self.session = tf.Session()
        self.graph = tf.get_default_graph()
        # the folder in which the model and weights are stored
        self.model_folder = 'models'
        self.modelfile = modelfile
        self.classfile =classfile
        # for some reason in a flask app the graph/session needs to be used in the init else it hangs on other threads
        self.load_mod()
        self.load_classes()
        
        
        
        with self.graph.as_default():
            with self.session.as_default():
                logging.info("neural network initialised")
                
        
    def load_mod(self):
        """
        :param file_name: [model_file_name]
        :return:
        """
        with self.graph.as_default():
            with self.session.as_default():
                try:
                    # load the model
                    self.model = load_model(os.path.join(self.model_folder, self.modelfile))
                        
                    logging.info("Neural Network loaded: ")
                    logging.info('\t' + "Neural Network model: " + self.modelfile)
                    return True
                except Exception as e:
                    logging.exception(e)
                    return False
    def load_classes(self):
        self.name_id_map = pickle.load(open(os.path.join(self.model_folder, self.classfile), "rb" ))
        
    def predict(self, input_img):
        with self.graph.as_default():
            with self.session.as_default():
                
                self.activations = np.round(np.squeeze(self.model.predict(np.expand_dims(preprocess_input(np.array(input_img)),axis=0))),2)
                print(self.model)
                df = pd.DataFrame(np.vstack((np.array(list(self.name_id_map.keys())).astype(int),np.array(list(self.name_id_map.values())))).T,columns=['idx','species'])
                df['activations'] = self.activations
                df = df.sort_values(by=['activations'],ascending=False)
                result = df.head(3)

                l = [ParseJsonResult()]*3

                for i,j in enumerate(result.iterrows()):
                    n,m = j
                    l[i] = ParseJsonResult()
                    l[i].idx = m.idx
                    l[i].species = m.species
                    l[i].activations = m.activations

                self.json = [l[i].toJSON() for i in range(len(l))]
                self.winner = json.loads(self.json[0])['species']

        return self.json

#### Oskar





app = Flask(__name__)
CORS(app)
#IMAGE params
PATH_TO_IMAGE = os.getenv("PATH_TO_IMAGE")
#HOST = os.getenv("HOST")
#PORT = os.getenv("PORT")
#DEBUG = os.getenv("DEBUG")


##oskar
model = NeuralNetwork(modelfile = 'model4.h5',classfile = 'dict.p')
logger = logging.getLogger('root')
##oskar



@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/predict_dogs', methods=['GET','POST'])
def predict_dogs():
    if request.files.get("image"):
        image = request.files["image"].read()
        image = Image.open(io.BytesIO(image))

        model.predict(image)

        result = model.json

        return jsonify(prediction=json.loads(result[0])['species'], accuracy=json.loads(result[0])['activations']), 200


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
    app.run()


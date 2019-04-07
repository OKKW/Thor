from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
from dotenv import load_dotenv
load_dotenv()
import os

#IMAGE params
PATH_TO_IMAGE = os.getenv("PATH_TO_IMAGE")
IMAGE_NAME = os.getenv("IMAGE_NAME")

# Model Params
NUM_TOP_PREDICTIONS  = int(os.getenv("NUM_PREDICTS"))
TARGET_SIZE = int(os.getenv("TARGET_SIZE"))
        
model = ResNet50(weights='imagenet')
model._make_predict_function()
#img_path = PATH_IMAGE_TO_PREDICT
def get_full_image_path(image_name):
    return PATH_TO_IMAGE +"/"+image_name

def get_image(input_image, by_name = False):
    if by_name:
        img_path = get_full_image_path(input_image)
        input_image_resized = image.load_img(img_path, target_size=(TARGET_SIZE, TARGET_SIZE))
        return input_image_resized
    if input_image.mode != "RGB":
        input_image = input_image.convert("RGB")
    return input_image.resize((TARGET_SIZE,TARGET_SIZE))

def process_image(input_image):
    proccessed_image = image.img_to_array(input_image)
    proccessed_image = np.expand_dims(proccessed_image, axis=0)
    proccessed_image = preprocess_input(proccessed_image)
    print(type(proccessed_image))
    print(proccessed_image)
    print(proccessed_image.shape)
    print("---------------------------------------NAME------------------------------------")
    return proccessed_image

def feed_network_with_image(input_image, by_name = False):
    input_image = get_image(input_image, by_name)
    processed_image = process_image(input_image)
    preds = model.predict(processed_image)
    return preds

def decode_predicitons(predictions):
    # decode the results into a list of tuples (class, description, probability)
    # (one such list for each sample in the batch)
    return decode_predictions(predictions, top = NUM_TOP_PREDICTIONS )[0]

def format_output_predictions(predicted):    
    for pred in predicted:
        print('You have a: ' + str(pred[1]).replace("_"," ") +' with :'+ str(pred[2])+' certainty')

def prediction_on_image(input_image, by_name = False):
    predictions_raw = feed_network_with_image(input_image, by_name)
    return decode_predicitons(predictions_raw)

if __name__ == '__main__':
    input_image = IMAGE_NAME
    format_output_predictions(prediction_on_image(input_image, True))


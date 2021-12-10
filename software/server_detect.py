import io
import picamera
import numpy as np
import time
import base64                  
import logging
import json
from tensorflow import keras
from tensorflow.keras import models
from PIL import Image, ImageDraw
from flask import Flask, request, jsonify, abort
from yolofn import yolo_out,draw

app = Flask(__name__)          
app.logger.setLevel(logging.DEBUG)

#load model
yolo = models.load_model('yolotest.h5')

#load classes labels
with open('coco_classes.txt') as f:
    class_names = f.readlines()
all_classes = [c.strip() for c in class_names]

def load_image(request):
    #Load input image from images folder add resize to match yolo model
    image_src = Image.open(request.files['media'])
    #image_src = image_src.rotate(180)
    size = (416, 416)
    #orig_size = image_src.size
    image_src = image_src.resize(size)
    #image_thumb = image_src.resize(size, Image.BICUBIC)
    image = np.array(image_src, dtype='float32')
    image /= 255.
    image = np.expand_dims(image, axis=0)
    return image, image_src

@app.route("/test", methods=['POST'])
def test_method():
    global yolo, all_classes
    request_start_time = time.time()
    response = {'obstacles': False,
                'model_time': 0.0,
                'request_time': 0.0,
                'accuracy': 0.0}
   
    #Load input image from images folder add resize to match yolo model
    image, orig_image = load_image(request)

    # Raw Output
    model_start_time = time.time() #prediction start time
    output = yolo.predict(image)
    model_end_time = time.time() #prediction end time
    response['model_time'] = model_end_time - model_start_time
    
    # Processed Output
    boxes, classes, scores = yolo_out(output, orig_image.size)
    if boxes is not None:
        #draw(image_thumb, boxes, scores, classes, all_classes)
        if 41 in classes and scores[classes.tolist().index(41)] > 0.01:
            response['obstacles'] = True
            response['accuracy'] = str(scores[classes.tolist().index(41)])
    
    # Display processed image output
    #orig_image.show()
    request_end_time = time.time()
    response['request_time'] = request_end_time - request_start_time
    return response

def run_server_api():
    app.run(host='0.0.0.0', port=8080)
  
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_func()
    return "Shutting down..."

if __name__ == "__main__":
    try:
        run_server_api()
    except KeyboardInterrupt:
        shutdown()
        

#Tiny Yolo 3 model test program
#BlackMagicai.com
import io
import picamera
import numpy as np
import time
import base64                  
import logging
import json
from tensorflow import keras
#from keras.models import load_model
from tensorflow.keras import models
from PIL import Image, ImageDraw
from flask import Flask, request, jsonify, abort
from yolofn import yolo_out,draw

app = Flask(__name__)          
app.logger.setLevel(logging.DEBUG)

@app.route("/test", methods=['POST'])
def test_method():
    t0 = time.time()
    #if not request.files:
    #    print('There is no files attribute in json')
    #    abort(400)
    yolo = models.load_model('yolotest.h5')
   
    #########################################
    #Load input image from images folder add resize to match yolo model imput 

    #my_stream.seek(0)
    image_src = Image.open(request.files['media'])
    image_src = image_src.rotate(180)
    size = (416, 416)
    orig_size = image_src.size
    image_thumb = image_src.resize(size, Image.BICUBIC)
    image = np.array(image_thumb, dtype='float32')
    image /= 255.
    image = np.expand_dims(image, axis=0)

    ##############################

    # Raw Output
    start = time.time() #prediction start time
    output = yolo.predict(image)
    end = time.time() #prediction end time

    print('Processing time: {0:.2f}s'.format(end-start))

    ############################

    with open('coco_classes.txt') as f:
        class_names = f.readlines()
    all_classes = [c.strip() for c in class_names]

    # Processed Output
    thumb_size = image_thumb.size
    boxes, classes, scores = yolo_out(output, thumb_size)
    result_dict = {'obstacles': False}
    if boxes is not None:
        draw(image_thumb, boxes, scores, classes, all_classes)
        print('scores:', scores)
        print('classes:', classes)
        if 41 in classes and scores[classes.tolist().index(41)] > 0.5:
            result_dict = {'obstacles': True}
    
    # Display processed image output
    image_thumb.show()

    #result_dict = {'output': 'output_key'}
    t1 = time.time()
    print('time:', t1 - t0)
    return result_dict
  
  
def run_server_api():
    app.run(host='0.0.0.0', port=8080)
  
  
if __name__ == "__main__":     
    run_server_api()


import io
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

app = Flask(__name__)          
app.logger.setLevel(logging.DEBUG)

@app.route("/test", methods=['POST'])
def test_method():
    t0 = time.time()
    yolo = models.load_model('yolotest.h5')
    image_src = Image.open(request.files['media'])
    file_name = "origin_dataset/" + str(time.time()) + ".jpg"
    im2 = image_src.save(file_name)
    result_dict = {'obstacles': False}
    return result_dict
  
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


import RPi.GPIO as GPIO
import time
import picamera
import io
from PIL import Image
import base64
import json
import requests


class Motor:
  def __init__(self, enable, in1, in2):
    self.enable = enable
    GPIO.setup(enable, GPIO.OUT)
    GPIO.output(enable, GPIO.LOW)
    self.pwm = GPIO.PWM(self.enable,1000)
    self.pwm.start(0)


    self.in1 = in1
    GPIO.setup(in1, GPIO.OUT)
    GPIO.output(in1, GPIO.LOW)
    self.in2 = in2
    GPIO.setup(in2, GPIO.OUT)
    GPIO.output(in2, GPIO.LOW)



right_motor = None
left_motor = None
camera = None
server_addr = 'http://192.168.1.19:8080/test'


def setup():
  GPIO.setmode(GPIO.BCM)
  global right_motor
  global left_motor
  right_motor = Motor(13, 19, 26);
  left_motor = Motor(12, 2, 3);
  initialize_camera()



def ask_server(my_stream):
  t0 = time.time()
  my_stream.seek(0)
  files = {"media": ('file.jpg', my_stream, 'image/jpg')}
  #print(requests.Request('POST', 'http://example.com', files=files).prepare().body)
  response = requests.post(server_addr, files=files)#, headers=headers)
  t1 = time.time()
  my_stream.close()
  try:
      data = response.json()
      print(data)
      print('time:', t1 - t0)
      return data['obstacles']
  except requests.exceptions.RequestException:
      print(response.text)

  return False



def initialize_camera():
  global camera
  camera = picamera.PiCamera()
  camera.resolution = (416,416)
  camera.start_preview()
  time.sleep(3)

def capture_pic():
  global camera
  my_stream = io.BytesIO()
  camera.capture(my_stream, 'jpeg')
  my_stream.seek(0)
  return my_stream


def turn_right():
  set_motors(150, -150, right_motor, left_motor)
  time.sleep(1.45/2)
  set_motors(0, 0, right_motor, left_motor)

def turn_left():
  set_motors(-150, 150, right_motor, left_motor)
  time.sleep(1.45/2)
  set_motors(0, 0, right_motor, left_motor)


def loop():
  while True:
    set_motors(70, 64, right_motor, left_motor)
    time.sleep(1)
    set_motors(0,0, right_motor, left_motor)
    if ask_server(capture_pic()):
      # obstacle detected
      turn_right()
      set_motors(70, 70, right_motor, left_motor)
      time.sleep(2)
      turn_left()


    # turn_right()
    # time.sleep(4)
    # turn_left()
    #time.sleep(4)



# void task(){
#   set_motors(-150, 150, left_motor, right_motor);
#   delay(1000);
#   set_motors(150, -150, left_motor, right_motor);
#   delay(1000);
#   set_motors(0, 0, left_motor, right_motor);
#   delay(5000);
# }


def destroy():
    set_motor(0, right_motor);
    set_motor(0, left_motor);
    right_motor.pwm.stop()
    left_motor.pwm.stop()
    GPIO.cleanup()
    # any clean up code for camera? doesn't seem like they have any in the example codes
    camera.close()


def set_motors( vel_a,  vel_b,  a,  b):
  set_motor(-vel_a, a);
  set_motor(-vel_b, b);

def set_motor(velocity, m):
  if (velocity == 0):
    GPIO.output(m.in1, GPIO.LOW)
    GPIO.output(m.in2, GPIO.LOW)

    m.pwm.ChangeDutyCycle(0)

  elif(velocity > 0):
    GPIO.output(m.in1, GPIO.LOW)
    GPIO.output(m.in2, GPIO.HIGH)
    m.pwm.ChangeDutyCycle(100*min(velocity, 255)/255)
  else:
    GPIO.output(m.in1, GPIO.HIGH)
    GPIO.output(m.in2, GPIO.LOW)
    m.pwm.ChangeDutyCycle( 100* min(-velocity, 255)/255);
  


if  __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

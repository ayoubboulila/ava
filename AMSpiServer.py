'''
Created on 30 janv. 2018

@author: AYB
'''
from flask import Flask, flash, redirect, render_template, request, session, abort, Response
import jinja2
import time
import config
import threading
import requests
#import redis
#from utils.RedisClient import RedisClient
from utils import Logger
import logging
from logging.handlers import RotatingFileHandler
import json as js
# utils.Broker import BROKER
from utils.RabbitCtl import BROKER
from lib.ai.detector.ObjectDetector import Detector
#from lib.ai.detector.detect_picamera import main as pc
#from DetectionStreamController import DestectionStream
#from flask_mqtt import Mqtt
#import paho.mqtt.publish as publish 

app = Flask(__name__)
log = Logger.RCLog('AMSpiServer')


my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('templates'),
])
app.jinja_loader = my_loader


@app.route('/')
@app.route('/index')
def index():
    
    test="ok"
    return render_template(
        'index.html',**locals())

@app.route("/stream")
def stream():
    mimetype = "multipart/x-mixed-replace; boundary=frame"
    
    #return "a"
    return Response(dt.start_fast_detection(use_rabbit=True), mimetype=mimetype)


@app.route('/index/forward', methods=['POST'])
def forward():
    log.debug("forward")
    try:
        speed = 100
        data = js.loads(request.data.decode('utf-8'))
        if data['speed']:
            speed = int(data['speed'])
            print(speed)
        json = '{"action": "go",  "speed": "'+ str(speed) +'", "time_limit": "0"}'
        r.publish('DCMC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in forward")
        log.error(ex, exc_info=True)
        return "NOTOK"
    
@app.route('/index/backword', methods=['POST'])
def backword():
    print("backword")
    try:
        speed = 100
        data = js.loads(request.data.decode('utf-8'))
        if data['speed']:
            speed = int(data['speed'])
            print(speed)
        json = '{"action": "back",  "speed": "' + str(speed) + '", "time_limit": "0"}'
        r.publish('DCMC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in backward")
        log.error(ex, exc_info=True)
        return "NOTOK"
    
    


@app.route('/index/turn_left', methods=['POST'])
def turn_left():
    print("turn_left")
    try:
        speed = 100
        data = js.loads(request.data.decode('utf-8'))
        if data['speed']:
            speed = int(data['speed'])
            print(speed)
        json = '{"action": "left",  "speed": "' + str(speed) + '", "time_limit": "0"}'
        r.publish('DCMC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in turn_left")
        log.error(ex, exc_info=True)
        return "NOTOK"
    
    

@app.route('/index/turn_right', methods=['POST'])
def turn_right():
    print("turn_right")
    
    try:
        speed = 100
        data = js.loads(request.data.decode('utf-8'))
        if data['speed']:
            speed = int(data['speed'])
            print(speed)
        json = '{"action": "right",  "speed": "' + str(speed) + '", "time_limit": "0"}'
        r.publish('DCMC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in turn_right")
        log.error(ex, exc_info=True)
        return "NOTOK"




@app.route('/index/stop', methods=['POST'])
def stop():
    print("stop")
    
    try:
        
        json = '{"action": "stop",  "speed": "0", "time_limit": "0"}'
        r.publish('DCMC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in stop")
        log.error(ex, exc_info=True)
        return "NOTOK"

@app.route('/index/servo/down', methods=['POST'])
def servo_up():
    print("servo up")
    try: 
        json = '{"action": "up", "angle": "-1"}'
        r.publish('SC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in servo_up")
        log.error(ex, exc_info=True)
        return "NOTOK"

@app.route('/index/servo/up', methods=['POST'])
def servo_down():
    print("servo down")
    try: 
        json = '{"action": "down", "angle": "-1"}'
        r.publish('SC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in servo_down")
        log.error(ex, exc_info=True)
        return "NOTOK"

@app.route('/index/servo/right', methods=['POST'])
def servo_left():
    print("servo left")
    try: 
        json = '{"action": "left", "angle": "-1"}'
        r.publish('SC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in servo_left")
        log.error(ex, exc_info=True)
        return "NOTOK"


@app.route('/index/servo/left', methods=['POST'])
def servo_right():
    print("servo right")
    try: 
        json = '{"action": "right", "angle": "-1"}'
        r.publish('SC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in servo_right")
        log.error(ex, exc_info=True)
        return "NOTOK"

@app.route('/index/servo/init', methods=['POST'])
def servo_init():
    print("servo init")
    try: 
        json = '{"action": "dummy", "angle": "-1"}'
        r.publish('SC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in servo_init")
        log.error(ex, exc_info=True)
        return "NOTOK"



@app.route('/tts/speak', methods=['POST'])
def speak():
    print("speak api")
    
    try:
        sentence = ""
        data = js.loads(request.data.decode('utf-8'))
        if data['sentence']:
            sentence = data['sentence']
            print(sentence)
        json = '{"action": "speak",  "sentence": "' + str(sentence) + '"}'
        log.debug("sending json: {}".format(json))
        r.publish('TTSC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in speak")
        log.error(ex, exc_info=True)
        return "NOTOK"


@app.context_processor
def inject_user():
    return dict(URL=config.URL)

def start_runner():
    def start_loop():
        not_started = True
        time.sleep(3)
        while not_started:
            #log.debug('In start loop')
            try:
                r = requests.get('http://127.0.0.1:3000/stream')
                if r.status_code == 200:
                    log.debug('Stream Detection Server started, quiting start_loop')
                    not_started = False
                log.debug(r.status_code)
            except Exception as ex:
                log.debug('Stream Detection Server not yet started')
                #log.error(ex, exc_info=True)
            time.sleep(2)

    #log.debug('Started stream check runner')
    thread = threading.Thread(target=start_loop)
    thread.start()
def start_detector():
    
    dt.start_fast_detection(use_rabbit=True)
    
def main():
    try:
        global r
        global dt
        r = BROKER()
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        handler = RotatingFileHandler('AMSpiServer.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        start_runner()
        dt = Detector(use_tft=True)
        #thread = threading.Thread(target=start_detector)
        #thread.start()
        
        app.run(debug=False, host='0.0.0.0', port='3000')
    except Exception as ex:
        log.error("Exception in Main flask server")
        log.error(ex, exc_info=True)
        json = '{"action": "exit",  "speed": "0", "time_limit": "0"}'
        r.publish('DCMC', json)
        
# def gen():
    # """
    # Generator to continuously grab and yield frames from the Camera object.
    # """
    # ds = DestectionStream()
    # while True:
        # frame = ds.get_frame()
        # yield (b'--frame-boundary\r\nContent-Type: image/jpeg\r\n\r\n'
                # + bytearray(frame) + b'\r\n'
        # )
        # with app.app_context():
            # # Add nominal delay between frames to prevent performance issues.
            # time.sleep(0.1)

if __name__ == "__main__":
    main()
    

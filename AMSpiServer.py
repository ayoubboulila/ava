'''
Created on 30 janv. 2018

@author: AYB
'''
from flask import Flask, flash, redirect, render_template, request, session, abort
import jinja2
from AMSpi import AMSpi
import time
import config
import redis
import Logger
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
log = Logger.RCLog('AMSpiServer')

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('templates'),
])
app.jinja_loader = my_loader
r = redis.StrictRedis()
#===============================================================================
# ### ASM init
# cont = AMSpi() 
# 
# try:
#     
#     # pin 12 -> D7 is set per default 
#     cont.set_74HC595_pins(21, 20, 16)
#     
#     # Set PINs for controlling all 4 motors (GPIO numbering)
#     #amspi.set_L293D_pins(5, 6, 13, 19)
#     
#     # PWM2A -> DC_MOTOR_1
#     # PWM2B -> DC_MOTOR_2
#     
#     cont.set_L293D_pins(PWM2A=5, PWM2B=6)
# except Exception as ex:
#     print("exception setting 74HC595_pins or L293D_pins")
#     cont.clean_up()
#     traceback.print_exc()
#===============================================================================





@app.route('/')
@app.route('/index')
def index():
    
    test="ok"
    return render_template(
        'index.html',**locals())






@app.route('/index/forward', methods=['POST'])
def forward():
    log.debug("forward")
    try:
        #cont.go(70)
        json = '{"action": "go",  "speed": "100", "time_limit": "0"}'
        r.publish('DCMC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in forward")
        #cont.clean_up()
        log.error(ex, exc_info=True)
        return "NOTOK"
    
    
    
    

@app.route('/index/backword', methods=['POST'])
def backword():
    print("backword")
    try:
        #cont.go_back(70)
        json = '{"action": "back",  "speed": "100", "time_limit": "0"}'
        r.publish('DCMC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in backward")
        #cont.clean_up()
        log.error(ex, exc_info=True)
        return "NOTOK"
    
    


@app.route('/index/turn_left', methods=['POST'])
def turn_left():
    print("turn_left")
    try:
        #cont.turn_left(50)
        json = '{"action": "left",  "speed": "80", "time_limit": "0"}'
        r.publish('DCMC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in turn_left")
        #cont.clean_up()
        log.error(ex, exc_info=True)
        return "NOTOK"
    
    

@app.route('/index/turn_right', methods=['POST'])
def turn_right():
    print("turn_right")
    
    try:
        #cont.turn_right(50)
        json = '{"action": "right",  "speed": "80", "time_limit": "0"}'
        r.publish('DCMC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in turn_right")
        #cont.clean_up()
        log.error(ex, exc_info=True)
        return "NOTOK"




@app.route('/index/stop', methods=['POST'])
def stop():
    print("stop")
    
    try:
        #cont.stop()
        json = '{"action": "stop",  "speed": "0", "time_limit": "0"}'
        r.publish('DCMC', json)
        return "OK"
    except Exception as ex:
        log.error("exception in stop")
        #cont.clean_up()
        log.error(ex, exc_info=True)
        return "NOTOK"

@app.context_processor
def inject_user():
    return dict(URL=config.URL)


def main():
    try:
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        handler = RotatingFileHandler('AMSpiServer.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.run(debug=False, host='0.0.0.0')
    except Exception as ex:
        log.error("Exception in Main flask server")
        log.error(ex, exc_info=True)
        json = '{"action": "exit",  "speed": "0", "time_limit": "0"}'
        r.publish('DCMC', json)
        #cont.clean_up()

if __name__ == "__main__":
    main()
    
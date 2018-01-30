'''
Created on 30 janv. 2018

@author: AYB
'''
from flask import Flask, flash, redirect, render_template, request, session, abort
import jinja2
from AMSpi import AMSpi
import time
import config

try:
    import RPi.GPIO as GPIO
except Exception as ex:
    print("exception importing GPIO")



app = Flask(__name__)

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('templates'),
])
app.jinja_loader = my_loader

### ASM init

try:
    
    cont = AMSpi() 
    cont.set_74HC595_pins(21, 20, 16)
    # Set PINs for controlling all 4 motors (GPIO numbering)
    #amspi.set_L293D_pins(5, 6, 13, 19)
    cont.set_L293D_pins(PWM2A=5, PWM2B=6)
except Exception as ex:
    print("exception")
    #cont.__exit__(None, None, None)





@app.route('/')
@app.route('/index')
def index():
    
    test="ok"
    return render_template(
        'index.html',**locals())






@app.route('/index/forward', methods=['POST'])
def forward():
    print("forward")
    try:
        cont.go()
        return "OK"
    except Exception as ex:
        print("exception")
        cont.__exit__(None, None, None)
        return "NOTOK"
    
    
    
    

@app.route('/index/backword', methods=['POST'])
def backword():
    print("backword")
    try:
        cont.go_back()
        return "OK"
    except Exception as ex:
        print("exception")
        cont.__exit__(None, None, None)
        return "NOTOK"
    
    


@app.route('/index/turn_left', methods=['POST'])
def turn_left():
    print("turn_left")
    try:
        cont.turn_left()
        return "OK"
    except Exception as ex:
        print("exception")
        cont.__exit__(None, None, None)
        return "NOTOK"
    
    

@app.route('/index/turn_right', methods=['POST'])
def turn_right():
    print("turn_right")
    
    try:
        cont.turn_right()
        return "OK"
    except Exception as ex:
        print("exception")
        cont.__exit__(None, None, None)
        return "NOTOK"




@app.route('/index/stop', methods=['POST'])
def stop():
    print("stop")
    
    try:
        cont.stop()
        return "OK"
    except Exception as ex:
        print("exception")
        cont.__exit__(None, None, None)
        return "NOTOK"

@app.context_processor
def inject_user():
    return dict(URL=config.URL)



if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
    #app.run()
'''
Created on 1 mars 2018

@author: AYB
'''

from lib.agent import snowboydecoder
import sys, os
import signal
import redis
import Logger


interrupted = False
log = Logger.RCLog('AgentController')
RES_PATH = os.path.join(os.path.dirname(__file__),'lib', 'agent', 'resources')


AVA_MODEL = os.path.join(RES_PATH, 'ava.pmdl')
AVA_STOP_MODEL = os.path.join(RES_PATH, 'ava_stop.pmdl')
AVA_GO_MODEL = os.path.join(RES_PATH, 'ava_go.pmdl')


models = [AVA_MODEL, AVA_STOP_MODEL, AVA_GO_MODEL]



def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

def execute_action(action):
    log.debug('got action: '+ action)
    if action == 'ava': 
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
    elif action == 'ava_stop':
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    elif action == 'ava_go':
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)



def main():
    try:
        # capture SIGINT signal, e.g., Ctrl+C
        signal.signal(signal.SIGINT, signal_handler)

        sensitivity = [0.5]*len(models)
        detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
        callbacks = [lambda: execute_action('ava'), 
                     lambda: execute_action('ava_stop'), 
                     lambda: execute_action('ava_go')]
        log.debug('Listening... ')

        # main loop
        # make sure you have the same numbers of callbacks and models
        detector.start(detected_callback=callbacks,
                       interrupt_check=interrupt_callback,
                       sleep_time=0.03)

        detector.terminate()
        
    except Exception as ex:
        log.error("exception in AgentController")
        log.error(ex, exc_info=True)



if __name__ == "__main__":
    main()

'''
Created on 1 mars 2018

@author: AYB
'''

from lib.agent import snowboydecoder
import sys, os
import signal
import redis
import Logger


TTSC_CH = 'TTSC'
interrupted = False
log = Logger.RCLog('AgentController')
RES_PATH = os.path.join(os.path.dirname(__file__),'lib', 'agent', 'resources')


AVA_MODEL = os.path.join(RES_PATH, 'ava.pmdl')
AVA_STOP_MODEL = os.path.join(RES_PATH, 'ava_stop.pmdl')
AVA_GO_MODEL = os.path.join(RES_PATH, 'ava_go.pmdl')
AVA_BACK_MODEL = os.path.join(RES_PATH, 'ava_back.pmdl')
AVA_TURN_LEFT_MODEL = os.path.join(RES_PATH, 'ava_turn_left.pmdl')
AVA_TURN_RIGHT_MODEL = os.path.join(RES_PATH, 'ava_turn_right.pmdl')
AVA_WHO_ARE_YOU_MODEL = os.path.join(RES_PATH, 'ava_who_are_you.pmdl')
AVA_DANCE_MODEL = os.path.join(RES_PATH, 'ava_dance.pmdl')
AVA_FOLLOW_ME_MODEL = os.path.join(RES_PATH, 'ava_follow_me.pmdl')


models = [AVA_MODEL, AVA_STOP_MODEL, AVA_GO_MODEL, AVA_BACK_MODEL, AVA_TURN_LEFT_MODEL, AVA_TURN_RIGHT_MODEL, AVA_WHO_ARE_YOU_MODEL, AVA_DANCE_MODEL, AVA_FOLLOW_ME_MODEL]



def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

def execute_action(action, broker):
    log.debug('got action: '+ action)
    if action == 'ava': 
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        json = '{"action": "speak",  "sentence": " yes"}'
        broker.publish(TTSC_CH, json)
    elif action == 'ava_stop':
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
        json = '{"action": "speak",  "sentence": " ok stopping"}'
        broker.publish(TTSC_CH, json)
    elif action == 'ava_go':
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
        json = '{"action": "speak",  "sentence": " ok going forward"}'
        broker.publish(TTSC_CH, json)
    elif action == 'ava_back':
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
        json = '{"action": "speak",  "sentence": " ok going backward"}'
        broker.publish(TTSC_CH, json)
    elif action == 'ava_turn_left':
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
        json = '{"action": "speak",  "sentence": " ok turning left"}'
        broker.publish(TTSC_CH, json)
    elif action == 'ava_turn_right':
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
        json = '{"action": "speak",  "sentence": " ok turning right"}'
        broker.publish(TTSC_CH, json)
    elif action == 'ava_who_are_you':
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
        json = '{"action": "speak",  "sentence": " well, my name is ava, i am an artificial virtual assistant, i was created by a young software architect who got inspired by the ex machina movie, so he gave me the name of its main humanoid character"}'
        broker.publish(TTSC_CH, json)
    elif action == 'ava_dance':
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
        json = '{"action": "speak",  "sentence": " wooho lets put some music"}'
        broker.publish(TTSC_CH, json)
    elif action == 'ava_follow_me':
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
        json = '{"action": "speak",  "sentence": " ok sure master"}'
        broker.publish(TTSC_CH, json)



def main():
    try:
        # capture SIGINT signal, e.g., Ctrl+C
        signal.signal(signal.SIGINT, signal_handler)
        broker = redis.StrictRedis()

        sensitivity = [0.5]*len(models)
        detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
        callbacks = [lambda: execute_action('ava', broker), 
                     lambda: execute_action('ava_stop', broker), 
                     lambda: execute_action('ava_go', broker),
                     lambda: execute_action('ava_back', broker), 
                     lambda: execute_action('ava_turn_left', broker), 
                     lambda: execute_action('ava_turn_right', broker), 
                     lambda: execute_action('ava_who_are_you', broker), 
                     lambda: execute_action('ava_dance', broker), 
                     lambda: execute_action('ava_follow_me', broker)]
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

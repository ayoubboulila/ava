'''
Created on 2 mars 2018

@author: AYB
'''


import sys, os
import signal
import redis
from utils import Logger
import subprocess
import json
from time import sleep


# json =  '{"action": "speak",  "sentence": ""}'

log = Logger.RCLog('TTSController')
TTSC_CH = 'TTSC'

class TTS:
    _BIN_ = '/home/pi/builded_backup/mimic/mimic'
    _VOICE_ = 'slt'
    
    
    
    def __init__(self, BIN =_BIN_, VOICE =_VOICE_):
        self._BIN_PATH_ = BIN
        self._VOICE_ = VOICE
        
    
    def build_args(self):
        args = [self._BIN_, '-voice', self._VOICE_, '--setf', 'duration_stretch=1' , '-t']
        return args    
        
    def speak(self, sentence):
        subprocess.check_output(self.build_args() + [sentence])
    





def main():
    try:
        broker = redis.StrictRedis()
        sub = broker.pubsub()
        sub.subscribe(TTSC_CH)
        tts = TTS()
        while True:
            message = sub.get_message()
            if message and not isinstance(message['data'], int) and message['type'] == 'message':
                log.debug(type(message['data']))
                data = json.loads(message['data'].decode('utf-8'))
                log.debug("TTSC: received data:")
                log.debug(data)
                action = data['action']
                sentence = data['sentence']
                tts.speak(sentence)
            sleep(0.4)
                
    except Exception as ex:
        log.error("error in TTSController")
        log.error(ex, exc_info=True)
        
        
        
if __name__ == "__main__":
    main()   

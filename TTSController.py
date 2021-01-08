'''
Created on 2 mars 2018

@author: AYB
'''


import sys, os
import signal
#import redis
#from utils.RedisClient import RedisClient
#from utils.Broker import BROKER
from utils.RabbitCtl import BROKER
from utils import Logger
from lib.light.Rgb import RGB
import subprocess
import json
from time import sleep
import hashlib
import pyaudio
import wave
from ctypes import *

# json =  '{"action": "speak",  "sentence": ""}'

log = Logger.RCLog('TTSController')
TTSC_CH = 'TTSC'
HC_CH = 'HC'
# code to suppress pyaudio warnings
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)
class TTS:
    _BIN_ = '/home/pi/builded_backup/mimic/mimic'
    _VOICE_ = 'slt'
    _TEMP_DIR = '/tmp/ava/out'
    
    
    
    def __init__(self, BIN =_BIN_, VOICE =_VOICE_):
        self._BIN_PATH_ = BIN
        self._VOICE_ = VOICE
        try:
            if not os.path.exists(os.path.dirname(self._TEMP_DIR)):
                os.makedirs(self._TEMP_DIR)
        except Exception as ex:
            print("exception in tempdir")
            
        
    
    def build_args(self):
        args = [self._BIN_, '-voice', self._VOICE_, '--setf', 'duration_stretch=1', '-t']
        return args    
        
    def speak(self, sentence):
        self.hash = self.generate_hash(sentence)
        mimic_file = os.path.join(self._TEMP_DIR, self.hash)
        command = self.build_args() + [sentence, '-o', mimic_file] 
        if not os.path.exists(mimic_file):
            print("command")
            print(command)
            subprocess.check_output(command)
        
        #subprocess.check_output(['aplay', mimic_file])
        wave_data = wave.open(mimic_file, 'rb')
        #with noalsaerr():
        audio = pyaudio.PyAudio()
        #define callback
        def chunk_callback(in_data, frame_count, time_info, status):
            chunk = wave_data.readframes(frame_count)
            return (chunk, pyaudio.paContinue)
        #open stream using callback
        #channels=wave_data.getnchannels()
        stream = audio.open(format=audio.get_format_from_width(wave_data.getsampwidth()),
                            channels=1,
                            rate=wave_data.getframerate(),
                            output=True,
                            stream_callback=chunk_callback)
        #start the stream
        # if broker != None:
        # broker.publish(HC_CH, '{"action": "play",  "anime": "talk"}')
        RGB.get_instance().set_color("w")
        stream.start_stream()
        #wait for the stream to finish
        while stream.is_active():
            sleep(0.1)
        #stop stream
        stream.stop_stream()
        # if broker != None:
            # broker.publish(HC_CH, '{"action": "play",  "anime": "standby"}')
        stream.close()
        wave_data.close()
        #close Pyaudio
        audio.terminate()
        RGB.get_instance().standby()
            
        
    
    def generate_hash(self, sentence):
        hash_obj = hashlib.sha256(sentence.encode('utf-8'))
        hex_digest = hash_obj.hexdigest()
        return hex_digest
    
    

def callback(ch, method, properties, message):
    tts = TTS()
    log.debug("callback received message: ".format(message.decode('utf-8')))
    data = json.loads(message.decode('utf-8'))
    log.debug("TTSC: received data:")
    log.debug(data)
    action = data['action']
    sentence = data['sentence']
    #broker.publish(HC_CH, '{"action": "play",  "anime": "talk"}')
    tts.speak(sentence)
    #broker.publish(HC_CH, '{"action": "play",  "anime": "standby"}')
    sleep(0.4)



def main():
    try:
        #broker = redis.StrictRedis()
        #broker = RedisClient().conn
        #sub = broker.pubsub()
        #tts = TTS()
        sub = BROKER()
        sub.subscribe(callback,TTSC_CH)
        
        # while True:
            # topic, message = sub.get_b()
            # if message != None:
                # log.debug(message)
                # data = json.loads(message)
                # log.debug("TTSC: received data:")
                # log.debug(data)
                # action = data['action']
                # sentence = data['sentence']
                # #broker.publish(HC_CH, '{"action": "play",  "anime": "talk"}')
                # tts.speak(sentence, broker)
                # #broker.publish(HC_CH, '{"action": "play",  "anime": "standby"}')
            # sleep(0.4)
                
    except Exception as ex:
        log.error("error in TTSController")
        log.error(ex, exc_info=True)
        
        
        
if __name__ == "__main__":
    main()   

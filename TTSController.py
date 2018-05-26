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
import hashlib
import pyaudio
import wave

# json =  '{"action": "speak",  "sentence": ""}'

log = Logger.RCLog('TTSController')
TTSC_CH = 'TTSC'
HC_CH = 'HC'

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
        
    def speak(self, sentence, broker=None):
        self.hash = self.generate_hash(sentence)
        mimic_file = os.path.join(self._TEMP_DIR, self.hash)
        command = self.build_args() + [sentence, '-o', mimic_file] 
        if not os.path.exists(mimic_file):
            print("command")
            print(command)
            subprocess.check_output(command)
        
        #subprocess.check_output(['aplay', mimic_file])
        wave_data = wave.open(mimic_file, 'rb')
        audio = pyaudio.PyAudio()
        #define callback
        def chunk_callback(in_data, frame_count, time_info, status):
            chunk = wave_data.readframes(frame_count)
            return (chunk, pyaudio.paContinue)
        #open stream using callback
        stream = audio.open(format=audio.get_format_from_width(wave_data.getsampwidth()),
                            channels=wave_data.getnchannels(),
                            rate=wave_data.getframerate(),
                            output=True,
                            stream_callback=chunk_callback)
        #start the stream
        if broker != None:
            broker.publish(HC_CH, '{"action": "play",  "anime": "talk"}')
        stream.start_stream()
        #wait for the stream to finish
        while stream.is_active():
            sleep(0.1)
        #stop stream
        stream.stop_stream()
        if broker != None:
            broker.publish(HC_CH, '{"action": "play",  "anime": "standby"}')
        stream.close()
        wave_data.close()
        #close Pyaudio
        audio.terminate()
            
        
    
    def generate_hash(self, sentence):
        hash_obj = hashlib.sha256(sentence.encode('utf-8'))
        hex_digest = hash_obj.hexdigest()
        return hex_digest
    
    





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
                #broker.publish(HC_CH, '{"action": "play",  "anime": "talk"}')
                tts.speak(sentence, broker)
                #broker.publish(HC_CH, '{"action": "play",  "anime": "standby"}')
            sleep(0.4)
                
    except Exception as ex:
        log.error("error in TTSController")
        log.error(ex, exc_info=True)
        
        
        
if __name__ == "__main__":
    main()   

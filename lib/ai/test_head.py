'''
Created on 4 avr. 2018

@author: AYB
'''


from lib.ai.Head import AVA
from time import sleep


ava = AVA()
ava.set_motion(ava.CONFIG.AVA_STANDBY_ANIME)
sleep(5)
ava.set_motion(ava.CONFIG.AVA_TALK_ANIME)
    
print(ava.CONFIG.AVA_STANDBY_ANIME)   
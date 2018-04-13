'''
Created on 4 avr. 2018

@author: AYB
'''

import os, sys


BASE = os.path.dirname(__file__)
RES_PATH = os.path.abspath(os.path.join(BASE, '..', '..', 'static', 'img', 'vid'))
print(RES_PATH)
AVA_STANDBY_ANIME = os.path.join(RES_PATH, 'standby__.avi')
AVA_TALK_ANIME = os.path.join(RES_PATH, 'talking__.avi')

print(AVA_STANDBY_ANIME)

ANIME_LIST = [AVA_STANDBY_ANIME, AVA_TALK_ANIME]

class Config:
    AVA_STANDBY_ANIME = AVA_STANDBY_ANIME
    AVA_TALK_ANIME = AVA_TALK_ANIME
    
    def __init__(self):
        pass
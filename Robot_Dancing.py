# -*- coding: utf-8 -*-
'''
Created on Sat Feb  7 22:19:47 2015
@author: guermoule
'''
import time 
import json
#from poppy.creatures import PoppyHumanoid
from Primitives.Pop_Dance_Primitive import SimpleBodyBeatMotion
import pypot.robot

''' 
# Simulated Robot Via V-REP  
poppy = PoppyHumanoid(simulator='vrep')
'''

# Reel Robot
poppy_config_file = './Config/poppy_config.json'
with open(poppy_config_file) as f:
    poppy_config = json.load(f) 
	
#poppy = PoppyHumanoid(config=poppy_config)
poppy = pypot.robot.from_config(poppy_config)
poppy.start_sync()

poppy.attach_primitive(SimpleBodyBeatMotion, 'dance_beat_motion')

dance = poppy.dance_beat_motion(poppy, 60)
dance.start()
 
time.sleep(50)

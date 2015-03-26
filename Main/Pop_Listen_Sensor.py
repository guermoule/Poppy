"""
Pop_Listen_Sensors
Collecte Data from Arduino sent by Sensors 

Author : H. Guermoule
"""

import os
from subprocess import call, DEVNULL
import serial
from time import sleep
#import pyaudio
#import wave

class serialEvent :
  def __init__(self, myPort, baudrate=115200):
      # open serial port
      self.ser = serial.Serial(myPort, baudrate)
      self.firstContact = False
      
      self.sensors = []
	  
  def update(self):     
      # read the serial buffer:
      myString = self.ser.readline()
      
      # if you got any bytes other than the linefeed:
      if (len(myString) != 0) :       
         # if you haven't heard from the microncontroller yet, listen:     
         if (self.firstContact == False or myString.rstrip() == 'hello') :
            self.ser.flushInput()        # clear the serial port buffer
            self.firstContact = True     # you've had first contact from the microcontroller
            self.ser.write('Go\n')       #ask for more data  
            return 0
         # if you have heard from the microcontroller: proceed
         else :
            # split the string at the commas and convert the sections into float:
            self.sensors = [float(val) for val in myString.split(",")]
			
			'''
            # print out the values you got:     
            for self.sensorNum in range(len(self.sensors)) :     
                print 'Sensor ',self.sensorNum, ':', self.sensors[self.sensorNum], '\t',
            print('\n')
            '''             
         # ask for more:   
         self.ser.write('Go\n')
         return 1
  
  # clean up		
  def close(self):
      # close serial
      self.ser.flush()
      self.ser.close() 
     
 # Action Mik
def Action_Mik(Val_mik1, Val_mik2, L_robot):

    L_tershold = 200.0
    Perc_tershold = 25

    if (Val_mik1 < L_tershold and Val_mik2 < L_tershold) :
		return 0
    Delta_val_mik = Val_mik1 - Val_mik2
    Per_cent_vals = (abs(Delta_val_mik) * 100)/max(Val_mik1,Val_mik2)
    
	"""
	if (Per_cent_vals >= Perc_tershold):
       print(Per_cent_vals)
       print('\n')
    """
    
	if (Delta_val_mik <= 0 and Per_cent_vals >= Perc_tershold) :
	    L_robot.Head_sound_motion.which_side = 'Right_Side'
    elif (Delta_val_mik > 0 and Per_cent_vals >= Perc_tershold):
	    L_robot.Head_sound_motion.which_side = 'Left_Side'
    else :
	    L_robot.Head_sound_motion.which_side = 'Center_Side'
 
    L_robot.Head_sound_motion.start()
    L_robot.Head_sound_motion.wait_to_stop()
    sleep(2)    
    Aplay_wave ()
    #sleep(2)
	
def Save_mik_to_file(Val_mik, outfile):  
      outfile.write(str(Val_mik))

def Aplay_wave():
    # DEVNULL ou None
    wf = "../Statics/Bonjour.wav"
    cmd = ['aplay', str(wf)]
    call(cmd, stdout=DEVNULL, stderr=DEVNULL)
    
# main() function
def main():
  import json 
  import pypot.robot 
  from Destin_Head_Primitive import Sound_Detect_Motion 
  
  # Serial Port to Arduino (Io Card)  
  strPort = '/dev/ttyACM0'
  
  fname = 'f_output_mik.dat'
  outfile = open(fname,'w')
  
  '''  
  from pypot.vrep import from_vrep
  from pypot.vrep import close_all_connections
  # Simulated Robot Via V-REP
  scene_path = '/Applications/V-REP_PRO_EDU_V3_2_0_Mac/scenes/poppy_humanoid.ttt'
  poppy = from_vrep(poppy_config, '127.0.0.1', 19997, scene_path)
  '''
  
  # Reel Robot
  poppy_config_file = '../Config/poppy_config.json'
  with open(poppy_config_file) as f:
     poppy_config = json.load(f)

  poppy = pypot.robot.from_config(poppy_config)
  poppy.start_sync() 
 
  # Init robot position 
  poppy.compliant = False 
  poppy.power_up() 
  
  Sensors_Event = serialEvent(strPort)
  poppy.attach_primitive(Sound_Detect_Motion(poppy), 'Head_sound_motion')

  while True : 
      try:
        if (Sensors_Event.update() != 0) :
            #Save_mik_to_file(max(Sensors_Event.sensors[0],Sensors_Event.sensors[1]), outfile)
            Action_Mik(Sensors_Event.sensors[0],Sensors_Event.sensors[1], poppy)
	        #Action_Temp_Hum(sensors[2])
	        # Others sensors ...
      except KeyboardInterrupt:
         print('exiting')   
         # clean up
         Sensors_Event.close()
         outfile.close()
         break

# call main
if __name__ == '__main__':
  main()
 


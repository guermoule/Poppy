'''
Pop_Listen_Sensors
Collecte Data from Arduino sent by Sensors ans make Action 

Author : H. Guermoule
'''

import serial
from time import sleep
from Audio.tts import PicoTTS
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
    # Define tersholds
    L_tershold = 200.0
    Perc_tershold = 25
    speaker = PicoTTS()
    salutation = ' Salut ! que puis-je pour toi ?'
    silence = False

    if (Val_mik1 < L_tershold and Val_mik2 < L_tershold) :
		return 0
    delta_val_mik = Val_mik1 - Val_mik2
    per_cent_vals = (abs(delta_val_mik) * 100)/max(Val_mik1,Val_mik2)
    
    if (per_cent_vals >= Perc_tershold):
       print(per_cent_vals)
       #print('\n')
       
    if (delta_val_mik <= 0 and per_cent_vals >= Perc_tershold) :
	    L_robot.Head_sound_motion.which_side = 'Right_Side'
    elif (delta_val_mik > 0 and per_cent_vals >= Perc_tershold):
	    L_robot.Head_sound_motion.which_side = 'Left_Side'
    else :
	    L_robot.Head_sound_motion.which_side = 'Center'
            silence = True
 
    L_robot.Head_sound_motion.start()
    L_robot.Head_sound_motion.wait_to_stop()
    sleep(2)    
    if silence == False :
         speaker.say(salutation)
         #sleep(2)
	
def Save_mik_to_file(Val_mik, outfile):  
      outfile.write(str(Val_mik))

    
# main() function
def main():
  import json 
  import pypot.robot 
  #from poppy_Humanoid_Part import PoppyHumanoidPart
  from Primitives.Destin_Head_Primitive import Sound_Detect_Motion
  
  # Serial Port to Arduino (Io Card)  
  strPort = '/dev/ttyACM0'
  
  fname = './Out/f_output_mik.dat'
  outfile = open(fname,'w')
  
  ''' 
  # Simulated Robot Via V-REP  
  poppy = PoppyHumanoid(simulator='vrep')
  '''
  
  # Reel Robot
  poppy_config_file = './Config/poppy_config.json'
  with open(poppy_config_file) as f:
     poppy_config = json.load(f)
  #poppy = PoppyHumanoidPart(config=poppy_config)
  poppy = pypot.robot.from_config(poppy_config)
  
  # Init robot 
  poppy.start_sync()  
  poppy.power_up() 
  
  poppy.attach_primitive(Sound_Detect_Motion(poppy), 'Head_sound_motion')
  Sensors_Event = serialEvent(strPort)


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
 


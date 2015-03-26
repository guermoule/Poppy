"""
ldr.py
Display analog data from Arduino using Python (matplotlib)
"""
 
import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque
 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

    
# plot class
class AnalogPlot:
  # constr
  def __init__(self, strPort, maxLen):
      # open serial port
      self.ser = serial.Serial(strPort, 115200)
 
      self.ax = deque([0.0]*maxLen)
      self.ay = deque([0.0]*maxLen)
      self.maxLen = maxLen
      self.firstContact = False
      
  # add to buffer
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.append(val)
      else:
          buf.pop()
          buf.appendleft(val)
 
  # add data
  def add(self, data):
      assert(len(data) == 2)
      self.addToBuf(self.ax, data[0])
      self.addToBuf(self.ay, data[1])
 
  # update plot

  def update(self, frameNum, a0, a1):
      try:
          line = self.ser.readline()
          
          if (self.firstContact == False or line.rstrip() == 'hello') :
            self.ser.flushInput()        # clear the serial port buffer
            self.firstContact = True     # you've had first contact from the microcontroller
            self.ser.write('Go\n')       #ask for more 


          else :  
            #print(line)  
            data = [float(val) for val in line.split(',')]
            # print data
            if(len(data) == 2):
              self.add(data)
              a0.set_data(range(self.maxLen), self.ax)
              a1.set_data(range(self.maxLen), self.ay)

      except KeyboardInterrupt:
          print('exiting')
      # more data   
      self.ser.write('Go\n')  
      return a0, 
 
  # clean up
  def close(self):
      # close serial
      self.ser.flush()
      self.ser.close()    
 
# main() function
def main():
  # create parser
  parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
  #parser.add_argument('--port', dest='port', required=True)
 
  # parse args
  args = parser.parse_args()
  
  strPort = '/dev/tty.usbmodem1421'
  #strPort = args.port
 
  print('reading from serial port %s...' % strPort)
 
  # plot parameters
  analogPlot = AnalogPlot(strPort, 100)
 
  print('plotting data...')
 
  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, 100), ylim=(0, 4))
  ax.set_title('Sampling Mik Voltage')
  ax.set_xlabel('time (ms)')
  ax.set_ylabel('voltage (mV)')
  #plt.grid(True)

  

  a0, = ax.plot([], [])
  a1, = ax.plot([], [])
  anim = animation.FuncAnimation(fig, analogPlot.update, 
                                 fargs=(a0, a1), 
                                 interval=50)
 
  anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
 
  # show plot
  plt.show()
  
  # clean up
  analogPlot.close()
 
  print('exiting.')
  
 
# call main
if __name__ == '__main__':
  main()

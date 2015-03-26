
#!/usr/bin/python

# Short program using pySerial module to write Arduino serial 
# data to a file.

import sys
import serial as ser

# Arduino serial port
addr = '/dev/ttyACM0'
baud = 115200
fname = sys.argv[1]
fmode = 'w'
reps = 18000

ard = ser.Serial(addr,baud)

outfile = open(fname,fmode)

for i in range(reps):
    x = ard.readline()
    outfile.write(x)
    # outfile.flush()

outfile.close()
 
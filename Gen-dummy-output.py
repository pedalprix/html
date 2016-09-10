#!/usr/bin/env python

import time

header = """Team              : Naracoorte High School
  Lap Number      : """
footer = """\nAverage Lap Time: 2:23.44
  Current Rider   : BenV
  Last 3 Laps -
    LapNo       Rider		Lap Time	Lap Start Time  Lap Finish Time
     22         NathanM		3:06.45		23:06.45	23:06.45
     21         NathanM		3:36.45		23:06.45	23:06.45
     20         BenV		3:06.45		23:06.45	23:06.45
  Fastest 3 Laps -
    LapNo       Rider		Lap Time	Lap Start Time  Lap Finish Time
     01         AlexM		3:06.45		23:06.45	23:06.45
     12         NathanM		3:06.45		23:06.45	23:06.45
     20         BenV		3:06.45		23:06.45	23:06.45
  Diagnostics -
    Time since last GPS message  : 4 seconds
    Time since last RFID message : 7 seconds"""

counter = 0
try:
   while True:
      ofile = open("Left.txt", "w")
      blob = header + str(counter) + footer
      ofile.write(blob)
      ofile.close() 
      counter += 1
      time.sleep(1)
except:
   pass

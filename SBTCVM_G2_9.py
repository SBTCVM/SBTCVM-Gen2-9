#!/usr/bin/env python
import VMSYSTEM.libbaltcalc as libbaltcalc
from VMSYSTEM.libbaltcalc import btint
import VMSYSTEM.MEM_G2x_9
import VMSYSTEM.CPU_G2x_9
import VMSYSTEM.IO_G2x_9
import VMSYSTEM.UIO_CURSES_G2x_9 as UIO
import time
import sys
import os
import curses
from threading import Thread
progrun=0
uiosys=None
try:
	cmd=sys.argv[1]
except:
	cmd=None
try:
	arg=sys.argv[2]
except:
	arg=None
if cmd in ['help', '-h', '--help']:
	print('''SBTCVM Gen2-9 virtual machine. curses frontend.
help, -h, --help: this help.
-v, --version: VM version
-a, --about: about SBTCVM
[trom], -r [trom], --run [trom]: launch SBTCVM with the selected TROM image 
    loaded into memory.
-s [trom] {CPU speed in Hz}, --slow [trom] {CPU speed in Hz}:
   -s overrides the default CPU clock speed. You may specify a float/int Hz value
    (after the trom filename). defaults to 2Hz''')
elif cmd in ["-a", "--about"]:
	print('''SBTCVM Gen2-9 virtual machine. curses frontend.
v2.1.0.alpha

Copyright (c) 2016-2018 Thomas Leathers and Contributors 

see readme.md for more information and licensing of media.

  SBTCVM Gen2-9 is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  SBTCVM Gen2-9 is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with SBTCVM Gen2-9. If not, see <http://www.gnu.org/licenses/>
  
  ''')
elif cmd in ['-v', '--version']:
	print('v2.1.0.alpha')
else:
	slow=0
	if cmd==None:
		romfile='TESTSHORT.TROM'
	elif cmd in ['-r', '--run']:
		if arg==None:
			sys.exit("Error! Must specify trom to run!")
		romfile=arg
	elif cmd in ['-s', '--slow']:
		if arg==None:
			sys.exit("Error! Must specify trom to run!")
		romfile=arg
		slow=1
		try: 
			targspeed=float(sys.argv[3])/1000.0
			slowspeed=1/(targspeed*1000.0)
		except IndexError:
			print("Using default slow delay. (2 hz)")
			targspeed=2/1000.0
			slowspeed=1/(targspeed*1000.0)
		except ValueError:
			sys.exit("Error. please specify slow delay as float or int.")
	else:
		romfile=cmd
	if slow==1:
		targtime=slowspeed
	else:
		#targspeed is in khz. acuracy may vary.
		targspeed=6.5#approx. speed should be close.
		#calculate approx speed.
		targtime=1/(targspeed*1000.0)
	try:
		
		print("SBTCVM Generation 2 9-trit VM, v2.1.0.alpha\n")
		#initialize memory subsystem
		memsys=VMSYSTEM.MEM_G2x_9.memory(romfile)
		#initialize IO subsystem
		iosys=VMSYSTEM.IO_G2x_9.io()
		
		cpusys=VMSYSTEM.CPU_G2x_9.cpu(memsys, iosys)
		progrun=1
		
		#curses startup
		curses.initscr()
		curses.noecho()
		curses.cbreak()
		mainscr=curses.initscr()
		mainscr.keypad(1)
		mainscr.nodelay(1)
		
		mhig, mwid = mainscr.getmaxyx()
		statwin = curses.newwin(2, mwid, 0, 0)
		ttywin = curses.newwin(mhig-2, mwid, 2, 0)
		maxy, maxx=ttywin.getmaxyx()
		
		ttywin.addstr(maxy-1, 0, "SBTCVM Curses frontend. SBTCVM Gen2-9 v2.1.0")
		ttywin.scrollok(1)
		ttywin.scroll(1)
		ttywin.refresh()
		
		#uio startup
		uiosys = UIO.uio(cpusys, memsys, iosys, statwin, ttywin, mainscr)
		dispthr=Thread(target = uiosys.statup, args = [])
		dispthr.daemon=True
		dispthr.start()
		uiosys.ttyraw("ready.")
		
		time.sleep(0.5)
		ttywin.redrawwin()
		ttywin.refresh()
		statwin.redrawwin()
		statwin.refresh()
		#main loop
		clcnt=0.0
		starttime=time.time()
		while progrun:
			#CPU Parse
			retval=cpusys.cycle()
			#increment clock tick.
			clcnt+=1
			#project when the next cycle should start, then subtract current time.
			xtime=(starttime + (clcnt - 1.0) * targtime) - time.time()
			#sleep for remaining time (xtime) if it is above 0
			if xtime>0.0:
				time.sleep(xtime)
			#exit code:
			if retval!=None:
				curses.echo()
				curses.endwin()
				uiosys.powoff()
				print("VMSYSHALT " + str(retval[1]) + ": " + retval[2])
				print("Approx. Speed: '" + str((float(clcnt)/(time.time()-starttime))/1000) + "' KHz")
				print("Target Speed : '" + str(targspeed) + "' Khz")
				
				progrun=0
	#in case of drastic failure, shutdown curses!
	finally:
		if progrun:
			curses.echo()
			curses.endwin()

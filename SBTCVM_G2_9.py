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
[trom], -r [trom], --run [trom]: launch SBTCVM with the selected TROM image 
    loaded into memory.
-s [trom] {slow delay in seconds}, --slow [trom] {slow delay in seconds}:
   -s overrides the default CPU clock delay. You may specify a float/int number
    of seconds to use (after the trom filename). defaults to 0.5 second delay
    per clock tick''')
elif cmd in ['-v', '--version']:
	print('v2.1.0.PRE-ALPHA')
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
			slowspeed=float(sys.argv[3])
		except IndexError:
			print("Using default slow delay. (0.5 seconds)")
			slowspeed=0.5
		except ValueError:
			sys.exit("Error. please specify slow delay as float or int.")
	else:
		romfile=cmd
	if slow==1:
		clspeed=slowspeed
	else:
		#targspeed is in khz. acuracy may vary.
		targspeed=6.5#approx. speed should be close.
		clspeed=1/(targspeed*1000.0)
		print(clspeed)
	try:
		
		print("SBTCVM Generation 2 9-trit VM, v2.1.0.PRE-ALPHA\n")
		#initialize memory subsystem
		memsys=VMSYSTEM.MEM_G2x_9.memory(romfile)
		#initialize IO subsystem
		iosys=VMSYSTEM.IO_G2x_9.io()
		
		cpusys=VMSYSTEM.CPU_G2x_9.cpu(memsys, iosys)
		progrun=1
		curses.initscr()
		curses.noecho()
		curses.cbreak()
		mainscr=curses.initscr()
		mainscr.keypad(1)
		
		#basic mainloop.
		mhig, mwid = mainscr.getmaxyx()
		statwin = curses.newwin(2, mwid, 0, 0)
		ttywin = curses.newwin(mhig-2, mwid, 2, 0)
		maxy, maxx=ttywin.getmaxyx()
		
		ttywin.addstr(maxy-1, 0, "SBTCVM Curses frontend. SBTCVM Gen2-9 v2.1.0")
		ttywin.scrollok(1)
		ttywin.scroll(1)
		ttywin.refresh()
		#statwin.addstr("r1: 0, r2: 0")
		#statwin.refresh()
		
		uiosys = UIO.uio(cpusys, memsys, iosys, statwin, ttywin)
		
		dispthr=Thread(target = uiosys.statup, args = [])
		dispthr.daemon=True
		dispthr.start()
		uiosys.ttyraw("ready.")
		stime=time.time()
		clcnt=0.0
		targtime=clspeed
		sleeptarg=targtime/10.0
		tbeg=time.time()
		while progrun:
			retval=cpusys.cycle()
			clcnt+=1
			xtime=(tbeg + (clcnt - 1.0) * targtime) - time.time()
			if xtime>0.0:
				time.sleep(xtime)
			if retval!=None:
				progrun=0
				uiosys.run=0
				curses.echo()
				curses.endwin()
				print("VMSYSHALT " + str(retval[1]) + ": " + retval[2])
				print("Approx. Speed: '" + str((float(clcnt)/(time.time()-stime))/1000) + "' KHz")
				print("Target Speed : '" + str(targspeed) + "' Khz")
	#in case of drastic failure, shutdown curses!
	finally:
		if progrun:
			if uiosys!=None:
				uiosys.run=0
			curses.endwin()
		
			

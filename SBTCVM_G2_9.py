#!/usr/bin/env python
import VMSYSTEM.libbaltcalc as libbaltcalc
from VMSYSTEM.libbaltcalc import btint
import VMSYSTEM.MEM_G2x_9
import VMSYSTEM.CPU_G2x_9
import VMSYSTEM.IO_G2x_9
import time
import sys
import os


try:
	cmd=sys.argv[1]
except:
	cmd=None
try:
	arg=sys.argv[2]
except:
	arg=None
if cmd in ['help', '-h', '--help']:
	print('''SBTCVM Gen2-9 virtual machine. pygame frontend.
help, -h, --help: this help.
-v, --version: VM version''')
elif cmd in ['-v', '--version']:
	print('v2.1.0.PRE-ALPHA')
else:
	if cmd==None:
		romfile='TESTSHORT.TROM'
	elif cmd in ['-r', '--run']:
		if arg==None:
			sys.exit("Error! Must specify trom to run!")
		romfile=arg
	else:
		romfile=cmd
	print("SBTCVM Generation 2 9-trit VM, v2.1.0.PRE-ALPHA\n")
	#initialize memory subsystem
	memsys=VMSYSTEM.MEM_G2x_9.memory(romfile)
	#initialize IO subsystem
	iosys=VMSYSTEM.IO_G2x_9.io()
	
	cpusys=VMSYSTEM.CPU_G2x_9.cpu(memsys, iosys)
	
	
	#basic mainloop.
	print("begin mainloop")
	while True:
		time.sleep(0.0001)
		time.sleep(1)
		cpusys.cycle()

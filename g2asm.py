#!/usr/bin/env python
import VMSYSTEM.libbaltcalc as libbaltcalc
import sys
import os
import VMSYSTEM.iofuncts as iofuncts
import VMSYSTEM.g2asmlib as g2asmlib
from VMSYSTEM.g2asmlib import mainloop
#common vars:
asmvers='v3.0.0'
versint=(3, 0, 0)



if __name__=="__main__":
	try:
		cmd=sys.argv[1]
	except:
		cmd=None
	try:
		arg=sys.argv[2]
	except:
		arg=None
	if cmd in ['help', '-h', '--help']:
		print('''SBTCVM assembler v3
For SBTCVM Gen2-9.
help, -h, --help: this help
-v, --version: assembler version
-b, (tasmname): build SBTCVM tasm source file into rom at same location.
-s, --syntax (tasmname): run assembler up to final sanity checks, but don't write rom image.
(tasmname): same as -b/--build''')
	elif cmd in ['-v', '--version']:
		print(asmvers)
	else:
		if cmd==None:
			print("Tip: Try g2-asm.py -h for help.")
			sys.exit()
		if cmd in ['-b', '--build', '-s', '--syntax']:
			argx=arg
		else:
			argx=cmd
		if cmd in ['-s', '--syntax']:
			syntaxonly=1
		else:
			syntaxonly=0
		
		#locate source file and extract destination basename and directory for mainloop class.
		pathx=iofuncts.findtrom(argx, ext=".tasm", exitonfail=1, exitmsg="source file was not found. STOP")
		basepath=pathx.rsplit(".", 1)[0]
		bpdir=os.path.dirname(basepath)
		bpname=os.path.basename(basepath)
		
		#open source file and init mainloop class
		sourcefile=open(pathx, 'r')
		mainl=mainloop(sourcefile, bpdir, bpname)
		
		#parse header
		mainl.headload()
		
		#parse each pass in order.
		if mainl.p0():
			sys.exit("Syntax Error (pass 0)")
		mainl.p1()
		if mainl.p2():
			sys.exit("Syntax Error (pass 2)")
		mainl.p3()
		if mainl.p4():
			sys.exit("Error: Invalid romdata! (pass 4)")
		if not syntaxonly:
			mainl.p5()
		sourcefile.close()
	
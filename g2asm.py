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
-b, (tasmname/sasname): build SBTCVM tasm source file into rom at same location or run sas script.
-s, --syntax (tasmname): run assembler up to final sanity checks, but don't write rom image.
(tasmname/sasname): same as -b/--build''')
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
		if cmd in ['-y', '--syntax']:
			syntaxonly=1
		else:
			syntaxonly=0
		pathx=iofuncts.findtrom(argx, ext=".sas", exitonfail=0, exitmsg="source file was not found. STOP")
		if pathx==None:
			pathx=iofuncts.findtrom(argx, ext=".tasm", exitonfail=1, exitmsg="source file was not found. STOP")
			g2asmlib.assemble(pathx, syntaxonly)
		elif pathx.lower().endswith(".tasm"):
			pathx=iofuncts.findtrom(argx, ext=".tasm", exitonfail=1, exitmsg="source file was not found. STOP")
			g2asmlib.assemble(pathx, syntaxonly)
		elif pathx.lower().endswith(".sas"):
			g2asmlib.sasparse(pathx, syntaxonly)
			
		
	
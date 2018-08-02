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
-a, --about: about SBTCVM
-b, (tasmname/xasname): build SBTCVM tasm source file into rom at same location or run an xas script.
-s, --syntax (tasmname): run assembler up to final sanity checks, but don't write rom image.
(tasmname/xasname): same as -b/--build''')
	elif cmd in ['-v', '--version']:
		print(asmvers)
	elif cmd in ["-a", "--about"]:
		print('''SBTCVM Assembler v3
''' + asmvers + '''
part of SBTCVM-Gen2-9 (v2.1.0.alpha)

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
		pathx=iofuncts.findtrom(argx, ext=".xas", exitonfail=0, exitmsg="xas file was not found. STOP")
		if pathx==None:
			pathx=iofuncts.findtrom(argx, ext=".tasm", exitonfail=1, exitmsg="source/xas file was not found. STOP")
			g2asmlib.assemble(pathx, syntaxonly)
		elif pathx.lower().endswith(".tasm"):
			pathx=iofuncts.findtrom(argx, ext=".tasm", exitonfail=1, exitmsg="source/xas file was not found. STOP")
			g2asmlib.assemble(pathx, syntaxonly)
		elif pathx.lower().endswith(".xas"):
			g2asmlib.xasparse(pathx, syntaxonly)
			
		
	
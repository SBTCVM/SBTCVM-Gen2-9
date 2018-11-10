#!/usr/bin/env python
import VMSYSTEM.libbaltcalc as libbaltcalc
import sys
import os
import VMSYSTEM.iofuncts as iofuncts
import VMSYSTEM.stnplib as stnplib
#from VMSYSTEM.g2asmlib import mainloop




stnpvers=stnplib.stnpvers
versint=stnplib.versint




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
		print('''SBTCVM simplified ternary numeric programming language.
--For SBTCVM Gen2-9.
   help, -h, --help: this help
   -v, --version: stnp compiler version
   -a, --about: about SBTCVM
   -c [sourcefile], --compile [sourcefile]: Compile source file into a tasm file,
      then run the assembler on it automatically, if successful.
   [sourcefile]: same as -c
   Note: if source is example.stnp, tasm file will be example__stnp.tasm. rom
   will be example.trom''')
	elif cmd in ['-v', '--version']:
		print(stnpvers)
	elif cmd in ["-a", "--about"]:
		print('''SBTCVM simplified ternary numeric programming language.
''' + stnpvers + '''
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
	if cmd == None:
		print("Tip: Try stnpcom.py -h for help.")
	else:
		if cmd in ['-c', '--compile']:
			argx=arg
		else:
			argx=cmd
		pathx=iofuncts.findtrom(argx, ext=".stnp", exitonfail=1, exitmsg="stnp file was not found. STOP", dirauto=1)
		stnplib.compwrap(pathx)
		
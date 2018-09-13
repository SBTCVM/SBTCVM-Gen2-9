#!/usr/bin/env python
import VMSYSTEM.libbaltcalc as libbaltcalc
from VMSYSTEM.libbaltcalc import btint
import VMSYSTEM.libtextcon as tcon
import time
import sys
import os
import VMSYSTEM.iofuncts as iofuncts


def romdump(fileobj, n0p=0):
	for line in fileobj:
		line=line.replace("\n", "")
		ival0, ival1 = line.split(",")
		trval0=btint(int(ival0))
		trval1=btint(int(ival1))
		pstring=trval0.bttrunk(9) + "  " + trval1.bttrunk(9)
		if n0p==1:
			pstring=pstring.replace("-", "n").replace("+", "p")
		print(pstring)

def romdumpver(fileobj, n0p=0):
	for line in fileobj:
		line=line.replace("\n", "")
		ival0, ival1 = line.split(",")
		trval0=btint(int(ival0))
		trval1=btint(int(ival1))
		pstring=trval0.bttrunk(9) + "  " + trval1.bttrunk(9)
		if n0p==1:
			pstring=pstring.replace("-", "n").replace("+", "p")
		tr0ischar=0
		tr1ischar=0
		for char in tcon.allchars:
			
			if char.dataval==trval0:
				pstring += ("  " + char.bldumpstr)
				tr0ischar=1
		if not tr0ischar:
			pstring += "  ."
		for char in tcon.allchars:
			if char.dataval==trval1:
				pstring += ("  " + char.bldumpstr)
				tr1ischar=1
		
		if not tr1ischar:
			pstring += "  ."
		pstring += str(int(trval0)).rjust(8) + str(int(trval1)).rjust(8)
		print(pstring)


if __name__=="__main__":
	try:
		cmd=sys.argv[1]
	except:
		cmd=None
	try:
		arg=sys.argv[2]
	except:
		arg=None
	if cmd in ["-h", "--help"]:
		print('''SBTCVM Gen2 romdump utility. v1.0.0
-h --help: this help
-v --version: version
-a, --about: about SBTCVM
-d [trom] dump contents of trom to standard output in +0- form. instructions and data colums separated by two spaces. "  "
-r [trom] same as -d, but also prints chars & decimal values
-dnp [trom] same as -d, but using n0p representation.
-rnp [trom] same as -dnp, but also prints chars & decimal values
[trom] (with no options) same as -d''')
	elif cmd in ["-v", "--version"]:
		print("SBTCVM Gen2 romdump utility. v1.0.0\n" + "part of SBTCVM-Gen2-9 v2.1.0.alpha")
	elif cmd in ["-a", "--about"]:
		print('''SBTCVM Gen2-9 romdump utility.
v1.0.0
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
	elif cmd in ["-d"]:
		romdump(iofuncts.loadtrom(arg))
	elif cmd in ["-dnp"]:
		romdump(iofuncts.loadtrom(arg), n0p=1)
	elif cmd in ["-r"]:
		romdumpver(iofuncts.loadtrom(arg))
	elif cmd in ["-rnp"]:
		romdumpver(iofuncts.loadtrom(arg), n0p=1)
	elif cmd == None:
		print("Tip: try romdump.py -h for help.")
	else:
		romdump(iofuncts.loadtrom(cmd))
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
		line=line.replace("/n", "")
		ival0, ival1 = line.split(",")
		trval0=btint(int(ival0))
		trval1=btint(int(ival1))
		pstring=trval0.bttrunk(9) + "  " + trval1.bttrunk(9)
		if n0p==1:
			pstring=pstring.replace("-", "n").replace("+", "p")
		print(pstring)

def romdumpver(fileobj, n0p=0):
	for line in fileobj:
		line=line.replace("/n", "")
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
-d [trom] dump contents of trom to standard output in +0- form. instructions and data colums separated by two spaces. "  "
-r [trom] same as -d, but also prints chars & decimal values
-dnp [trom] same as -d, but using n0p representation.
-rnp [trom] same as -dnp, but also prints chars & decimal values
[trom] (with no options) same as -d''')
	elif cmd in ["-v", "--version"]:
		print("SBTCVM Gen2 romdump utility. v1.0.0")
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
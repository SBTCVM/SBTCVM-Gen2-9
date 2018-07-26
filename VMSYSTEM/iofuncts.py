#!/usr/bin/env python
from . import libbaltcalc
btint=libbaltcalc.btint
import os
import sys

#file io common functions


#trom loader. can also be used for other file types.
VMSYSROMS=os.path.join("VMSYSTEM", "ROMS")
def loadtrom(fname, ext=".trom", exitonfail=1, exitmsg="ERROR: Nonexistant TROM!"):
	for filenameg in [fname, fname+ext.lower(), fname+ext.upper()]:
		if os.path.isfile(filenameg) and filenameg.lower().endswith(ext):
			return(open(filenameg, "r"))
		elif os.path.isfile(os.path.join("ROMS", filenameg)):
			return(open(os.path.join("ROMS", filenameg), "r"))
		elif os.path.isfile(os.path.join("VMUSER", filenameg)):
			return(open(os.path.join("VMUSER", filenameg), "r"))
		elif os.path.isfile(os.path.join("VMSYSTEM", filenameg)):
			return(open(os.path.join("VMSYSTEM", filenameg), "r"))
		elif os.path.isfile(os.path.join(VMSYSROMS, filenameg)):
			return(open(os.path.join(VMSYSROMS, filenameg), "r"))
	if exitonfail:
		sys.exit(exitmsg)
	else:
		return None
#same as loadtrom, but returns path.
def findtrom(fname, ext=".trom", exitonfail=1, exitmsg="ERROR: Nonexistant TROM!"):
	for filenameg in [fname, fname+ext.lower(), fname+ext.upper()]:
		if os.path.isfile(filenameg) and filenameg.lower().endswith(ext):
			return(filenameg)
		elif os.path.isfile(os.path.join("ROMS", filenameg)):
			return(os.path.join("ROMS", filenameg))
		elif os.path.isfile(os.path.join("VMUSER", filenameg)):
			return(os.path.join("VMUSER", filenameg))
		elif os.path.isfile(os.path.join("VMSYSTEM", filenameg)):
			return(os.path.join("VMSYSTEM", filenameg))
		elif os.path.isfile(os.path.join(VMSYSROMS, filenameg)):
			return(os.path.join(VMSYSROMS, filenameg))
	if exitonfail:
		sys.exit(exitmsg)
	else:
		return None
	



#!/usr/bin/env python
from . import libbaltcalc
btint=libbaltcalc.btint
import os
import sys

#file io common functions

#Buffered logging class.
class logit:
	def __init__(self, logname, buffsize=60):
		self.buff=""
		self.fname=logname
		self.logfile=open(os.path.join("CAP", logname), "w")
		self.buffsize=buffsize
	def write(self, data):
		self.buff+=data
		if len(self.buff)>=self.buffsize:
			self.writelog()
	def writelog(self):
		self.logfile.write(self.buff)
		self.buff=""
	def close(self):
		self.writelog()
		self.logfile.close()

VMSYSROMS=os.path.join("VMSYSTEM", "ROMS")

def recur_dir(fnameg):
	for maindir in ["VMSYSTEM", VMSYSROMS, "ROMS", "VMUSER", ]:
		for dirname in os.listdir(maindir):
			dirpath=os.path.join(maindir, dirname)
			if dirname.lower().startswith("r_") and os.path.isdir(dirpath):
				filepath=os.path.join(dirpath, fnameg)
				if os.path.isfile(filepath):
					return filepath
	return None

#trom loader. can also be used for other file types.

def loadtrom(fname, ext=".trom", exitonfail=1, exitmsg="ERROR: Nonexistant TROM!"):
	for filenameg in [fname, fname+ext.lower(), fname+ext.upper()]:
		if os.path.isfile(filenameg) and filenameg.lower().endswith(ext):
			return (open(filenameg, "r"))
		
		elif os.path.isfile(os.path.join("VMSYSTEM", filenameg)):
			return (open(os.path.join("VMSYSTEM", filenameg), "r"))
		elif os.path.isfile(os.path.join(VMSYSROMS, filenameg)):
			return (open(os.path.join(VMSYSROMS, filenameg), "r"))
		elif os.path.isfile(os.path.join("ROMS", filenameg)):
			return (open(os.path.join("ROMS", filenameg), "r"))
		elif os.path.isfile(os.path.join("VMUSER", filenameg)):
			return (open(os.path.join("VMUSER", filenameg), "r"))
		recurret=recur_dir(filenameg)
		if recurret!=None:
			return (open(recurret, "r"))
	if exitonfail:
		sys.exit(exitmsg)
	else:
		return None
#same as loadtrom, but returns path.
def findtrom(fname, ext=".trom", exitonfail=1, exitmsg="ERROR: Nonexistant TROM!"):
	for filenameg in [fname, fname+ext.lower(), fname+ext.upper()]:
		if os.path.isfile(filenameg) and filenameg.lower().endswith(ext):
			return (filenameg)
		
		elif os.path.isfile(os.path.join("VMSYSTEM", filenameg)):
			return (os.path.join("VMSYSTEM", filenameg))
		elif os.path.isfile(os.path.join(VMSYSROMS, filenameg)):
			return (os.path.join(VMSYSROMS, filenameg))
		elif os.path.isfile(os.path.join("ROMS", filenameg)):
			return (os.path.join("ROMS", filenameg))
		elif os.path.isfile(os.path.join("VMUSER", filenameg)):
			return (os.path.join("VMUSER", filenameg))
		recurret=recur_dir(filenameg)
		if recurret!=None:
			return (recurret)
	if exitonfail:
		sys.exit(exitmsg)
	else:
		return None
	



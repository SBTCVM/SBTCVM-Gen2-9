#!/usr/bin/env python
from . import libbaltcalc
btint=libbaltcalc.btint
import os
import sys

#file io common functions

#Buffered logging class. used in high-speed components. i.e. TTY's logging functionality.
class logit:
	def __init__(self, logname, buffsize=60):
		self.buff=""
		self.fname=logname
		self.logfile=open(os.path.join("cap", logname), "w")
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

vmsysroms=os.path.join("vmsystem", "roms")
reservedpaths=["cfg"]

smartpaths=["vmsystem", vmsysroms, "roms", "apps", "demos", "vmuser"]

#handles r_* directories.
def recur_dir(fnameg):
	for maindir in smartpaths:
		for dirname in os.listdir(maindir):
			dirpath=os.path.join(maindir, dirname)
			if dirname.lower().startswith("r_") and os.path.isdir(dirpath):
				filepath=os.path.join(dirpath, fnameg)
				if os.path.isfile(filepath):
					return filepath
	return None

def auto_dir(fnameg, ext):
	#autodir functionality.
	for maindir in smartpaths:
		dirpath=os.path.join(maindir, fnameg)
		if os.path.isdir(dirpath):
			for filex in os.listdir(dirpath):
				if filex.lower().startswith("auto_") and filex.lower().endswith(ext):
					fpath=os.path.join(dirpath, filex)
					if os.path.isfile(fpath):
						return fpath
	return None

#trom loader. also used for other file types.

def loadtrom(fname, ext=".trom", exitonfail=1, exitmsg="ERROR: Nonexistant TROM!", dirauto=0):
	if '+' in fname:
		fname=os.path.join(*fname.split("+"))
	if dirauto:
		dirauret=auto_dir(fname, ext)
		if dirauret!=None:
			return open(dirauret, 'r')
	for filenameg in [fname, fname+ext.lower(), fname+ext.upper()]:
		if os.path.isfile(filenameg) and filenameg.lower().endswith(ext):
			return (open(filenameg, "r"))
		
		elif os.path.isfile(os.path.join("vmsystem", filenameg)):
			return (open(os.path.join("vmsystem", filenameg), "r"))
		elif os.path.isfile(os.path.join(vmsysroms, filenameg)):
			return (open(os.path.join(vmsysroms, filenameg), "r"))
		elif os.path.isfile(os.path.join("roms", filenameg)):
			return (open(os.path.join("roms", filenameg), "r"))
		elif os.path.isfile(os.path.join("apps", filenameg)):
			return (open(os.path.join("apps", filenameg), "r"))
		elif os.path.isfile(os.path.join("demos", filenameg)):
			return (open(os.path.join("demos", filenameg), "r"))
		elif os.path.isfile(os.path.join("vmuser", filenameg)):
			return (open(os.path.join("vmuser", filenameg), "r"))
		recurret=recur_dir(filenameg)
		if recurret!=None:
			return (open(recurret, "r"))
	if exitonfail:
		sys.exit(exitmsg)
	else:
		return None
#same as loadtrom, but returns path. also used for other file types. i.e. source code in compilers.
def findtrom(fname, ext=".trom", exitonfail=1, exitmsg="ERROR: Nonexistant TROM!", dirauto=0):
	if '+' in fname:
		fname=os.path.join(*fname.split("+"))
	if dirauto:
		dirauret=auto_dir(fname, ext)
		if dirauret!=None:
			return dirauret
	for filenameg in [fname, fname+ext.lower(), fname+ext.upper()]:
		if os.path.isfile(filenameg) and filenameg.lower().endswith(ext):
			return (filenameg)
		
		elif os.path.isfile(os.path.join("vmsystem", filenameg)):
			return (os.path.join("vmsystem", filenameg))
		elif os.path.isfile(os.path.join(vmsysroms, filenameg)):
			return (os.path.join(vmsysroms, filenameg))
		elif os.path.isfile(os.path.join("roms", filenameg)):
			return (os.path.join("roms", filenameg))
		elif os.path.isfile(os.path.join("apps", filenameg)):
			return (os.path.join("apps", filenameg))
		elif os.path.isfile(os.path.join("demos", filenameg)):
			return (os.path.join("demos", filenameg))
		elif os.path.isfile(os.path.join("vmuser", filenameg)):
			return (os.path.join("vmuser", filenameg))
		
		recurret=recur_dir(filenameg)
		if recurret!=None:
			return (recurret)
	if exitonfail:
		sys.exit(exitmsg)
	else:
		return None
	



#!/usr/bin/env python
import libbaltcalc
from libbaltcalc import btint
import os
import sys

def loadtrom(filenameg):
	if os.path.isfile(filenameg):
		return(open(filenameg, "r"))
	elif os.path.isfile(os.path.join("ROMS", filenameg)):
		return(open(os.path.join("ROMS", filenameg), "r"))
	elif os.path.isfile(os.path.join("VMUSER", filenameg)):
		return(open(os.path.join("VMUSER", filenameg), "r"))
	elif os.path.isfile(os.path.join("VMSYSTEM", filenameg)):
		return(open(os.path.join("VMSYSTEM", filenameg), "r"))
	elif os.path.isfile(os.path.join(VMSYSROMS, filenameg)):
		return(open(os.path.join(VMSYSROMS, filenameg), "r"))
	else:
		#print ("FATAL ERROR: libtrom: NONEXISTENT TROM! (" + filenameg + ")")
		sys.exit("FATAL ERROR: libtrom: NONEXISTENT TROM! (" + filenameg + ")")


class memory:
	def __init__(self, trom):
		self.trom=trom
		self.INSTDICT={}
		self.DATDICT={}
		linecnt=libbaltcalc.mni(9)
		print "Setting up Virtual RAM system"
		TROMFILE=loadtrom(trom)
		for rmline in TROMFILE:
			rmline=rmline.replace("\n", "")
			self.INSTDICT[linecnt]=btint(rmline[:6])
			self.DATDICT[linecnt]=btint(rmline[6:])
			linecnt += 1
		TROMFILE.close()
		while linecnt<=libbaltcalc.mpi(9):
			self.INSTDICT[linecnt]=btint("000000")
			self.DATDICT[linecnt]=btint("000000000")
			linecnt += 1
		print "Virtual RAM ready: " + str(len(self.DATDICT)) + " data words, \n" + str(len(self.INSTDICT)) + " instruction words"
	#memory read
	def getinst(self, addr):
		return self.INSTDICT[int(addr)]
	def getdata(self, addr):
		return self.DATDICT[int(addr)]
	#memory write
	def setinst(self, addr, value):
		(self.INSTDICT[int(addr)]).changeval(value)
	def setdata(self, addr, value):
		(self.DATDICT[int(addr)]).changeval(value)
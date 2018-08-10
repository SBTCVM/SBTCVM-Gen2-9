#!/usr/bin/env python
from . import libbaltcalc
from . import iofuncts
btint=libbaltcalc.btint
import os
import sys


class memory:
	def __init__(self, trom):
		self.trom=trom
		self.INSTDICT={}
		self.DATDICT={}
		linecnt=libbaltcalc.mni(9)
		print("Setting up Virtual RAM subsystem")
		TROMFILE=iofuncts.loadtrom(trom, dirauto=1)
		for rmline in TROMFILE:
			rmline=rmline.replace("\n", "").split(",")
			self.INSTDICT[linecnt]=btint(int(rmline[0]))
			self.DATDICT[linecnt]=btint(int(rmline[1]))
			linecnt += 1
		TROMFILE.close()
		#pad memory map to max size if not already maxxed.
		while linecnt<=libbaltcalc.mpi(9):
			self.INSTDICT[linecnt]=btint(0)
			self.DATDICT[linecnt]=btint(0)
			linecnt += 1
		print("Virtual RAM ready: " + str(len(self.DATDICT)) + " data words, \n" + str(len(self.INSTDICT)) + " instruction words\n")
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
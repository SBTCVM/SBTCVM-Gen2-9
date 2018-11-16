#!/usr/bin/env python
from . import libbaltcalc
from . import iofuncts
btint=libbaltcalc.btint
from . import libtextcon as tcon
import os
import sys
import random


#various smaller common IOBUS devices. i.e. random number generators.

#standard common device configuration startup.
def factorydevs(iosys):
	#programmable-range random number generators.
	devrandno(iosys, 50)
	devrandno(iosys, 53)
	devrandno(iosys, 56)
	devrandno(iosys, 59)


#random number gen
class devrandno:
	def __init__(self, iosys, baseaddr, defaultrange=9841):
		
		self.randstart=-defaultrange
		self.randend=defaultrange
		
		
		iosys.setwritenotify(baseaddr, self.setrandstart)
		iosys.setwritenotify(baseaddr+1, self.setrandend)
		iosys.setreadoverride(baseaddr+2, self.getrandno)
	def getrandno(self, addr, data):
		if self.randstart>self.randend:
			return btint(random.randint(self.randend, self.randstart))
		else:
			return btint(random.randint(self.randstart, self.randend))
		
	def setrandstart(self, addr, data):
		self.randstart=int(data)
	def setrandend(self, addr, data):
		self.randend=int(data)
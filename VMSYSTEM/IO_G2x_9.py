#!/usr/bin/env python
import libbaltcalc
from libbaltcalc import btint
import os
import sys




class io:
	def __init__(self):
		print "IO subsystem initalizing..."
		addrset=libbaltcalc.mni(9)
		self.IODICT={}
		self.WriteNotifyDict={}
		self.WriteNotifyList=[]
		while addrset<=libbaltcalc.mpi(9):
			self.IODICT[addrset]=btint(0)
			self.WriteNotifyDict[addrset]=None
			addrset+=1
		print "IO initalized: " + str(len(self.IODICT)) + " unique addresses\n"
	#NON-CPU components should use this to get notified of IObus writes at specific addresses.
	#note that functref should be a refrence to a specific function that is to be run, with the form:
	#functref(addr, data)
	def setnotify(self, addr, functref):
		self.WriteNotifyList.extend([int(addr)])
		self.WriteNotifyDict[addr]=functref
	def ioread(self, addr):
		return self.IODICT[addr]
	def iowrite(self, addr, data):
		addrobj=self.IODICT[addr]
		addrobj.changeval(data)
		#if address is registered by a component via setnotify, call the specified function.
		if addr in self.WriteNotifyList:
			functref=self.WriteNotifyDict[addr]
			functref(btint(addr), addrobj)
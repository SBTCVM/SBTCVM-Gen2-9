#!/usr/bin/env python
from . import libbaltcalc
btint=libbaltcalc.btint
import os
import sys




class io:
	def __init__(self, io_id=0):
		print("IO" + str(io_id) + " subsystem initalizing...")
		addrset=libbaltcalc.mni(9)
		self.IODICT={}
		self.WriteNotifyDict={}
		self.WriteNotifyList=[]
		self.ReadNotifyDict={}
		self.ReadNotifyList=[]
		self.ReadOverrideDict={}
		self.ReadOverrideList=[]
		#build IObus memory & Write/Read Notify dictionaries.
		while addrset<=libbaltcalc.mpi(9):
			self.IODICT[addrset]=btint(0)
			self.WriteNotifyDict[addrset]=None
			self.ReadNotifyDict[addrset]=None
			self.ReadOverrideDict[addrset]=None
			addrset+=1
		#print("IO" + str(io_id) + " initalized: " + str(len(self.IODICT)) + " unique addresses\n")
	#NON-CPU components should use this to get notified of IObus writes at specific addresses.
	#note that functref should be a refrence to a specific function that is to be run, with the form:
	#functref(addr, data)
	def setwritenotify(self, addr, functref):
		self.WriteNotifyList.extend([int(addr)])
		self.WriteNotifyDict[addr]=functref
	def setreadnotify(self, addr, functref):
		self.ReadNotifyList.extend([int(addr)])
		self.ReadNotifyDict[addr]=functref
	def setreadoverride(self, addr, functref):
		self.ReadOverrideList.extend([int(addr)])
		self.ReadOverrideDict[addr]=functref
	#ioread and iowrite should only be used by the CPU(s) devices should use deviceread and devicewrite (see below)
	def ioread(self, addr):
		if int(addr) in self.ReadOverrideList:
			#get data at address anyways. (useful for refrence, ect, also needed to keep IO map updated)
			addrobjreal=self.IODICT[int(addr)]
			xfunctref=self.ReadOverrideDict[int(addr)]
			gaddrobj=xfunctref(btint(int(addr)), addrobjreal)
			#update data point.
			addrobjreal.changeval(gaddrobj)
			#print("ioreadoverride")
			
		else:
			gaddrobj=self.IODICT[int(addr)]
		#if address is registered by a component via setreadnotify, call the specified function.
		if addr in self.ReadNotifyList:
			functref=self.ReadNotifyDict[int(addr)]
			functref(btint(int(addr)), gaddrobj)
		return gaddrobj
	def iowrite(self, addr, data):
		addrobj=self.IODICT[int(addr)]
		addrobj.changeval(data)
		#if address is registered by a component via setwritenotify, call the specified function.
		if addr in self.WriteNotifyList:
			functref=self.WriteNotifyDict[int(addr)]
			functref(btint(addr), addrobj)
	#deviceread and devicewrite functions are for IObus Devices, and any non-CPU subsystem
	#that needs to read/write the IObus without triggering the read and write function callbacks.
	def deviceread(self, addr):
		return self.IODICT[addr]
	def devicewrite(self, addr, data):
		addrobj=self.IODICT[addr]
		addrobj.changeval(data)
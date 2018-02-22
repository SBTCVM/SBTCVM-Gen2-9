#!/usr/bin/env python
from . import libbaltcalc
btint=libbaltcalc.btint
import os
import sys




class io:
	def __init__(self):
		print("IO subsystem initalizing...")
		addrset=libbaltcalc.mni(9)
		self.IODICT={}
		self.WriteNotifyDict={}
		self.WriteNotifyList=[]
		self.ReadNotifyDict={}
		self.ReadNotifyList=[]
		#build IObus memory & Write/Read Notify dictionaries.
		while addrset<=libbaltcalc.mpi(9):
			self.IODICT[addrset]=btint(0)
			self.WriteNotifyDict[addrset]=None
			self.ReadNotifyDict[addrset]=None
			addrset+=1
		print("IO initalized: " + str(len(self.IODICT)) + " unique addresses\n")
	#NON-CPU components should use this to get notified of IObus writes at specific addresses.
	#note that functref should be a refrence to a specific function that is to be run, with the form:
	#functref(addr, data)
	def setwritenotify(self, addr, functref):
		self.WriteNotifyList.extend([int(addr)])
		self.WriteNotifyDict[addr]=functref
	def setreadnotify(self, addr, functref):
		self.ReadNotifyList.extend([int(addr)])
		self.ReadNotifyDict[addr]=functref
	#ioread and iowrite should only be used by the CPU(s) devices should use deviceread and devicewrite (see below)
	def ioread(self, addr):
		addrobj=self.IODICT[addr]
		#if address is registered by a component via setreadnotify, call the specified function.
		if addr in self.ReadNotifyList:
			functref=self.ReadNotifyDict[addr]
			functref(btint(addr), addrobj)
		return addrobj
	def iowrite(self, addr, data):
		addrobj=self.IODICT[addr]
		addrobj.changeval(data)
		#if address is registered by a component via setwritenotify, call the specified function.
		if addr in self.WriteNotifyList:
			functref=self.WriteNotifyDict[addr]
			functref(btint(addr), addrobj)
	#deviceread and devicewrite functions are for IObus Devices, and any non-CPU subsystem
	#that needs to read/write the IObus without triggering the read and write function callbacks.
	def deviceread(self, addr):
		return self.IODICT[addr]
	def devicewrite(self, addr, data):
		addrobj=self.IODICT[addr]
		addrobj.changeval(data)
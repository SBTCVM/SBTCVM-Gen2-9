#!/usr/bin/env python
from . import libbaltcalc
from . import iofuncts
btint=libbaltcalc.btint
from . import libtextcon as tcon
import os
import sys
import random


class vdi_filebuff:
	def __init__(self, iosys, cpusys, memsys):
		return
#SBTCVM Balanced Ternary Virtual Disk Interface
#DRAFT. 
class sbtvdi:
	def __init__(self, iosys, cpusys, memsys):
		self.iosys=iosys
		self.cpusys=cpusys
		self.memsys=memsys
		self.cmdbuff=[]
		self.outbuff=[]
		self.status=0
		#CLI IO lines:
		iosys.setwritenotify(100, self.clipipe_input)
		iosys.setwritenotify(102, self.clireset)
		iosys.setreadoverride(101, self.clipipe_output)
		iosys.setreadoverride(102, self.clistatus)
		self.prm=0
	def outstr(self, outx):
		for x in outx:
			self.outbuff.append(tcon.strtodat[x])
	def clipipe_input(self, addr, data):
		if data==1:
			if not self.prm:
				self.outbuff.append(1)
			self.cmdparse(tcon.datlisttostr(self.cmdbuff))
			self.cmdbuff=[]
		elif data==2:
			if len(self.cmdbuff)>0:
				self.cmdbuff.pop(-1)
				if not self.prm:
					self.outbuff.append(2)
		else:
			if data.intval in tcon.dattostr:
				self.cmdbuff.append(data.intval)
				if not self.prm:
					self.outbuff.append(data.intval)
	def clipipe_output(self, addr, data):
		if len(self.outbuff)>0:
			return btint(self.outbuff.pop(0))
		else:
			return btint(0)
	def clistatus(self, addr, data):
		return btint(self.status)
	#should be called by application before using shell.
	def clireset(self, addr, data):
		if data==1:
			self.prm=1
		else:
			self.prm=0
		self.cmdbuff=[]
		self.outbuff=[]
		if not self.prm==1:
			self.outstr("\nSBTVDI Serial Console: rev: 1.1\n>")
		self.status=0
	def cmdparse(self, cmdstr):
		cmdlist=cmdstr.split(" ", 1)
		cmd=cmdlist[0]
		if cmd=='return' and self.prm==0:
			self.status=1
		elif cmd=='quit' and self.prm==0:
			self.status=2
		elif cmd=='help':
			if self.prm==1:
				self.outstr('''SBTVDI Serial Console (mode 1) commands:
help   : this text
''')
			else:
				self.outstr('''SBTVDI Serial Console (mode 0) commands:
help   : this text
return : request to return to application
quit   : request to quit
''')
		else:
			self.outstr("ERROR: '" + cmd + "' is not valid/available in this mode!\n")
		
		if self.prm==0:
			self.outstr('>')
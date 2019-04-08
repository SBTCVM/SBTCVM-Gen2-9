#!/usr/bin/env python
from . import libbaltcalc
from . import iofuncts
btint=libbaltcalc.btint
from . import libtextcon as tcon
import os
import sys
import random
import vmsystem.tdisk1lib as td1

class vdi_filebuff:
	def __init__(self, iosys, cpusys, memsys, offset, disks):
		self.iosys=iosys
		self.cpusys=cpusys
		self.memsys=memsys
		self.offset=offset
		self.filename=""
		self.openfile=None
		self.disks=disks
		self.diskindex=0
		self.fileseek=0
		self.fileopen=0
		self.selecteddisk=self.disks[self.diskindex]
		return
	def write_char(self, addr, data):#w
		self.filename=self.filename+tcon.dattostr[int(data)]
	def filename_reset(self, addr, data):#w
		self.filename=""
	def filename_exists(self, addr, data):#r
		return btint((self.filename in self.selecteddisk.filedict))
	def file_close(self, addr, data):#w
		self.openfile=None
		self.fileopen=0
	def file_open(self, addr, data):#r
		if self.filename in self.selecteddisk.filedict:
			self.openfile=self.selecteddisk.filedict[self.filename]
			self.fileopen=1
			return btint(1)
		return btint(0)
	def is_open(self, addr, data):#r
		return btint(self.fileopen)
	def disk_set(self, addr, data):#w
		data=int(data)
		if data in disks:
			self.diskindex=data
			self.selecteddisk=self.disks[self.diskindex]
	def disk_get(self, addr, data):#r
		return btint(self.diskindex)
	def seek_set(self, addr, data):#r
		if self.openfile==None:
			return btint(1)
		newseek=data+9841
		if newseek+1>len(self.openfile):
			return btint(1)
		self.fileseek=newseek
		return btint(0)
	def seek_get(self, addr, data):#r
		return btint(self.fileseek)
	def seek_inc(self, addr, data):#r
		if self.openfile==None:
			return btint(1)
		newseek=self.fileseek+1
		if newseek+1>len(self.openfile):
			return btint(1)
		self.fileseek=newseek
		return btint(0)
	def seek_dec(self, addr, data):#r
		if self.openfile==None:
			return btint(1)
		newseek=self.fileseek-1
		if newseek<0:
			return btint(1)
		self.fileseek=newseek
		return btint(0)
	def read_inst(self, addr, data):#r
		if self.openfile!=None:
			return self.openfile[self.seek][0]
	def read_data(self, addr, data):#r
		if self.openfile!=None:
			return self.openfile[self.seek][1]
	def write_data(self, addr, data):#w
		if self.openfile!=None:
			self.openfile[self.seek][1].changeval(data)
	def write_inst(self, addr, data):#w
		if self.openfile!=None:
			self.openfile[self.seek][0].changeval(data)
	def resetload(self, addr, data):#w
		#TODO: resetload sbtvdi callback & cpu soft-reset
		return
	
#SBTCVM Balanced Ternary Virtual Disk Interface
#DRAFT. 
class sbtvdi:
	def __init__(self, iosys, cpusys, memsys, diska=None, diskb=None, bootfromdisk=0):
		self.iosys=iosys
		self.cpusys=cpusys
		self.memsys=memsys
		self.cmdbuff=[]
		self.outbuff=[]
		self.status=0
		self.disks={0: diska, 1: diskb, 2: td1.ramdisk()}
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
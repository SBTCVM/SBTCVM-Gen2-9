#!/usr/bin/env python
from . import libbaltcalc
from . import iofuncts
btint=libbaltcalc.btint
from . import libtextcon as tcon
import os
import sys
import random
import vmsystem.tdisk1lib as td1


### NEW SBTVDI PLAN
# as much operations are handled via VDI Serial comamnds ONLY, as reasonable.
# Some commands will have IO-register inputs and outputs. (fileIO for example)
# resetload is now a VDI command that accepts: rstload [diskindex] [filename]
# filebuffers will assign/report filenames and such via VDI Serial.

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
	##TODO: file IO and seek (old code was too off-target, didn't meet up with the tdisk1lib API that well.)
	#def resetload(self, addr, data):#w
		##TODO: memory reset & load from VDI disk file data.
		#cpusys.softreset()
		
		#return
	
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
		#program mode flag. if 0: run in CLI mode. if 1: run in program mode.
		#program mode: does not mirror user input, and should be used
		#    for using VDI commands directly within program code.
		#CLI mode    : mirrors user input, intened to be used directly by user.
		self.prm=0
		#todo: disk bootup code:
		#    - try to boot from disk A then disk B
		#    - (obviously) ramdisk is not valid.
		#    - SBTVDI should try "resetload" (aka boot from) "boot.txe"
		#    - if boot.txe does not exist on the disk, then the disk is 
		#        considered a "non-system disk"
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
		#print(self.status)
		return btint(self.status)
		
	#should be called by application before using shell.
	def clireset(self, addr, data):
		#print("huh")
		if data==1:
			self.prm=1
		else:
			self.prm=0
		self.cmdbuff=[]
		self.outbuff=[]
		self.status=0
		if not self.prm==1:
			self.outstr("\nSBTVDI Serial Console: rev: 1.1\n>")
		self.status=0
	def cmdparse(self, cmdstr):
		cmdlist=cmdstr.split(" ", 1)
		cmdlist_as=cmdstr.split(" ")
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
			self.outstr('''dmnt0 [disk image]: Mount SBTVDI disk image to drive index 0
dmnt1 [disk image]: Mount SBTVDI disk image to drive index 1
rstld [drive index] [filename] : load and run full-memory prorgams from disk.
''')
		elif cmd=="dmnt0" or cmd=="dmnt1":
			if cmd=="dmnt0":
				mntindex=0
				stoffst=0
			else:
				mntindex=1
				stoffst=-20
			if not len(cmdlist_as)>=2:
				self.outstr("ERROR: specify 'dmnt* [filename]'!\n")
				self.status=-20+stoffst
			else:
				fname=iofuncts.findtrom(cmdlist_as[1], ext=".tdsk1", exitonfail=0, dirauto=1)
				#print(fname)
				if fname==None:
					self.outstr("ERROR: disk image '" + cmdlist_as[1] + "' not found.\n")
					#print("ARGH")
					self.status=-21+stoffst
					return
				else:
					retval=td1.loaddisk(fname, readonly=0)
					if isinstance(retval, str):
						self.status=-22+stoffst
						self.outstr("TDSK1 Fault: '" + retval + "'\n")
					else:
						if self.disks[mntindex]!=None:
							if self.disks[mntindex].ro==0 and self.disks[mntindex].rd==0:
								td1.savedisk(self.disks[mntindex])
								del self.disks[mntindex]
						self.disks[mntindex]=retval
								
		elif cmd=="rstld":
			if not len(cmdlist_as)>=3:
				self.outstr("ERROR: specify 'rstld [diskid] [filename]'!\n")
				self.status=-2
			else:
				try:
					if int(cmdlist_as[1]) in self.disks or int(cmdlist_as[1]) == -1:
						self.resetload_getfile(int(cmdlist_as[1]), cmdlist_as[2])
				except ValueError:
					self.outstr("ERROR: Invalid Integer in disk id! '" + cmdlist_as[1] + "'\n")
					self.status=-1
		else:
			self.outstr("ERROR: '" + cmd + "' is not valid/available in this mode!\n")
		
		if self.prm==0:
			self.outstr('>')
	def resetload_getfile(self, diskid, filename):
		for did in self.disks:
			if diskid==did or diskid==-1:
				if self.disks[did]==None:
					if diskid!=-1:
						self.outstr("ERROR:  drive index '" + str(diskid) + "' Not ready/no disk inserted.\n")
						self.status=-5
						return
				else:
					if filename in self.disks[did].files:
						self.resetload_restart(self.disks[did].files[filename])
						return
		if diskid not in self.disks and diskid!=-1:
			self.outstr("ERROR:  drive index '" + str(diskid) + "' does not exist.\n")
			self.status=-4
			return
		self.outstr("ERROR: '" + filename + "' Was not found!\n")
		self.status=-3
	def resetload_restart(self, filelisting):
		#restart CPU
		self.cpusys.softreset()
		#reset CLI io buffers and params
		self.clireset(None, 0)
		#call special memory system resetload helper. (blanks RAM and loads file into it)
		self.memsys.resetload_helper(filelisting)
		

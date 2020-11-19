#!/usr/bin/env python

from . import MEM_G2x_9
from . import CPU_G2x_9
from . import IO_G2x_9
from . import libbaltcalc
btint=libbaltcalc.btint

from threading import Thread

import time
def cocpu_setup(cpusys2, iosys1, iosys2, memsys2, targtime, targspeed):
	cocpuinst=cocpu(iosys1, iosys2, memsys2, cpusys2)
	
	dispthr=Thread(target = cocpuinst.cocpu_process, args = [targtime*2, targspeed/2.0])
	dispthr.daemon=True
	dispthr.start()
	return cocpuinst
	


shutdown=0


class io_pipe:
	def __init__(self, sourceIO, sourceAdr, destIO, destAdr):
		self.bufferS=[]
		self.bufferD=[]
		sIO=sourceIO
		dIO=destIO
		sA=sourceAdr
		dA=destAdr
		
		sIO.setreadoverride(sA, self.sourceRead)
		
		dIO.setreadoverride(dA, self.destRead)
		sIO.setwritenotify(sA, self.sourceWrite)
		dIO.setwritenotify(dA, self.destWrite)
	def sourceWrite(self, addr, data):
		self.bufferS.append(int(data))
	def destWrite(self, addr, data):
		
		self.bufferD.append(int(data))
	def sourceRead(self, addr, data):
		try:
			return btint(self.bufferD.pop(0))
		except IndexError:
			return btint(0)
	def destRead(self, addr, data):
		try:
			return btint(self.bufferS.pop(0))
		except IndexError:
			return btint(0)

class cocpu:
	def __init__(self, iosys1, iosys2, memsys2, cpusys2):
		
		self.clcnt=0.0
		self.starttime=None
		self.cocpu_hlt=1
		self.powoff_flg=0
		self.iosys1=iosys1
		self.iosys2=iosys2
		self.memsys=memsys2
		self.cpusys=cpusys2
		self.shutdown=0
		self.progrun=1
		self.pipe0=io_pipe(self.iosys1, 1100, self.iosys2, 1100)
		self.pipe0=io_pipe(self.iosys1, 1101, self.iosys2, 1101)
		self.pipe0=io_pipe(self.iosys1, 1102, self.iosys2, 1102)
		self.pipe0=io_pipe(self.iosys1, 1103, self.iosys2, 1103)
		iosys1.setreadnotify(1001, self.io_reset)
		iosys1.setwritenotify(1000, self.io_cocpu_state)
		self.postout1=None
		self.postout2=None
		self.postout3=None
		iosys1.setreadoverride(1000, self.io_cocpu_getstate)
		iosys2.setreadnotify(1001, self.io_reset)
		iosys2.setwritenotify(1000, self.io_cocpu_state)
		
		iosys2.setreadoverride(1000, self.io_cocpu_getstate)
		self.ishalted=1
	def io_reset(self, addr, data):
		self.cocpu_hlt=2
		self.cpusys.softreset(cocpu=1)
	def io_cocpu_getstate(self, addr, data):
		if self.cocpu_hlt==2:
			return btint(0)
		return btint(self.cocpu_hlt)
	def io_cocpu_state(self, addr, data):
		data=int(data)
		if data==1 and self.cocpu_hlt==0:
			self.cocpu_hlt=1
			
		elif data==0 and self.cocpu_hlt==1:
			self.cocpu_hlt=2
	
	def VDI_rstld(self, filelisting):
		#if the cocpu is running, halt it, wait for halt confirm,
		#	do memory load and CPU reset, then resume CPU.
		#	(prevents CoCPU from running after reset, and before memory is changed)
		if not self.cocpu_hlt:
			self.cocpu_hlt=1
			while not self.ishalted:
				time.sleep(0.01)
			self.cpusys.softreset(cocpu=1)
			self.memsys.resetload_helper(filelisting)
			self.cocpu_hlt=2
		#if the cocpu is already halted, leave it like that.
		else:
			self.cpusys.softreset(cocpu=1)
			self.memsys.resetload_helper(filelisting)
	def powoff(self):
		self.shutdown=1
		while self.progrun==1:
			time.sleep(0.01)
			#print(self.progrun)
			#print(self.progrun)
	def cocpu_process(self, targtime, targspeed):
		while self.progrun:
			if self.cocpu_hlt==1:
				time.sleep(0.01)
				self.ishalted=1
				if self.shutdown==1:
					print("COCPU Was not running.")
					self.progrun=0
					break
			elif self.cocpu_hlt==2:
				self.clcnt=0.0
				self.starttime=time.time()
				self.cocpu_hlt=0
				self.ishalted=0
				if self.shutdown==1:
					print("COCPU Was not running.")
					self.progrun=0
					break
			else:
				#CPU Parse
				retval=self.cpusys.cycle()
				#increment clock tick.
				self.clcnt+=1
				#project when the next cycle should start, then subtract current time.
				xtime=(self.starttime + (self.clcnt - 1.0) * targtime) - time.time()
				#sleep for remaining time (xtime) if it is above 0
				if xtime>0.0:
					time.sleep(xtime)
				#exit code:
				if retval!=None or self.shutdown==1:
					if retval!=None:
						
						self.postout1=("COCPU VMSYSHALT " + str(retval[1]) + ": " + retval[2])
					else:
						self.postout1=None
					self.postout2=("COCPU Approx. Speed: '" + str((float(self.clcnt)/(time.time()-self.starttime))/1000) + "' KHz")
					self.postout3=("COCPU Target Speed : '" + str(targspeed) + "' Khz")
					
					self.cocpu_hlt=1
					self.progrun=0
					break
	
	def printstats(self):
		if self.postout1!=None:
			print(self.postout1)
		
		if self.postout2!=None:
			print(self.postout2)
		
		if self.postout3!=None:
			print(self.postout3)
	
#!/usr/bin/env python
from . import libbaltcalc
btint=libbaltcalc.btint


#SBTCVM Generation 2 CPU core: G2x_9_r1


class cpu:
	def __init__(self, memorysystem, iosystem):
		self.memsys=memorysystem
		self.iosys=iosystem
		self.designation="SBTCVM_G2x_9_r1"
		print("SBTCVM Generation 2x 9-trit CPU core Initializing...\nCPU Designation: " + self.designation + "\n")
		self.execpoint=btint(libbaltcalc.mni(9))
		self.reg1=btint(0)
		self.reg2=btint(0)
		#memory pointers
		
		#address of memory pointer
		self.mempoint1=btint(libbaltcalc.mni(9))
		#column position: data=0 Inst=1
		self.mempoint2_di=0
		#address of memory pointer
		self.mempoint2=btint(libbaltcalc.mni(9))
		#column position: data=0 Inst=1
		self.mempoint2_di=0
		#address of memory pointer
		self.mempoint3=btint(libbaltcalc.mni(9))
		#column position: data=0 Inst=1
		self.mempoint3_di=0
		self.fop1=btint(0)
		self.fop2=btint(0)
		self.fop3=btint(0)
		
		self.dataval=btint(0)
		self.instval=btint(0)
		self.intercaught={}
		self.intstack=[]
		
	def cycle(self):
		if self.execpoint.intval>9841:
			if self.exception("Exec Pointer Overrun", -3):
				return 1, -3, "Exec Pointer Overrun"
		#self.instval.changeval(self.memsys.getinst(self.execpoint))
		#self.dataval.changeval(self.memsys.getdata(self.execpoint))
		self.instval.intval=self.memsys.getinst(self.execpoint).intval
		self.dataval.intval=self.memsys.getdata(self.execpoint).intval
		#print(self.instval.intval)
		#print(self.dataval.intval)
		#print(self.reg1.intval)
		#print(self.reg2.intval)
		if self.instval.intval == 0:
			pass
		#setreg1
		elif self.instval.intval == -9841:
			self.reg1.changeval(self.dataval.intval)
			#print("setreg1")
			#print(self.reg1)
		#setreg2
		elif self.instval.intval == -9840:
			self.reg2.changeval(self.dataval.intval)
		#copy reg2 to reg1
		elif self.instval.intval == -9839:
			self.reg1.changeval(self.reg2.intval)
		#copy reg1 to reg2
		elif self.instval.intval == -9838:
			self.reg2.changeval(self.reg1.intval)
		#swap reg1 and reg2
		elif self.instval.intval == -9837:
			tmpval=self.reg1.intval
			self.reg1.changeval(self.reg2.intval)
			self.reg2.changeval(tmpval)
		#invert1
		elif self.instval.intval == -9836:
			self.reg1.changeval( - self.reg1.intval)
		#invert2
		elif self.instval.intval == -9835:
			self.reg2.changeval( - self.reg2.intval)
		#ALU
		#add
		elif self.instval.intval == -9800:
			self.reg1.changeval(self.reg1.intval+self.reg2.intval)
			self.pointeroll1()
		elif self.instval.intval == -9799:
			self.reg2.changeval(self.reg1.intval+self.reg2.intval)
			self.pointeroll2()
		elif self.instval.intval == -9798:
			self.reg1.changeval(self.dataval.intval+self.reg1.intval)
			self.pointeroll1()
		elif self.instval.intval == -9797:
			self.reg2.changeval(self.dataval.intval+self.reg2.intval)
			self.pointeroll2()
		#sub
		elif self.instval == -9796:
			self.reg1.changeval(self.reg1.intval-self.reg2.intval)
			self.pointeroll1()
		elif self.instval == -9795:
			self.reg2.changeval(self.reg1.intval-self.reg2.intval)
			self.pointeroll2()
		elif self.instval == -9794:
			self.reg1.changeval(self.reg1.intval-self.dataval.intval)
			self.pointeroll1()
		elif self.instval.intval == -9793:
			self.reg2.changeval(self.reg2.intval-self.dataval.intval)
			self.pointeroll2()
		#mul
		elif self.instval.intval == -9792:
			self.reg1.changeval(self.reg1.intval*self.reg2.intval)
			self.pointeroll1()
		elif self.instval.intval == -9791:
			self.reg2.changeval(self.reg1.intval*self.reg2.intval)
			self.pointeroll2()
		elif self.instval.intval == -9790:
			self.reg1.changeval(self.reg1.intval*self.dataval.intval)
			self.pointeroll1()
		elif self.instval.intval == -9789:
			self.reg2.changeval(self.reg2.intval*self.dataval.intval)
			self.pointeroll2()
		#division
		elif self.instval.intval == -9788:
			try:
				self.reg1.changeval(self.reg1.intval//self.reg2.intval)
				self.pointeroll1()
			except ZeroDivisionError:
				if self.exception("Zero Division.", -2):
					return 1, -2, "Zero Division."
				else:
					return None
				
		elif self.instval.intval == -9787:
			try:
				self.reg2.changeval(self.reg1.intval//self.reg2.intval)
				self.pointeroll2()
			except ZeroDivisionError:
				if self.exception("Zero Division.", -2):
					return 1, -2, "Zero Division."
				else:
					return None
		elif self.instval.intval == -9786:
			try:
				self.reg1.changeval(self.reg1.intval//self.dataval.intval)
				self.pointeroll1()
			except ZeroDivisionError:
				if self.exception("Zero Division.", -2):
					return 1, -2, "Zero Division."
				else:
					return None
		elif self.instval.intval == -9785:
			try:
				self.reg2.changeval(self.reg2.intval//self.dataval.intval)
				self.pointeroll2()
			except ZeroDivisionError:
				if self.exception("Zero Division.", -2):
					return 1, -2, "Zero Division."
				else:
					return None
		#  ---gotos---:
		
		#goto:
		elif self.instval.intval == -9600:
			self.goto(self.dataval.intval)
			return None
		#goto if equal
		elif self.instval.intval == -9599:
			if self.reg1==self.reg2:
				self.goto(self.dataval.intval)
				return None
		#goto if less
		elif self.instval.intval == -9598:
			if self.reg1<self.reg2:
				self.goto(self.dataval.intval)
				return None
		#goto if more
		elif self.instval.intval == -9597:
			if self.reg1>self.reg2:
				self.goto(self.dataval.intval)
				return None
		#goto reg1
		elif self.instval.intval == -9596:
			self.goto(self.reg1.intval)
			return None
		#goto reg2
		elif self.instval.intval == -9595:
			self.goto(self.reg2.intval)
			return None
		
		
		
		#--memory read --
		#dataread1:
		elif self.instval.intval == -9500:
			self.reg1.changeval(self.memsys.getdata(self.dataval))
		#dataread2:
		elif self.instval.intval == -9499:
			self.reg2.changeval(self.memsys.getdata(self.dataval))
		#instread1
		elif self.instval.intval == -9498:
			self.reg1.changeval(self.memsys.getinst(self.dataval))
		#instread2:
		elif self.instval.intval == -9497:
			self.reg2.changeval(self.memsys.getinst(self.dataval))
		
		#--Memory write --
		#datawrite1
		elif self.instval.intval == -9496:
			self.memsys.setdata(self.dataval, self.reg1)
		#datawrite2
		elif self.instval.intval == -9495:
			self.memsys.setdata(self.dataval, self.reg2)
		#instwrite1
		elif self.instval.intval == -9494:
			self.memsys.setinst(self.dataval, self.reg1)
		#instwrite2
		elif self.instval.intval == -9493:
			self.memsys.setinst(self.dataval, self.reg2)
		
		#--IO write --
		#iowrite1
		elif self.instval.intval == -9492:
			self.iosys.iowrite(self.dataval, self.reg1.intval)
		#iowrite2
		elif self.instval.intval == -9491:
			self.iosys.iowrite(self.dataval, self.reg2.intval)
		
		#--IO read --
		#ioread1
		elif self.instval.intval == -9490:
			self.reg1.changeval(self.iosys.ioread(self.dataval.intval))
		#ioread2
		elif self.instval.intval == -9489:
			self.reg2.changeval(self.iosys.ioread(self.dataval.intval))
		
		#--fast output ports--
		#fopwri1
		elif self.instval.intval == -9460:
			self.iosys.iowrite(self.fop1, self.dataval)
		#fopset1
		elif self.instval.intval == -9459:
			self.fop1.changeval(self.dataval.intval)
		#fopwri2
		elif self.instval.intval == -9458:
			self.iosys.iowrite(self.fop2, self.dataval)
		#fopset2
		elif self.instval.intval == -9457:
			self.fop2.changeval(self.dataval.intval)
		#fopwri3
		elif self.instval.intval == -9456:
			self.iosys.iowrite(self.fop3, self.dataval)
		#fopset3
		elif self.instval.intval == -9455:
			self.fop3.changeval(self.dataval.intval)
		
		#soft stop:
		elif self.instval.intval == -9000:
			if self.exception("soft stop.", -1, cancatch=0):
				return 1, -1, "soft stop."
		self.execpoint.intval+=1
		return None
	#pointer rollover code.
	def pointeroll1(self):
		if self.reg1.intval<-9841:
			while self.reg1.intval<-9841:
				self.reg1-=-9841
		elif self.reg1.intval>9841:
			while self.reg1.intval>9841:
				self.reg1-=9841
		return
	def pointeroll2(self):
		if self.reg2.intval<-9841:
			while self.reg2.intval<-9841:
				self.reg2-=-9841
		elif self.reg2.intval>9841:
			while self.reg2.intval>9841:
				self.reg2-=9841
		return
	
	
	
	#goto function
	def goto(self, address):
		self.execpoint.intval=address
		return
	#stub. fill out with needed code once exception/interrupt system is active.
	#ensure uncatchable exceptions set the cancatch attribute to zero.
	def exception(self, status, exid, cancatch=1):
		
		return 1
		
		
		
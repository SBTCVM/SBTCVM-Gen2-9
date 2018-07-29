#!/usr/bin/env python
from . import libbaltcalc
btint=libbaltcalc.btint


#SBTCVM Generation 2 CPU core: G2x_9_r1


class cpu:
	def __init__(self, memorysystem, iosystem):
		self.memsys=memorysystem
		self.designation="SBTCVM_G2x_9_r1"
		print("SBTCVM Generation 2x 9-trit CPU core Initializing...\nCPU Designation: " + self.designation + "\n")
		self.execpoint=btint(libbaltcalc.mni(9))
		self.reg1=btint(0)
		self.reg2=btint(0)
		self.mempoint=btint(libbaltcalc.mni(9))
		self.dataval=btint(0)
		self.instval=btint(0)
	def cycle(self):
		if self.execpoint>9841:
			if self.exception("Exec Pointer Overrun", -3):
				return 1, -3, "Exec Pointer Overrun"
		self.instval.changeval(self.memsys.getinst(self.execpoint))
		self.dataval.changeval(self.memsys.getdata(self.execpoint))
		#print(self.instval.intval)
		#print(self.dataval.intval)
		#print(self.reg1.intval)
		#print(self.reg2.intval)
		#setreg1
		if self.instval == -9841:
			self.reg1.changeval(self.dataval.intval)
			#print("setreg1")
			#print(self.reg1)
		#setreg2
		elif self.instval == -9840:
			self.reg2.changeval(self.dataval.intval)
		#copy reg2 to reg1
		elif self.instval == -9839:
			self.reg1.changeval(self.reg2.intval)
		#copy reg1 to reg2
		elif self.instval == -9838:
			self.reg2.changeval(self.reg1.intval)
		#swap reg1 and reg2
		elif self.instval == -9837:
			tmpval=self.reg1.intval
			self.reg1.changeval(self.reg2.intval)
			self.reg2.changeval(tmpval)
		#ALU
		#add
		elif self.instval == -9800:
			self.reg1.changeval(self.reg1.intval+self.reg2.intval)
			self.pointeroll1()
		elif self.instval == -9799:
			self.reg2.changeval(self.reg1.intval+self.reg2.intval)
			self.pointeroll2()
		elif self.instval == -9798:
			self.reg1.changeval(self.dataval.intval+self.reg1.intval)
			self.pointeroll1()
		elif self.instval == -9797:
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
		elif self.instval == -9793:
			self.reg2.changeval(self.reg2.intval-self.dataval.intval)
			self.pointeroll2()
		#mul
		elif self.instval == -9792:
			self.reg1.changeval(self.reg1.intval*self.reg2.intval)
			self.pointeroll1()
		elif self.instval == -9791:
			self.reg2.changeval(self.reg1.intval*self.reg2.intval)
			self.pointeroll2()
		elif self.instval == -9790:
			self.reg1.changeval(self.reg1.intval*self.dataval.intval)
			self.pointeroll1()
		elif self.instval == -9789:
			self.reg2.changeval(self.reg2.intval*self.dataval.intval)
			self.pointeroll2()
		#division
		elif self.instval == -9788:
			try:
				self.reg1.changeval(self.reg1.intval//self.reg2.intval)
				self.pointeroll1()
			except ZeroDivisionError:
				if self.exception("Zero Division.", -2):
					return 1, -2, "Zero Division."
				else:
					return None
				
		elif self.instval == -9787:
			try:
				self.reg2.changeval(self.reg1.intval//self.reg2.intval)
				self.pointeroll2()
			except ZeroDivisionError:
				if self.exception("Zero Division.", -2):
					return 1, -2, "Zero Division."
				else:
					return None
		elif self.instval == -9786:
			try:
				self.reg1.changeval(self.reg1.intval//self.dataval.intval)
				self.pointeroll1()
			except ZeroDivisionError:
				if self.exception("Zero Division.", -2):
					return 1, -2, "Zero Division."
				else:
					return None
		elif self.instval == -9785:
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
		elif self.instval == -9600:
			self.goto(self.dataval.intval)
			return None
		#goto if equal
		elif self.instval == -9599:
			if self.reg1==self.reg2:
				self.goto(self.dataval.intval)
				return None
		#goto if less
		elif self.instval == -9598:
			if self.reg1<self.reg2:
				self.goto(self.dataval.intval)
				return None
		#goto if more
		elif self.instval == -9597:
			if self.reg1>self.reg2:
				self.goto(self.dataval.intval)
				return None
		#goto reg1
		elif self.instval == -9596:
			self.goto(self.reg1.intval)
			return None
		#goto reg2
		elif self.instval == -9595:
			self.goto(self.reg2.intval)
			return None
		
		#soft stop:
		elif self.instval == -9000:
			if self.exception("soft stop.", -1):
				return 1, -1, "soft stop."
		self.execpoint+=1
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
		self.execpoint.changeval(address)
		return
	#stub. fill out with needed code once exception/interrupt system is active.
	def exception(self, status, exid):
		
		return 1
		
		
		
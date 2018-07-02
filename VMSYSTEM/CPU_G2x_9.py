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
		self.instval.changeval(self.memsys.getinst(self.execpoint))
		self.dataval.changeval(self.memsys.getdata(self.execpoint))
		print(self.instval)
		#setreg1
		if self.instval == -9841:
			self.reg1.changeval(self.dataval.intval)
			print("setreg1")
			print(self.reg1)
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
		#soft stop:
		elif self.instval == -9000:
			if self.exception("soft stop.", -1):
				return 1, -1, "soft stop."
		self.execpoint+=1
		return None
	#stub. fill out with needed code once exception/interrupt system is active.
	def exception(self, status, exid):
		print("VMSYSHALT " + str(exid) + ": " + status)
		return 1
		
		
		
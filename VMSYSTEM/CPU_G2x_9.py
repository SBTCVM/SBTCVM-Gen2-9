#!/usr/bin/env python
import libbaltcalc
from libbaltcalc import btint


#SBTCVM Generation 2 CPU core: G2x_9_r1


class cpu:
	def __init__(self, memorysystem, iosystem):
		self.memsys=memorysystem
		self.designation="SBTCVM_G2x_9_r1"
		print "SBTCVM Generation 2x 9-trit CPU core Initalizing...\nCPU Designation: " + self.designation + "\n"
		self.execpoint=btint(libbaltcalc.mni(9))
		self.reg1=btint(0)
		self.reg2=btint(0)
		self.mempoint=btint(libbaltcalc.mni(9))
	def process(self):
		self.instval=self.memsys.getinst(self.execpoint)
		self.dataval=self.memsys.getdata(self.execpoint)
		return
		
		
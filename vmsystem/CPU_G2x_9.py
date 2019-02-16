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
		self.stack1=[]
		self.stack2=[]
		self.stack3=[]
		self.stack4=[]
		self.stack5=[]
		self.stack6=[]
		self.exintreturns=[]
		self.exints=[]
		self.normintreturns=[]
		self.normints=[]
		self.exceptcode=0
		self.exceptflg=0
		self.critfault=None
	def cycle(self):
		if self.execpoint.intval>9841:
			if self.exception("Exec Pointer Overrun", -3, cancatch=0):
				return 1, -3, "Exec Pointer Overrun"
		self.instval.intval=self.memsys.getinst(self.execpoint).intval
		self.dataval.intval=self.memsys.getdata(self.execpoint).intval
		##EXCEPTION SYSTEM
		if self.critfault!=None:
			return 1, self.critfault[0], self.critfault[1]
		elif self.exceptflg:
			self.exceptflg=0
			exid, status = self.exints.pop(0)
			if self.instval.intval!=100 and self.instval.intval!=101:
				return 1, exid, status
			elif self.instval.intval==101:
				self.exceptcode=0
			elif self.execpoint.intval==9841:
				if self.exception("Exec Pointer Overrun", -3, 0):
					return 1, -3, "Exec Pointer Overrun"
			else:
				self.execpoint.intval+=1
				self.normintreturns.insert(0, [self.reg1.intval, self.reg2.intval, self.execpoint.intval, self.exceptcode])
				self.execpoint.intval=self.dataval.intval
				self.instval.intval=self.memsys.getinst(self.execpoint).intval
				self.dataval.intval=self.memsys.getdata(self.execpoint).intval
				
				
			
		#opcode parser
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
		#abs1
		elif self.instval.intval == -9834:
			self.reg1.changeval(abs(self.reg1.intval))
		#abs2
		elif self.instval.intval == -9833:
			self.reg2.changeval(abs(self.reg2.intval))
		#nabs1
		elif self.instval.intval == -9832:
			self.reg1.changeval( - abs(self.reg1.intval))
		#nabs2
		elif self.instval.intval == -9831:
			self.reg2.changeval( - abs(self.reg2.intval))
		
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
				self.reg1.intval=0
				if self.exception("Zero Division.", -2, cancatch=1):
					return 1, -2, "Zero Division."
				
		elif self.instval.intval == -9787:
			try:
				self.reg2.changeval(self.reg1.intval//self.reg2.intval)
				self.pointeroll2()
			except ZeroDivisionError:
				self.reg2.intval=0
				if self.exception("Zero Division.", -2, cancatch=1):
					return 1, -2, "Zero Division."
		elif self.instval.intval == -9786:
			try:
				self.reg1.changeval(self.reg1.intval//self.dataval.intval)
				self.pointeroll1()
			except ZeroDivisionError:
				self.reg1.intval=0
				if self.exception("Zero Division.", -2, cancatch=1):
					return 1, -2, "Zero Division."
		elif self.instval.intval == -9785:
			try:
				self.reg2.changeval(self.reg2.intval//self.dataval.intval)
				self.pointeroll2()
			except ZeroDivisionError:
				self.reg2.intval=0
				if self.exception("Zero Division.", -2, cancatch=1):
					return 1, -2, "Zero Division."
		# special remainder-quotient division
		#divmod
		elif self.instval.intval == -9784:
			try:
				self.reg2.intval, self.reg1.intval=divmod(self.reg1.intval, self.reg2.intval)
				self.pointeroll2()
			except ZeroDivisionError:
				self.reg2.intval=0
				if self.exception("Zero Division.", -2, cancatch=1):
					return 1, -2, "Zero Division."
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
		#stack1
		elif self.instval.intval == -9100:
			stsubr=self.stack_subparse(self.dataval, self.stack1, -4)
			if stsubr!=None:
				if self.exception("Stack1" + stsubr[1], stsubr[0], cancatch=1):
					return 1, stsubr[0], "Stack1" + stsubr[1]
		#stack2
		elif self.instval.intval == -9101:
			stsubr=self.stack_subparse(self.dataval, self.stack2, -5)
			if stsubr!=None:
				if self.exception("Stack2" + stsubr[1], stsubr[0], cancatch=1):
					return 1, stsubr[0], "Stack2" + stsubr[1]
		#stack3
		elif self.instval.intval == -9102:
			stsubr=self.stack_subparse(self.dataval, self.stack3, -6)
			if stsubr!=None:
				if self.exception("Stack3" + stsubr[1], stsubr[0], cancatch=1):
					return 1, stsubr[0], "Stack3" + stsubr[1]
		#stack4
		elif self.instval.intval == -9103:
			stsubr=self.stack_subparse(self.dataval, self.stack4, -7)
			if stsubr!=None:
				if self.exception("Stack4" + stsubr[1], stsubr[0], cancatch=1):
					return 1, stsubr[0], "Stack4" + stsubr[1]
					
		#stack5
		elif self.instval.intval == -9104:
			stsubr=self.stack_subparse(self.dataval, self.stack5, -8)
			if stsubr!=None:
				if self.exception("Stack5" + stsubr[1], stsubr[0], cancatch=1):
					return 1, stsubr[0], "Stack5" + stsubr[1]
		#stack6
		elif self.instval.intval == -9105:
			stsubr=self.stack_subparse(self.dataval, self.stack6, -9)
			if stsubr!=None:
				if self.exception("Stack6" + stsubr[1], stsubr[0], cancatch=1):
					return 1, stsubr[0], "Stack6" + stsubr[1]
		#soft stop:
		elif self.instval.intval == -9000:
			if self.exception("soft stop.", -1, cancatch=0):
				return 1, -1, "soft stop."
		self.execpoint.intval+=1
		#exreturn
		if self.instval.intval == 102:
			self.exreturn()
		#exclear
		if self.instval.intval == 103:
			self.exclear()
		#exceptcode
		if self.instval.intval == 104:
			self.reg1.intval = self.exceptcode
		
		return None
	def exreturn(self):
		try:
			self.reg1.intval, self.reg2.intval, self.execpoint.intval, self.exceptcode=self.exintreturns.pop(0)
			if self.exceptcode!=0:
				self.exceptflag=1
		except IndexError:
			return
	#clears the Exception status, but keeps going at current address, and doesn't reset registers.
	def exclear(self):
		try:
			foo1, foo2, foo3, self.exceptcode=self.exintreturns.pop(0)
			if self.exceptcode!=0:
				self.exceptflag=1
		except IndexError:
			return
	#pointer rollover code.
	def pointeroll1(self):
		if self.reg1.intval<-9841:
			#while self.reg1.intval<-9841:
			#	self.reg1-=-9841
			self.reg1.changeval(self.reg1.bttrunk(9))
		elif self.reg1.intval>9841:
			#while self.reg1.intval>9841:
			#	self.reg1-=9841
			self.reg1.changeval(self.reg1.bttrunk(9))
		
		return
	def pointeroll2(self):
		if self.reg2.intval<-9841:
			#while self.reg2.intval<-9841:
			#	self.reg2-=-9841
			self.reg2.intval=9841
			self.reg2.changeval(self.reg2.bttrunk(9))
		elif self.reg2.intval>9841:
			#while self.reg2.intval>9841:
			#	self.reg2-=9841
			self.reg2.changeval(self.reg2.bttrunk(9))
		return
	
	
	
	#goto function
	def goto(self, address):
		self.execpoint.intval=address
		return
	def stack_subparse(self, dataval, stacklist, baseexcept):
		#pop
		if dataval.intval==0:
			try:
				self.reg1.intval=stacklist.pop(0)
				return None
			except IndexError:
				return baseexcept, " Underflow"
		elif dataval.intval==1:
			try:
				self.reg2.intval=stacklist.pop(0)
				return None
			except IndexError:
				return baseexcept, " Underflow"
		#push
		elif dataval.intval==2:
			if len(stacklist)>9841:
				return baseexcept-10, " Overflow"
			stacklist.insert(0, self.reg1.intval)
			return None
		elif dataval.intval==3:
			if len(stacklist)>9841:
				return baseexcept-10, " Overflow"
			stacklist.insert(0, self.reg2.intval)
			return None
		#peek
		elif dataval.intval==4:
			try:
				self.reg1.intval=stacklist[0]
				return None
			except IndexError:
				return baseexcept, " Underflow"
		elif dataval.intval==5:
			try:
				self.reg2.intval=stacklist[0]
				return None
			except IndexError:
				return baseexcept, " Underflow"
		elif dataval.intval==6:
			stacklist.reverse()
			
		
	#ensure uncatchable exceptions set the cancatch attribute to zero.
	def exception(self, status, exid, cancatch=1):
		if cancatch:
			self.exints.insert(0, [exid, status])
			self.exceptcode=exid
			self.exceptflg=1
		else:
			self.critfault=[exid, status]
			self.exceptcode=exid
			self.exceptflg=1
			return 1
		
		
		